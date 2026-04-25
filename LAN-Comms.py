from termcolor import colored
import threading
import socket
import time
import os
from readchar import readkey, key
import pickle # im sorry im actually using pickles in my program LMAOO
import win32con, win32api

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
    myMsg = {"name": username, "color": selected_color, "msg": "".join(myMsgText), "type": 0}
    sock.sendto(pickle.dumps(myMsg), ("255.255.255.255", port))
    myMsgText = []

def sendLeave():
    sock.sendto(pickle.dumps({"name": username, "color": selected_color, "type": 3}), ("255.255.255.255", port))

# Source - https://stackoverflow.com/a/74969378
# Posted by nat-echlin
# Retrieved 2026-04-25, License - CC BY-SA 4.0

def exit_handler(event):
    if event in [win32con.CTRL_C_EVENT, win32con.CTRL_LOGOFF_EVENT,
                         win32con.CTRL_BREAK_EVENT, win32con.CTRL_SHUTDOWN_EVENT,
                         win32con.CTRL_CLOSE_EVENT]:
        sendLeave()

win32api.SetConsoleCtrlHandler(exit_handler, 1)


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
    elif type(k) == str:
        myMsgText.append(k)
# print(colored(f"[{message["name"]}]: {message["msg"]}", colors[message["color"]]))
threadSend = threading.Thread(target=send)
threadRecv = threading.Thread(target=receive)
threadType = threading.Thread(target=getKeyStroke)
myMsgText = []
ActiveUsers = []
sock.sendto(pickle.dumps({"name": username, "color": selected_color, "type": 1}), ("255.255.255.255", port))

# Message Structure:
# Type 0: Regular message. Contains "name", "color", "msg", "type", "type"
# Type 1: Join alert. This is sent by a new user, when they join a chat. Contains "name", "color", "type"
# Type 2: Join acknowledgement. This is a response by all the current members of a chat, after the Join alert. Contains "name", "color", "type"
# Type 3: Leave alert. This is sent by a user who is leaving. Contains "name", "color", "type"
while True:
    print("\033[5A")
    alreadyPrintedMsgBox =  False
    while (threadType.is_alive() == True) and (threadRecv.is_alive() == True):
        pass
    if threadRecv.is_alive() == False:
        if len(allMsg) == 0:
            pass
        else:
            if allMsg[-1]["type"] == 0: # Someone sent a regular message
                print(f"{colored(f"[{allMsg[-1]["name"]}]: {allMsg[-1]["msg"]}", colors[allMsg[-1]["color"]])}{" "*(42+len(f"Connected to port {port}"))}")
            elif allMsg[-1]["type"] == 1: # Someone joined
                if {"name": allMsg[-1]["name"], "color": allMsg[-1]["color"]} in ActiveUsers:
                    pass
                else:
                    ActiveUsers.append({"name": allMsg[-1]["name"], "color": allMsg[-1]["color"]})
                    print(f"{colored(f"{allMsg[-1]["name"]} just joined!", colors[allMsg[-1]["color"]])}{" "*42}")
                    sock.sendto(pickle.dumps({"name": username, "color": selected_color, "type": 2}), ("255.255.255.255", port))
            elif allMsg[-1]["type"] == 2: # Join acknowledgement
                if {"name": allMsg[-1]["name"], "color": allMsg[-1]["color"]} in ActiveUsers:
                    pass
                else:
                    ActiveUsers.append({"name": allMsg[-1]["name"], "color": allMsg[-1]["color"]})
            elif allMsg[-1]["type"] == 3:
                ActiveUsers.pop(ActiveUsers.index({"name": allMsg[-1]["name"], "color": allMsg[-1]["color"]}))
        if alreadyPrintedMsgBox == False:
            print(f"╔═{"═"*(len("".join(myMsgText))+len(username)+3)}═╗ {" "*42}")
            print(f"║{colored(f"[{username}]: {"".join(myMsgText)}", colors[selected_color])} ║{" "*42}")
            print(f"╚═{"═"*(len("".join(myMsgText))+len(username)+3)}═╝ {" "*42}")
            for user in ActiveUsers:
                print(colored(f"■ {user["name"]}", colors[user["color"]]), end=" - ")
            print(colored(f"Connected to port {port}", "dark_grey"))
            alreadyPrintedMsgBox = True
        threadRecv = threading.Thread(target=receive)
        threadRecv.start()
    if threadType.is_alive() == False:
        if alreadyPrintedMsgBox == False:
            print(f"╔═{"═"*(len("".join(myMsgText))+len(username)+3)}═╗ {" "*42}")
            print(f"║{colored(f"[{username}]: {"".join(myMsgText)}", colors[selected_color])} ║{" "*42}")
            print(f"╚═{"═"*(len("".join(myMsgText))+len(username)+3)}═╝ {" "*42}")
            for user in ActiveUsers:
                print(colored(f"■ {user["name"]}", colors[user["color"]]), end=" - ")
            print(colored(f"Connected to port {port}", "dark_grey"), " "*(42+len(f"Connected to port {port}")))
            alreadyPrintedMsgBox = True
        threadType = threading.Thread(target=getKeyStroke)
        threadType.start()
    
# Cool box divider: ╔════════╗
#                   ║        ║ Source: https://gist.github.com/jamiew/40c66061b666272462c17f65addb14d5
#                   ╚════════╝
