# Ability to read config
from yaml import safe_load 

# Import local class definitions
from gui import UiWindow
from movie import Movie

# Read settings
CONFIG_FILE = "config.yml" 
# Read the file on disk
file = open(CONFIG_FILE, "r")

# Parse the raw YAML data
config = safe_load(file)

# Read config values into variables
THEATRE_ROWS = config['theatre']['rows']
THEATRE_COLS = config['theatre']['cols']
MOVIES = config['movies']

# Create a config object to be used by the UI classes
config = {
    'title': config['window']['title'],
    'col_max': config['theatre']['cols'],
    'row_max': config['theatre']['rows'],
    'bg_color': config['color']['background'],
    'color_free': config['color']['free'],
    'color_claimed': config['color']['claimed'],
    'color_reserved': config['color']['reserved'],
    'app_title': config['window']['title'],
}


# Create a list of Movie objects based on the config data
movies = []
for movie in MOVIES:
    movies.append(Movie(movie, THEATRE_ROWS, THEATRE_COLS))

# Instantiate the main UI class
window = UiWindow(config, movies)

# Run the event loop of the TkInter UI framework
window.mainloop()
