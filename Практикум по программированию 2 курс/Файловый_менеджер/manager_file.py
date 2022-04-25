import os
import shutil
import sys
from config import main_folder


def recursion_folders(*names):
    make_folders(*names, recursive=True)


def print_folder_work():
    global current_directory
    print('/'+'/'.join(current_directory[1:]))


def path_reader(path, mode=True):
    global current_directory
    path = [item for el in path.split('\\') for item in el.split('/')]
    if path[0] == '.':
        path = list(current_directory + path[1:])
    elif path[0] == '..':
        if len(current_directory) > 1:
            path = list(current_directory[:-1] + path[1:])
        else:
            path = list(current_directory + path[1:])
    elif path[0] == '':
        path[0] = main_folder
    else:
        path = list(current_directory + path)
    secondary = '/'+'/'.join(path[1:]) if mode else path
    return os.path.join(*path), secondary


def make_folders(*names, recursive=False):
    for name in names:
        path = path_reader(name)
        try:
            os.makedirs(path[0]) if recursive else os.mkdir(path[0])
        except FileExistsError:
            print(f'Directory has already exist: {path[1]}')
        except FileNotFoundError:
            print(f'Invalid path: {path[1]}')


def remove_folders(*names, recursive=False):
    for name in names:
        path = path_reader(name)
        try:
            if recursive:
                tree = list(os.walk(path[0]))[::-1]
                for objects in tree:
                    for item in objects[1]:
                        os.rmdir(os.path.join(objects[0], item))
                    for item in objects[2]:
                        os.remove(os.path.join(objects[0], item))
                os.rmdir(objects[0])
            else:
                os.rmdir(path[0])
        except FileNotFoundError:
            print(f'Invlid path {path[1]}')
        except OSError:
            print(f'Folder isn\'n empty {path[1]} (use rmflds)')


def recursion_remove_folders(*names):
    remove_folders(*names, recursive=True)


def go_to_folder(name):
    global current_directory
    path = path_reader(name, mode=False)
    if os.path.exists(path[0]):
        current_directory = list(path[1])
    else:
        print('No such file or directory')


def create_file(*names):
    for name in names:
        path = path_reader(name)
        try:
            with open(path[0], 'x'):
                pass
        except FileExistsError:
            pass


def write_file(name):
    path = path_reader(name)
    print("Ctrl-Z (Windows) or Ctrl-D (Unix) for close")
    try:
        with open(path[0], 'a') as file:
            while True:
                try:
                    file.write(input()+'\n')
                except EOFError:
                    break
    except FileExistsError:
        print(f'File doesn\'t exist {path[1]}')


def read_file(*names):
    for name in names:
        path = path_reader(name)
        try:
            with open(path[0], 'r') as file:
                for line in file.readlines():
                    print(line, end='')
        except FileExistsError:
            print(f'File doesn\'t exist {path[1]}')


def remove_file(*names):
    for name in names:
        path = path_reader(name)
        try:
            os.remove(path[0])
        except FileNotFoundError:
            print(f'Invlid path {path[1]}')


def copy_file(from_, to_):
    from_ = path_reader(from_)
    to_ = path_reader(to_)
    if sys.platform == 'win32':
        os.system(f'copy "{from_[0]}" "{to_[0]}"')
    else:
        os.system(f'cp -r {from_[0]} {to_[0]}')


def replace_file(from_, to_):
    from_ = path_reader(from_)
    to_ = path_reader(to_)
    try:
        os.replace(from_[0], to_[0])
    except FileNotFoundError:
        print(f'Invlid path {from_[1], to_[1]}')


def rename_f(name, new_name):
    name = path_reader(name)
    new_name = path_reader(new_name)
    try:
        os.rename(name[0], new_name[0])
    except FileNotFoundError:
        print(f'Invlid path {name[1], new_name[1]}')


def print_help_string():
    help_string = r''''print_folder_work' -- напечатать рабочую папку
'make_folders [folder_name] [folder_name] ..' -- Создание папок
'recursion_folders [folder_name] [folder_name] ..' -- Сделать папки рекурсивными
'remove_folders [folders_name] [folder_name] ..' -- Удаление папок
'recursion_remove_folders [folder_name] [folder_name] ..' -- Рекурсивное удаление папок
'go_to_folder [folder_name]' -- перейдите в папку, измените текущую папку
'create_file [file_name] [file_name] ..' -- создание файлов
'write_file [file_name]' -- запись в файл, ввод строки
'read_file [file_name] [file_name] ..' -- отобразить файл
'remove_file [file_name] [file_name] ..' -- удалить файл
'copy_file [file_from] [file_to]' -- Копировать file_name в folder/new_file
'replace_file [file_folder] [file_folder]' -- замените file/folder на другой file/folder
'rename_f [file_folder]' -- переименовать файл или папку
'exit' -- выход
'help' -- чтобы получить список команд'''
    print(help_string)


def command_prompt():
    global current_directory
    commands = {
        'print_folder_work': print_folder_work,
        'make_folders': make_folders,
        'recursion_folders': recursion_folders,
        'remove_folders': remove_folders,
        'recursion_remove_folders': recursion_remove_folders,
        'go_to_folder': go_to_folder,
        'create_file': create_file,
        'write_file': write_file,
        'read_file': read_file,
        'remove_file': remove_file,
        'copy_file': copy_file,
        'replace_file': replace_file,
        'rename_f': rename_f,
        'help': print_help_string
    }

    while True:
        command = input('Командный запрос:/' +
                        '/'.join(current_directory[1:])+'$ ').split()
        if command[0] == 'exit':
            break
        try:
            commands[command[0]](*command[1:])
        except KeyError:
            print(
                'Неверная команда. Используйте "справка", чтобы просмотреть список команд.')
        except PermissionError:
            print('В разрешении отказано')


current_directory = [main_folder]
command_prompt()
