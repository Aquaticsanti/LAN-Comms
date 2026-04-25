from termcolor import colored
import threading
import socket
import time
import os
from readchar import readkey, key
import pickle # im sorry im actually using pickles in my program LMAOO
import atexit
import pyperclip

def cls(): # Source - https://stackoverflow.com/a/684344
    os.system('cls' if os.name=='nt' else 'clear')

def printLoading(text: str, wait: int|float = 3):
    global connected
    print(f"{text}   ", end="\r")
    time.sleep(wait/4)
    if connected == True:
        return
    print(f"{text}.  ", end="\r")
    time.sleep(wait/4)
    if connected == True:
        return
    print(f"{text}.. ", end="\r")
    time.sleep(wait/4)
    if connected == True:
        return
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
connected = False
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
connected = True
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

connected = False
printLoading("Joining", 1)
cls()
allMsg = []

def receive():
    global allMsg
    message = sock.recvfrom(4096)
    message = pickle.loads(message[0])
    allMsg.append(message)

def send():
    global myMsg
    global myMsgText
    myMsg = {"name": username, "color": selected_color, "msg":"".join(myMsgText)}
    sock.sendto(pickle.dumps(myMsg), ("255.255.255.255", port))
    myMsgText = []

def getKeyStroke():
    global myMsgText
    global threadSend
    k = readkey()
    if k == key.ENTER:
        threadSend = threading.Thread(target=send)
        threadSend.start()
    elif k == key.BACKSPACE:
        try:
            myMsgText.pop()
        except IndexError:
            pass
    elif k == key.PAGE_DOWN:
        myMsgText.append(pyperclip.paste())
    elif type(k) == str:
        myMsgText.append(k)
# print(colored(f"[{message["name"]}]: {message["msg"]}", colors[message["color"]]))
threadSend = threading.Thread(target=send)
threadRecv = threading.Thread(target=receive)
threadType = threading.Thread(target=getKeyStroke)
myMsgText = []
# Message Structure:
# Type 0: Regular message. Contains "name", "color", "msg", "type", "type"
# Type 1: Join alert. This is sent by a new user, when they join a chat. Contains "name", "color", "type"
# Type 2: Join acknowledgement. This is a response by all the current members of a chat, after the Join alert. Contains "name", "color", "type"
# Type 3: Leave alert. This is sent by a user who is leaving. Contains "name", "color", "type"
while True:
    alreadyPrintedMsgBox =  False
    while threadType.is_alive() == True ^ threadRecv.is_alive() == True:
        pass

    if threadRecv.is_alive() == False:
        print("\033[3A")
        try:
            print(f"{colored(f"[{allMsg[-1]["name"]}]: {allMsg[-1]["msg"]}", colors[allMsg[-1]["color"]])}{" "*42}")
        
        except:
            pass
        if alreadyPrintedMsgBox == False:
            print(f"╔═{"═"*(len("".join(myMsgText))+len(username)+3)}═╗ {" "*42}")
            print(f"║{colored(f"[{username}]: {"".join(myMsgText)}", colors[selected_color])} ║{" "*42}")
            print(f"╚═{"═"*(len("".join(myMsgText))+len(username)+3)}═╝ {" "*42}")
            alreadyPrintedMsgBox = True

        threadRecv = threading.Thread(target=receive)
        threadRecv.start()

    if threadType.is_alive() == False:

        print("\033[3A")

        if alreadyPrintedMsgBox == False:
            print(f"╔═{"═"*(len("".join(myMsgText))+len(username)+3)}═╗ {" "*42}")
            print(f"║{colored(f"[{username}]: {"".join(myMsgText)}", colors[selected_color])} ║{" "*42}")
            print(f"╚═{"═"*(len("".join(myMsgText))+len(username)+3)}═╝ {" "*42}")
            alreadyPrintedMsgBox = True
        threadType = threading.Thread(target=getKeyStroke)
        threadType.start()
    
# Cool box divider: ╔════════╗
#                   ║        ║ Source: https://gist.github.com/jamiew/40c66061b666272462c17f65addb14d5
#                   ╚════════╝
