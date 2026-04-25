# ![LAN-Comms](/logos/logo%20transparent.png)

A CLI app to send messages over LAN!

It's stupidly simple, with
- No encryption
- No direct messages

It's just
- Names
- Ports
- <span style="color:#FF0000">C</span><span style="color:#FF8000">o</span><span style="color:#FFFF00">l</span><span style="color:#00FF00">o</span><span style="color:#0000FF">r</span><span style="color:#8000FF">s</span>

# How it works
- Open the program
- Input the port, or leave empty for default (3535)
  - Ports are the equivalent of chatrooms, choose the same as your friends and you'll be able to talk to them!
- Input your username
- Select your color using the arrow keys

And *voila*, you're in!

# Downloads
Currently, LAN-Comms is only available for **Windows**. Please do not expect that to change.

Just grab the *.exe* file from the [releases page](https://github.com/Aquaticsanti/LAN-Comms/releases/latest), and you're all set!

# Building

To build a *.exe* file, use [PyInstaller](https://pyinstaller.org/)!

First, clone the repo
```` 
git clone https://github.com/Aquaticsanti/LAN-Comms.git
````
Then, _cd_ into the repo, and delete __dist/__ and __LAN-Comms.spec__.

Lastly, run:
````
pyinstaller -F -n "LAN-Comms" -i "logos/logo square.png" LAN-Comms.py
````
And done! You should find _LAN-Comms.exe_ on your dist folder!
# Enjoy!