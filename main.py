import curses
import json
from editor import Editor

def main(stdscr):
    """
    The main function to run the text editor.
    """
    with open('config.json', 'r') as f:
        config = json.load(f)

    editor = Editor(stdscr, config)
    editor.run()

if __name__ == "__main__":
    curses.wrapper(main)