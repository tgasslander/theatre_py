# Movie Theatre school hack

Helping my kid to build a skeleton piece of code

# Requirements

- 10 rows
- 15 columns
- Ability to reserve a seat
- Ability to make a group reservation of 2-5 (inclusive) on the same row
- UI

## Concepts

### Separation of Concerns

- Separate configuration from code (config.yml)
- Separate data layer from presentation layer

### OOP

Use object oriented programming

### Callbacks

Provide functions to be executed asyncrhonously.

## Description

Read config from an external file (config.yml) using the `pyyaml` library.
Add the `pyyaml` lib to `requirements.txt` to make it easy to install using `pip`.
Use `tkinter` as UI framework and put the Movies and Seats in their own classes.

### Classes

#### Data layer

##### Movie

`Movie` maintains a list of rows in which it stores `Seat` instances, being created at construction.
It also provides methods to retrieve data, and set the state of the `Seat` objects. Therefore it
imports the `Seat` class.

`Movie` knows how to calculate the first available seats for a group booking and how to reserve its
claimed seats.


##### Seat

`Seat` implements the representation of a movie theatre seat. It knows its state (claimed, free)
and its row and colum.
Additionally it exports methods to set/read the state.

`Seat` knows how to toggle the claimed state and how to mark a seat as reserved.

#### Presentation layer

##### UiWindow

`UiWindow` inherits `tk.Tk` and implements the UI creation and event handling.
Rather than knowing the state of the `Seat` objects or `Movie` objects it simply renders the UI
based on the state it retrieves from the classes in the data layer.

The `redraw` function creates and refreshes the grid of `UiSeats`.


##### UiSeat

`UiSeat` inherits `ttk.Button` and it is the UI representation of the data layer `Seat`.
It knows how to force the UI to redraw
by way of a callback.

##### MovieSelector

`MovieSelector` inherits `ttk.Combobox` and it presents a dropdown with the list of movie titles
that are available. It knows how to force a redraw and how to inform the `UiWindow` about which
movie has been selected.

##### Header

`Header` inherits from `tk.Frame` and builds up UI elements like buttons, a label and an input.
The buttons allow for reserving one or several seats or claiming 2-5 consecutive seats.
It knows how to reserve and claim in the `UiWindow` class by using callbacks.
