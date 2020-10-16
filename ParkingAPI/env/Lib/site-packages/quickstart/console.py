"""Module controls input/output to terminal"""

import subprocess
from os import path
import sys
import tty
import termios


class ValidationError(Exception):
    """Raised for validation errors."""


def is_path(i):
    """Checks if entered value is a path"""
    i = path.expanduser(i)
    if path.exists(i) and not path.isdir(i):
        raise ValidationError("Please enter a valid path name.")
    return i


def allow_empty(i):
    """Validates on all entered values"""
    return i


def nonempty(i):
    """Validates on only non empty values"""
    if not i:
        raise ValidationError("Please enter some text.")
    return i


def boolean(i):
    """Checks if entered value is some boolean"""
    if i.upper() not in ('Y', 'YES', 'N', 'NO'):
        raise ValidationError("Please enter either 'y' or 'n'.")
    return i.upper() in ('Y', 'YES')


def is_type(i):
    """Checks is entered value is either lib or exe"""
    if i.upper() not in ('LIB', 'EXE'):
        raise ValidationError("Pleasse enter either 'lib' or 'exe'.")
    return i


def is_list(i):
    """Converts entered value into a list"""
    i = i.split(' ')
    return i


def title(text, size=-1):
    """Prints underlined title"""
    print(white(bold(text)))
    if size != -1:
        print(white(bold("=" * size)))
    else:
        print(white(bold("=" * len(text))))


def sub_title(text, size=-1):
    """Prints underlined subtitle"""
    print(white(text))
    if size != -1:
        print(white("-" * size))
    else:
        print(white("-" * len(text)))


def section(text, size=-1):
    """Prints section title"""
    if size != -1 and size > len(text):
        width = int((size - len(text)) / 2)
        print(cyan("\n" + '=' * width + text + '=' * width + "\n"))
    else:
        print(cyan(text))


def term_input(prompt_str):
    """Gets input from user"""
    print(prompt_str, end='')
    print('\033[1m', end='')
    out = input('')
    print('\033[21m', end='')
    return out


def prompt(data, name, description, default=None, validator=nonempty, indent=0):
    """Runs prompt for specified data"""
    if name in data:
        if default is not None:
            if data[name] is True:
                print(' ' * indent + magenta(
                    "%s [%s]: " % (description, default)) + bold("Yes"))
            elif data[name] is False:
                print(' ' * indent + magenta(
                    "%s [%s]: " % (description, default)) + bold("No"))
            else:
                print(' ' * indent + magenta("%s [%s]: " % (
                    description, default)) + bold("%s" % data[name]))
        else:
            if data[name] is True:
                print(' ' * indent + magenta("%s: " % description) +
                      bold("True"))
            elif data[name] is False:
                print(' ' * indent + magenta("%s: " % description) +
                      bold("False"))
            else:
                print(' ' * indent + magenta("%s: " % description) + bold(
                    "%s" % data[name]))
    else:
        while True:
            if default is not None:
                prompt_str = ' ' * indent + '%s [%s]: ' % (description, default)
            else:
                prompt_str = ' ' * indent + description + ': '
            prompt_str = prompt_str.encode('utf-8')
            prompt_str = magenta(prompt_str.decode("utf-8"))
            i = term_input(prompt_str).strip()
            if default and not i:
                i = default
            try:
                i = validator(i)
            except ValidationError as err:
                print(' ' * indent + bold(red('* ' + str(err))))
                continue
            break
        if i is default or i is True or i is False:
            print("\033[1A\r", end='')
            if default is not None:
                if i is True:
                    print(' ' * indent + magenta(
                        "%s [%s]: " % (description, default)) + bold("Yes"))
                elif i is False:
                    print(' ' * indent + magenta(
                        "%s [%s]: " % (description, default)) + bold("No"))
                else:
                    print(' ' * indent + magenta(
                        "%s [%s]: " % (description, default)) + bold("%s" % i))
            else:
                if i is True:
                    print(' ' * indent + magenta("%s: " % description) +
                          bold("True"))
                elif i is False:
                    print(' ' * indent + magenta("%s: " % description) +
                          bold("False"))
                else:
                    print(' ' * indent + magenta("%s: " % description) + bold(
                        "%s" % i))
        data[name] = i


def select_list(data, name, disp, options, show_title=True):
    """Select data option from interactive list"""
    select = 0
    if show_title is True:
        sub_title(disp, 25)
    if show_title is False:
        print(magenta(disp))
    running = True
    if name in data:
        running = False
    while running is True:
        for i, string in enumerate(options):
            if i == select:
                print("  " + reverse(magenta("(%i) " % i + string)))
            else:
                print("  " + magenta("(%i) " % i + string))
        print(">>\033[1m", end='')
        key = input()
        print("\033[21m")
        if key == '':
            running = False
        elif int(key) < len(options) and int(key) >= 0:
            select = int(key)
        if running is True:
            for i in range(0, len(options) + 2):
                print("\033[1A\r" + ' ' * 25 + '\r', end='')
    if show_title is False:
        if name not in data:
            for i in range(0, len(options) + 3):
                print("\033[1A\r" + ' ' * 25 + '\r', end='')
        else:
            print("\033[1A\r" + ' ' * 25 + '\r', end='')
        print(magenta("%s [%s]: " % (disp, options[0])) +
              bold(white("%s" % options[select])))
    else:
        if name not in data:
            for i in range(0, len(options) + 2):
                print("\033[1A\r" + ' ' * 25 + '\r', end='')
        else:
            print("\033[1A\r" + ' ' * 25 + '\r', end='')
        for i, string in enumerate(options):
            if i == select:
                print("  " + bold(white("(%i) %s" % (i, string))))
            else:
                print("  " + magenta("(%i) %s" % (i, string)))
    data[name] = options[select]


def set_cursor(line, col):
    """Sets the terminal cursor position"""
    print("\033[%i;%iH" % (line, col))


def clear():
    """Clears the terminal of output"""
    subprocess.call("clear", shell=True)


def create_attr(name):
    """Creates set attibute functions"""

    def inner(text):
        """Sets text to use applied attibute"""
        return "\033[%s" % _attrs[name][0] + text + "\033[%s" % _attrs[name][1]

    globals()[name] = inner


def create_color(name):
    """Creates set color functions"""

    def inner(text):
        """Sets text to use applied color"""
        return "\033[%s" % _colors[name][0] + text + "\033[%s" % _colors[name][1]

    globals()[name] = inner


_attrs = {
    'bold': ('01m', '21m'),
    'dim': ('02m', '22m'),
    'underlined': ('03m', '24m'),
    'blink': ('05m', '25m'),
    'reverse': ('07m', '27m'),
    'hidden': ('08m', '28m')
}

_colors = {
    'red': ('31m', '39m'),
    'green': ('32m', '39m'),
    'yellow': ('33m', '39m'),
    'blue': ('34m', '39m'),
    'magenta': ('35m', '39m'),
    'cyan': ('36m', '39m'),
    'grey': ('27m', '39m'),
    'white': ('97m', '39m')
}

for _name in _attrs:
    create_attr(_name)
for _name in _colors:
    create_color(_name)


class _Getch:

    def __call__(self, count):
        fdin = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fdin)
        try:
            tty.setraw(sys.stdin.fileno())
            chin = sys.stdin.read(count)
        finally:
            termios.tcsetattr(fdin, termios.TCSADRAIN, old_settings)
        return chin


getch = _Getch()
