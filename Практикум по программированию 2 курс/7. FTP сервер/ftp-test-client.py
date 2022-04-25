import socket
import re
import os



test_strings = [
    "mkdir test1",
    "cd ...../test1",
    "cd ./test1",
    "mkdir ../test1/test11",
    "ls",
    "pwd",
    "rmtree test11",
    "ls",
    "touch 1.txt",
    "rename 1.txt 11.txt",
    "ls",
    "remove 1.txt",
    "cat 1.txt",
    "cat 11.txt",
    "cd ////",
    "pwd",
    "cd \\",
    "pwd",
    "rmtree test1",
    "ls"
]

HOST = 'localhost'
PORT = 6666
END_FLAG = b"$$STREAM_FILE_END_FLAG$$"
FAIL_FLAG = b'$FAILED$'

# login = input("Введите логин: ")
# password = input("Введите пароль: ")
login = password = 'test'

current_directory = "\\"

def creator(message, size=0):
    global login, password, current_directory
    return f"{login}=login{password}=password{current_directory}=cur_dir{size}=file_size{message}".encode()


def receiving(request):
    global sock, FAIL_FLAG, END_FLAG
    
    flag_finder = sock.recv(1024)
    if FAIL_FLAG in flag_finder:
        print((flag_finder.replace(FAIL_FLAG, b"")).decode())
    else:
        filename = re.split("[ \\/]+", request)[-1]
        with open (filename, "wb") as bytefile:
            while True:
                if END_FLAG in flag_finder:
                    bytefile.write(flag_finder.replace(END_FLAG, b""))
                    break
                else:
                    bytefile.write(flag_finder)
                    flag_finder = sock.recv(1024)

def sending(request):
    global sock, END_FLAG
    filename = re.split("[ \\/]+", request)[-1]
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        sock.send(creator(request, size))
        enought_flag = sock.recv(1024).decode()
        if enought_flag != '$ENOUGHT$':
            print(enought_flag)
            return
        with open(filename, "rb") as bytefile:
    
            while read_bytes := bytefile.read(1024):
                sock.send(read_bytes)
        sock.send(END_FLAG)
    else:
        print("Нет такого файла")
        
def main(command):
    global current_directory
    sock = socket.socket()
    print(">", command)
    request = command
    request = request.strip()
    if request == "exit":
        print("goodbye")
        return
    
    sock.connect((HOST, PORT))
    if request[:9] == "send_file":
        if request == "send_file":
            print("Нет такого файла")
        else:
            sending(request)
    else:
        sock.send(creator(request))
        if request[:9] == "get_file " or request == "get_file":
            receiving(request)
        else:
            response = sock.recv(1024).decode()
            # print("recieved:", response)
            if request[:3] == "cd " or request == "cd":
                current_directory = response
            else:
                print(response)
    sock.close()

sock = socket.socket()
for command in test_strings:
    try:
        main(command)
    except:
        print('Некорректная работа!')
        raise
