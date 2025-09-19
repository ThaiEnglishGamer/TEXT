import curses
import json
import os
import importlib

class TextEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.load_config()
        self.load_plugins()
        self.text = ""
        self.cursor_x = 0
        self.cursor_y = 0
        self.current_page = "EDITOR"
        self.run()

    def load_config(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)

    def load_plugins(self):
        self.plugins = []
        plugins_dir = "plugins"
        for filename in os.listdir(plugins_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{plugins_dir}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                if hasattr(module, "Plugin"):
                    self.plugins.append(module.Plugin())

    def run(self):
        curses.curs_set(1)
        self.stdscr.nodelay(1)
        while True:
            self.draw()
            key = self.stdscr.getch()
            if key != -1:
                if self.current_page == "EDITOR":
                    self.handle_editor_input(key)
                elif self.current_page == "HELP":
                    self.handle_help_input(key)
                elif self.current_page == "SETTING":
                    self.handle_setting_input(key)

    def draw(self):
        self.stdscr.clear()
        if self.current_page == "EDITOR":
            self.draw_editor()
        elif self.current_page == "HELP":
            self.draw_help()
        elif self.current_page == "SETTING":
            self.draw_setting()
        self.stdscr.refresh()

    def draw_editor(self):
        for i, line in enumerate(self.text.split("\n")):
            self.stdscr.addstr(i, 0, line)
        self.stdscr.move(self.cursor_y, self.cursor_x)

    def draw_help(self):
        self.stdscr.addstr(0, 0, "HELP PAGE")
        for i, (key, desc) in enumerate(self.config["keybinds"].items()):
            self.stdscr.addstr(i + 2, 0, f"{key}: {desc}")

    def draw_setting(self):
        self.stdscr.addstr(0, 0, "SETTINGS PAGE")
        self.stdscr.addstr(2, 0, "Loaded Plugins:")
        for i, plugin in enumerate(self.plugins):
            self.stdscr.addstr(i + 3, 2, f"- {plugin.name}")

    def handle_editor_input(self, key):
        if key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_y += 1
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x += 1
        elif key == curses.KEY_BACKSPACE or key == 127:
            if self.cursor_x > 0:
                lines = self.text.split("\n")
                lines[self.cursor_y] = lines[self.cursor_y][:self.cursor_x - 1] + lines[self.cursor_y][self.cursor_x:]
                self.text = "\n".join(lines)
                self.cursor_x -= 1
        elif key == 27: # Escape key
            exit()
        elif key == curses.KEY_F1:
            self.current_page = "HELP"
        elif key == curses.KEY_F2:
            self.current_page = "SETTING"
        else:
            lines = self.text.split("\n")
            if self.cursor_y >= len(lines):
                lines.append("")
            lines[self.cursor_y] = lines[self.cursor_y][:self.cursor_x] + chr(key) + lines[self.cursor_y][self.cursor_x:]
            self.text = "\n".join(lines)
            self.cursor_x += 1

    def handle_help_input(self, key):
        if key == curses.KEY_F1:
            self.current_page = "EDITOR"

    def handle_setting_input(self, key):
        if key == curses.KEY_F2:
            self.current_page = "EDITOR"

def main(stdscr):
    TextEditor(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)