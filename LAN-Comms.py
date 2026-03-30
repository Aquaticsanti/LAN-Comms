from termcolor import colored
import threading
import socket
import time
import os
from readchar import readkey, key
import pickle # im sorry im actually using pickles in my program LMAOO

def cls(): # Source - https://stackoverflow.com/a/684344
    os.system('cls' if os.name=='nt' else 'clear')

def printLoading(text: str, wait: int|float = 3):

    print(f"{text}   ", end="\r")
    time.sleep(wait/4)
    print(f"{text}.  ", end="\r")
    time.sleep(wait/4)
    print(f"{text}.. ", end="\r")
    time.sleep(wait/4)
    print(f"{text}...", end="\r")
    time.sleep(wait/4)
print(colored("""
██╗░░░░░░█████╗░███╗░░██╗░░░░░░░█████╗░░█████╗░███╗░░░███╗███╗░░░███╗░██████╗
██║░░░░░██╔══██╗████╗░██║░░░░░░██╔══██╗██╔══██╗████╗░████║████╗░████║██╔════╝
██║░░░░░███████║██╔██╗██║█████╗██║░░╚═╝██║░░██║██╔████╔██║██╔████╔██║╚█████╗░
██║░░░░░██╔══██║██║╚████║╚════╝██║░░██╗██║░░██║██║╚██╔╝██║██║╚██╔╝██║░╚═══██╗
███████╗██║░░██║██║░╚███║░░░░░░╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░╚═╝░██║██████╔╝
╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝░░░░░░░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚═════╝░""", "light_grey"))
print("Welcome to LAN-Comms!")
print("Please input your desired port.", colored("Leave empty for default (3535)", "dark_grey"))

while True:
    port = input()
    if port == "":
        port = 3535
        break
    try:
        port = int(port)
    except:
        print(f"Uh oh, '{port}' is not a number! Please input a number.")
        continue
    else:
        if port < 0:
            print(f"Uh oh,'{port}' is a negative number! Please input a positive number.")
            continue
        elif port > 65535:
            print(f"Uh oh, '{port}' is higher than 65535! Please input a number lower than 65535.")
            continue
        elif port < 1024:
            print(f"Uh oh, port {port} is a system port! Please choose a number higher than 1024.")
        else:
            break

print(f"Great! Port {port} has been selected!")

thread = threading.Thread(target=printLoading, kwargs={"text": "Connecting", "wait": 3})
thread.start()
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # For debugging purposes, allows 2 clients on the same machine
while thread.is_alive() == True:
    pass
try:
    sock.bind(("0.0.0.0", port))
except Exception as e:
    print(f"Uh oh, looks like something went wrong... {e}")
    os._exit(0)
print("Connected!   ")
print("Please input your username:")
while True:
    username = input()
    if username == "":
        print("Username can't be blank, please choose another username!")
    else:
        break
print("Now, please pick your color. Use the up and down arrow keys to change, and enter to select")
colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
"light_grey", "dark_grey", "light_red", "light_green", "light_yellow", "light_blue",
"light_magenta", "light_cyan"]
selected_color = 0
while True:
    print("", colored(username, colors[selected_color]), end="\r")
    k = readkey()
    if k == key.UP:
        selected_color += 1
        if selected_color > len(colors)-1:
            selected_color = 0
    elif k == key.DOWN:
        selected_color -= 1
        if selected_color < 0:
            selected_color = len(colors)-1
    elif k == key.ENTER:
        print(colored(username, colors[selected_color]), "")
        break

printLoading("Joining", 2.5)
cls()


def receive():
    pass
def send():
    pass
threadSend = threading.Thread(target=send)
threadRecv = threading.Thread(target=receive)

myMsg = input("whachu wanna send: ")
myMsg = {"name": username, "color": selected_color, "msg":myMsg}
sock.sendto(pickle.dumps(myMsg), ("255.255.255.255", port))
message, address = sock.recvfrom(4096)
message = pickle.loads(message)
print(colored(f"[{message["name"]}]: {message["msg"]}", colors[message["color"]]))



    
