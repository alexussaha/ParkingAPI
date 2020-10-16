"""Loads default values for C++ projects"""

import os
from os import path
import quickstart.console as out


def load_files(data):
    """Sets folders, files, replacement strings and commands"""
    source_dir = path.join(data['root'], data['source_dir'])
    include_dir = path.join(data['root'], data['include_dir'])
    build_dir = path.join(data['root'], data['build_dir'])
    ext_dir = path.join(data['root'], data['ext_dir'])

    for i, string in enumerate(data['link']):
        data['link'][i] = '-l' + string + ' '

    folders = [data['root'], source_dir, include_dir, build_dir, ext_dir]
    files = [('cpp/source/main.cpp', path.join(source_dir, 'main.cpp')),
             ('cpp/clang-format', path.join(data['root'], 'clang-format'))]
    commands = []
    replace = []
    replace.append(("project_name", data['name']))
    replace.append(("project_title", data['name'].title()))
    replace.append(("project_description", data['description']))
    replace.append(("project_type", data['type']))
    replace.append(("project_source_dir", data['source_dir']))
    replace.append(("project_include_dir", data['include_dir']))
    replace.append(("project_build_dir", data['build_dir']))
    replace.append(("project_ext_dir", data['ext_dir']))
    replace.append(("project_link", ''.join(data['link'])))

    if data['git'] is True:
        commands.append("cd %s && git init" % data['root'])
        files.append(("cpp/.gitignore", path.join(data['root'], ".gitignore")))
        if data['tests'] is True:
            commands.append(
                "cd %s && git submodule add https://github.com/google/googletest %s/googletest"
                % (data['root'], data['ext_dir']))

            if data['tests'] is True:
                test_dir = path.join(data['root'], data['test_dir'])
        folders.append(test_dir)
        files.append(("cpp/test/tmp.cpp", path.join(test_dir, "tmp.cpp")))
        files.append(("cpp/external/Makefile_t", path.join(ext_dir,
                                                           "Makefile")))
        replace.append(("project_test_dir", data['test_dir']))
    else:
        files.append(("cpp/external/Makefile", path.join(ext_dir, "Makefile")))

    if data['docs'] is True:
        doc_dir = path.join(data['root'], data['doc_dir'])
        folders.append(doc_dir)
        replace.append(("project_doc_dir", data['doc_dir']))
        if data['doc-sys'] == "MkDocs":
            folders.append(path.join(doc_dir, 'css'))
            files.append(('cpp/mkdocs.yml', path.join(data['root'],
                                                      'mkdocs.yml')))
            files.append(('cpp/docs/index.md', path.join(doc_dir, 'index.md')))
            files.append(('cpp/docs/css/extra.css', path.join(
                doc_dir, 'css/extra.md')))
            if "mkdocs" not in data['pip-install']:
                data['pip-install'].append("mkdocs")
            if "pygments" not in data['pip-install']:
                data['pip-install'].append("pygments")
        elif data['doc-sys'] == "Sphinx":
            pass

    if data['comp'] == "GNU Make":
        files.append(("cpp/Makefile", path.join(data['root'], "Makefile")))
        files.append(("cpp/source/Makefile", path.join(source_dir, "Makefile")))
        if data['tests'] is True:
            files.append(("cpp/test/Makefile", path.join(
                data['root'], data['test_dir'], "Makefile")))

    if data['ci'] is True:
        ci_file = ["cpp/", ""]
        if data['ci-server'] == "Travis-CI":
            ci_file[0] += "travis"
            ci_file[1] = path.join(data['root'], ".travis.yml")

        if data['deploy-pages'] is True:
            ci_file[0] += "_dp"

        if data['coverage'] == "CodeCov":
            ci_file[0] += "_cc"
            files.append(("cpp/.codecov.yml", path.join(data['root'],
                                                        ".codecov.yml")))

        ci_file[0] += ".yml"
        files.append(ci_file)

        project_apt = "- sudo apt-get install "
        if data['apt-install'] == []:
            project_apt = ""
        else:
            for pack in data['apt-install']:
                project_apt += str(pack) + ' '

        replace.append(("project_apt", str(project_apt)))

        print(project_apt)

        project_pip = "- sudo pip install "
        if data['pip-install'] == []:
            project_pip = ""
        else:
            for pack in data['pip-install']:
                project_pip += str(pack) + ' '

        replace.append(("project_pip", str(project_pip)))

        print(project_pip)

    return folders, files, commands, replace


def main(data):
    """Prompts user for missing data for c++ projects"""
    out.sub_title("C++", 25)
    out.section("General", 25)
    out.prompt(data, 'name', 'Project name', None, out.nonempty)
    out.prompt(data, 'description', 'Project description', None,
               out.allow_empty)
    out.prompt(data, 'type', 'Project type (lib/exe)', 'lib', out.is_type)
    out.prompt(data, 'git', 'Create git repo', 'Yes', out.boolean)
    out.section("Directories", 25)
    current_dir = path.basename(os.getcwd())
    if current_dir.lower() == data['name'].lower():
        out.prompt(data, 'root', 'Root directory', '.', out.is_path)
    else:
        out.prompt(data, 'root', 'Root directory', data['name'].lower(),
                   out.is_path)
    out.prompt(data, 'source_dir', 'Source directory', 'source', out.is_path)
    out.prompt(data, 'include_dir', 'Include directory', 'include', out.is_path)
    out.prompt(data, 'build_dir', 'Build directory', 'build', out.is_path)
    out.prompt(data, 'ext_dir', 'External directory', 'external', out.is_path)
    out.section("Unit Tests", 25)
    out.prompt(data, 'tests', 'Enable unit tests', 'Yes', out.boolean)
    if data['tests'] is True:
        out.prompt(data, 'test_dir', 'Test directory', 'test', out.is_path)
    out.section("Documentation", 25)
    out.prompt(data, 'docs', 'Create documentation', 'Yes', out.boolean)
    if data['docs'] is True:
        out.select_list(data, 'doc-sys', 'Documentation Constructor',
                        ['MkDocs', 'Sphinx', 'None'], False)
        out.prompt(data, 'doc_dir', 'Documentation directory', 'docs',
                   out.is_path)
        out.section("Compiling", 25)
    out.select_list(data, 'comp', 'Compiler', ['GNU Make'], False)
    out.prompt(data, 'link', 'Lined libraries', '', out.is_list)
    out.section("Continuous Integration", 25)
    out.prompt(data, 'ci', 'Enable continuous integration', 'Yes', out.boolean)
    if data['ci'] is True:
        out.select_list(data, 'ci-server', 'Continuous Integration Server',
                        ['Travis-CI'], False)
        out.prompt(data, 'deploy-pages', 'Auto deploy Github pages', 'Yes',
                   out.boolean)
        out.prompt(data, 'apt-install', 'Install from apt-get', '', out.is_list)
        out.prompt(data, 'pip-install', 'Install from pip', '', out.is_list)
        out.select_list(data, 'coverage', "Code Coverage", ['CodeCov', 'None'],
                        False)
        print()
    return load_files(data)


def default(data):
    """Creates project with default settings"""
    data['description'] = ''
    data['type'] = 'lib'
    data['git'] = True
    data['source_dir'] = 'source'
    data['include_dir'] = 'include'
    data['build_dir'] = 'build'
    data['ext_dir'] = 'external'
    data['tests'] = True
    data['test_dir'] = 'test'
    data['docs'] = True
    data['doc_dir'] = 'doc'
    data['doc-sys'] = 'MkDocs'
    data['comp'] = 'GNU Make'
    data['link'] = []
    data['ci'] = True
    data['ci-server'] = 'Travis-CI'
    data['deploy-pages'] = True
    data['apt-install'] = []
    data['pip-install'] = []
    data['coverage'] = 'CodeCov'
    return main(data)
