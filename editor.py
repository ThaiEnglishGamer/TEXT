import curses
import os

class Editor:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config
        self.lines = [""]
        self.cursor_y, self.cursor_x = 0, 0
        self.top_line = 0
        self.filename = None

        curses.curs_set(1)
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)

    def run(self):
        while True:
            self.render()
            key = self.stdscr.getch()
            if key == -1:
                continue

            if key == 27:  # Escape key to exit
                break
            elif key == curses.KEY_UP:
                self.move_cursor(-1, 0)
            elif key == curses.KEY_DOWN:
                self.move_cursor(1, 0)
            elif key == curses.KEY_LEFT:
                self.move_cursor(0, -1)
            elif key == curses.KEY_RIGHT:
                self.move_cursor(0, 1)
            elif key == curses.KEY_BACKSPACE or key == 127:
                self.delete_char()
            elif key == 10:  # Enter key
                self.insert_newline()
            elif 32 <= key <= 126:
                self.insert_char(chr(key))

    def render(self):
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()

        for i, line in enumerate(self.lines[self.top_line:self.top_line + height -1]):
            self.stdscr.addstr(i, 0, line)

        self.stdscr.move(self.cursor_y - self.top_line, self.cursor_x)
        self.stdscr.refresh()

    def move_cursor(self, dy, dx):
        new_y = self.cursor_y + dy
        new_x = self.cursor_x + dx

        if 0 <= new_y < len(self.lines):
            self.cursor_y = new_y

        if 0 <= new_x <= len(self.lines[self.cursor_y]):
            self.cursor_x = new_x

    def insert_char(self, char):
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[:self.cursor_x] + char + line[self.cursor_x:]
        self.cursor_x += 1

    def delete_char(self):
        if self.cursor_x > 0:
            line = self.lines[self.cursor_y]
            self.lines[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            current_line = self.lines.pop(self.cursor_y)
            self.cursor_y -= 1
            self.cursor_x = len(self.lines[self.cursor_y])
            self.lines[self.cursor_y] += current_line

    def insert_newline(self):
        line = self.lines[self.cursor_y]
        self.lines[self.cursor_y] = line[:self.cursor_x]
        self.lines.insert(self.cursor_y + 1, line[self.cursor_x:])
        self.cursor_y += 1
        self.cursor_x = 0