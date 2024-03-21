import tkinter as tk
from tkinter import ttk

class UiSeat(ttk.Button):
    ''' Augment the ttk.Button to represent a clickable Seat widget '''
    CLAIMED_STYLE = 'Claimed.TButton'
    RESERVED_STYLE = 'Reserved.TButton'
    FREE_STYLE = 'Free.TButton'

    def __init__(self, container, seat, config, redraw_cb):
        # Store the redraw callback from the calling class
        self.redraw = redraw_cb

        # Create styles to show different states of the button
        style = ttk.Style()
        style.configure(self.FREE_STYLE, font=
                        ('calibri', 10, 'bold'),
                        foreground = 'black', background = config['color_free'])

        style_claimed = ttk.Style()
        style_claimed.configure(self.CLAIMED_STYLE, background=config['color_claimed'])

        style_reserved = ttk.Style()
        style_reserved.configure(self.RESERVED_STYLE, background=config['color_reserved'])

        # Set the default style
        self.current_style = self.FREE_STYLE

        # If claimed, select the claimed style
        if seat.is_claimed():
            self.current_style = self.CLAIMED_STYLE

        # If not free, select the reserved style
        if not seat.is_free():
            self.current_style = self.RESERVED_STYLE

        # Call the parent's constructor and apply the chosen style from above
        super().__init__(container,
                         style=self.current_style,
                         text=seat.get_label())


        # Bind the left button click event to the on_click method
        self.bind('<Button-1>', self.on_click)

        # Store the seat data class in this instance
        self.seat = seat

    def on_click(self, event):
        ''' Click handler method '''
        print(f'clicked {event.widget}, {self.seat.get_label()}')

        # Ignore clicks if this seat has already been reserved
        if not self.seat.is_free():
            return

        # Toggle the claimed state and update the styling
        self.seat.toggle_claim()
        if self.seat.is_claimed():
            self.config(style=self.CLAIMED_STYLE)
        else:
            self.config(style=self.FREE_STYLE)
        self.redraw()


class MovieSelector(ttk.Combobox):
    ''' Augment the ttk.Combobox class with application specific behavior '''
    titles = []

    def __init__(self, container, movies, redraw_cb, set_movie_cb, **kwargs):
        # Store callbacks into the calling class
        self.redraw = redraw_cb
        self.set_movie = set_movie_cb

        # Store non-function member variables
        self.movies = movies
        self.width = 0

        # Figure out a suitable width of the Combobox by calculating the length
        # of the longest title
        for m in movies:
            title = m.get_title()
            self.titles.append(title)
            title_len = len(title)
            if self.width < title_len:
                self.width = title_len

        # Construct the base class
        super().__init__(container, **kwargs);

        # Add the selectable values
        self['values'] = self.titles

        # Set the default value (first movie in the list)
        self.set(self['values'][0])

        # Set the width to fit the longest title
        self.config(width=self.width)

        # Bind the selection event
        self.bind('<<ComboboxSelected>>', self.on_select)

    def on_select(self, event):
        ''' Compare the selected string with the titles in this instance to find out
            which movie was selected and set it as the selected one in the calling class
        '''
        for movie in self.movies:
            if movie.get_title() == self.get():
                print(f'switch to: {movie.get_title()}')
                self.set_movie(movie)
                self.redraw()

class Header(tk.Frame):
    ''' Create a top frame to put the title and booking button in '''
    def __init__(self, parent, config, reserve_cb, group_claim_cb, **kwargs):
        self.reserve = reserve_cb
        self.group_claim = group_claim_cb

        super().__init__(parent, **kwargs)

        # Create the actual frame of this widget 
        top_frame = tk.Frame(self, bg=config['bg_color'])
        top_frame.pack(side=tk.TOP, fill=tk.X)
        label = ttk.Label(top_frame, text=config['app_title'])
        label.pack()

        # Create the reservation button and connect it to the self.reserve method
        self.reserve_button = ttk.Button(self,
                                         text="Reserve",
                                         command=self.reserve,
                                         state=tk.DISABLED)
        self.reserve_button.pack()

        # Create the group booking button and connect it to the self.group_reserve method
        self.multi_button = ttk.Button(self,
                                  text="Group booking",
                                  command=self.group_reserve,
                                  state=tk.DISABLED)
        self.multi_button.pack()

        # Register validation functions for the input field
        vcmd = (self.register(self.is_number), '%S')
        invcmd = self.register(self.on_non_number)
        # Create the input fied and connect the validation functions to it
        self.input = tk.Entry(self,
                              validate="key",
                              validatecommand=vcmd,
                              invalidcommand=invcmd)
        self.input.pack()

    def is_number(self, val):
        ''' make sure that the input value is within range and an actual number '''
        if not val.isdigit():
            return False
        if 1 < int(val) < 6:
            self.multi_button.config(state=tk.NORMAL)
            return True
        return False

    def on_non_number(self):
        ''' handler for when text field input validation failed '''
        print('Must input a number between 2 and 5!')

    def group_reserve(self):
        ''' attempt reserving the requested number of seats '''
        number = self.input.get()
        if 1 < int(number) < 6:
            self.group_claim(int(number))
        print(number)

    def reserve_btn_enabled(self, enabled):
        ''' enable or disable the reservation button '''
        if enabled:
            new_state = tk.NORMAL
        else:
            new_state = tk.DISABLED
        self.reserve_button.config(state=new_state)

class UiWindow(tk.Tk):
    ''' Main UI class to connect all widgets and layout the window '''

    def __init__(self, config, movies):
        super().__init__()

        self.config = config
        self.bg_color = config['bg_color']

        ## Set up window properties
        self.title(config['title'])
        self.geometry("720x550")
        self.resizable(width=True, height=True)

        # Add the header element on top
        self.header = Header(self, config, self.reserve, self.claim_group)
        self.header.pack()

        # Create a left frame to put the movie selector in
        left_frame = tk.Frame(self, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        movie_selector = MovieSelector(left_frame, movies, self.redraw, self.set_movie)
        movie_selector.pack()

        # Create a frame for the seat rows
        seat_grid = tk.Frame(self, bg=self.bg_color)
        seat_grid.pack(side="top", fill="both", expand = True)
        self.seat_grid = seat_grid

        # Draw the first movie in the list
        self.movie = movies[0]
        self.redraw()

        # Put an exit button on the bottom
        bottom_frame = tk.Frame(self, bg=self.bg_color)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Button(bottom_frame,
                   text="Quit",
                   command=self.destroy).grid(column=1, row=config['row_max']+1)

    def claim_group(self, number):
        ''' claim a group of seats using the data layer '''
        group = self.movie.claim_group(number)

        # if the return array has no elements, no consecutive seats were found
        if len(group) == 0:
            print(f'cannot find {number} consecutive seats!')
        else:
            self.redraw()

    def reserve(self):
        ''' mark the selected seats as reserved in the data layer '''
        self.movie.reserve_seats()
        self.redraw()

    def set_movie(self, movie):
        ''' store the currently selected movie '''
        self.movie = movie


    def redraw(self):
        print(f'redraw: {self.movie.get_title()} claimed: {self.movie.num_claimed()}')

        # Clear the seat_grid by getting all the children (UiSeat:s) and destroy them
        for btn in self.seat_grid.winfo_children():
            btn.destroy()

        # Build the seat_grid
        for row in self.movie.get_rows():
            for seat in row:
                UiSeat(self.seat_grid, seat, self.config, self.redraw).grid(
                            column=seat.get_col(),
                            row=seat.get_row())

        # Make sure to enable the reservation button only if there are claimed seats
        self.header.reserve_btn_enabled(self.movie.num_claimed() > 0)
