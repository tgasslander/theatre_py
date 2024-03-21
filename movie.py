from seat import Seat

class Movie:
    ''' Uber class to hold an entire Movie including metadata and seats '''

    def __init__(self, movie, rows, cols):
        self.name = movie['name']
        self.price = movie['price']
        self.date = movie['date']
        self.time = movie['time']
        self._setup(rows, cols)

    def _setup(self, rows, cols):
        ''' Create seats, row by row and column by column '''
        self.rows = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(Seat(r,c))
            self.rows.append(row)

    def get_rows(self):
        ''' Return all rows '''
        return self.rows

    def display(self):
        ''' For debugging purposes '''
        print('movie::display')
        print(f'name: {self.name}')
        print(f'date: {self.date}')
        print(f'time: {self.time}')
        print(f'price: {self.price}')
        for r in self.rows:
            for s in r:
                s.display()

    def get_title(self):
        ''' Return the title of the movie '''
        return self.name

    def num_claimed(self):
        ''' Return the number of claimed seats in this movie '''
        claimed = 0
        for row in self.rows:
            for c in row:
                if c.is_claimed():
                    claimed = claimed + 1

        return claimed

    def reserve_seats(self):
        ''' Convert claimed seats to reserved '''
        for r in self.rows:
            for seat in r:
                if seat.is_claimed() and seat.is_free():
                    seat.reserve()

    def claim_group(self, number):
        ''' Traverse the seats, row by row, and try to claim `number` consecutive seats '''
        group = []
        for r in self.rows:
            group.clear() # Always clear so that all `number` people can sit on the same row
            for seat in r:
                if not seat.is_claimed() and seat.is_free():
                    col = seat.get_col()
                    # Check that the cols are consecutive by comparing the current
                    # column with the previously stored seat
                    if len(group) > 0:
                        prev_seat = group[-1]
                        prev_col = prev_seat.get_col()

                        # If the current Seat is next to the previous, store it
                        if col == 0 or col == prev_col + 1:
                            group.append(seat)
                        else: # otherwise, start over
                            group.clear()
                    else:
                        group.append(seat)

                    # If we've found a `number` of consecutive seats, we're done
                    # so let's set them to claimed and return
                    if len(group) == number:
                        for s in group:
                            s.toggle_claim()
                        return group
