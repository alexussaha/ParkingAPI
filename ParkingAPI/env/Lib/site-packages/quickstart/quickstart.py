"""Quickstart to create frameworks for projects"""

import os
from os import path
import quickstart.console as out

__display_version__ = "v0.3"

__bin_dir__ = os.path.dirname(__file__)


def mkdir(folder):
    """Creates a new directory at dir"""
    if path.isdir(folder):
        return
    os.makedirs(folder)


def write(source, dest, replace_list):
    """
    Creates a file copied from source to dest, and replaces matches with
    replacement from replace_list
    """
    source = path.join(__bin_dir__, "templates/", source)
    with open(source, 'r') as file:
        filedata = file.read()

    for search_str, replace_str in replace_list:
        filedata = filedata.replace(search_str, replace_str)

    with open(dest, 'w') as file:
        file.write(filedata)


def gen_folders(folders):
    """Generates all folders for project"""
    out.section("Folders", 25)
    for folder in folders:
        mkdir(folder)
        print(out.green("Generated ") + out.magenta("\"%s\"" % folder))


def gen_files(files, replace):
    """Generates all files for project"""
    out.section("Files", 25)
    for source, dest in files:
        write(source, dest, replace)
        print(out.green("Copied ") + out.magenta("\"%s\"" % str(source)))


def gen_commands(commands):
    """Run all commands for project"""
    out.section("Commands", 25)
    for exe in commands:
        os.system(exe)
        print(out.green("Ran ") + out.magenta("\"%s\"" % str(exe)))


def generate(files, folders, commands, replace):
    """Generates project folders/files/commands"""
    out.title("Genrating", 25)
    gen_folders(folders)
    gen_files(files, replace)
    gen_commands(commands)


def main():
    """allows user to enter data for project, and genorates project"""
    out.clear()
    out.title("Quickstart Utility %s" % __display_version__, 25)
    data = {}
    out.select_list(data, 'lang', "Languages", ["C++", "C++ (Default)"])
    folders = []
    files = []
    print()
    if data['lang'] == "C++":
        import quickstart.languages.cpp
        folders, files, commands, replace = quickstart.languages.cpp.main(data)
    elif data['lang'] == "C++ (Default)":
        import quickstart.languages.cpp
        folders, files, commands, replace = quickstart.languages.cpp.default(
            data)
    else:
        print(out.red("Not a valid type \"%s\"" % data['lang']))

    generate(files, folders, commands, replace)


if __name__ == "__main__":
    main()
