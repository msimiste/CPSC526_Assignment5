import socket
import time
import irc
import random
import string
import sys

HOST = ""              # the Twitch IRC server
PORT = 1234                         # always use port 6667!
NICK = "testBOt"            # your Twitch username, lowercase
PASS = "pwiscpsc1234" # your Twitch OAuth token
#CHAN = "testg"                   # the channel you want to join


def main():
    
    connection()
    
    
def connectIRC(s, nick, CHAN):    
    nick = nick + ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    s.send("USER {} {} {} {}:Test\n".format(nick,nick,nick,nick).encode("utf-8"))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(nick).encode("utf-8"))
    s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

def parsemsg(s):
    """Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if not s:
       raise IRCBadMessage("Empty line.")
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args

def connection():
    # network functions go here
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    PHRASE = sys.argv[4]
    
    print("Line 50: " + CHAN)
    
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("USER {} {} {} {}:Test\n".format(NICK,NICK,NICK,NICK).encode("utf-8"))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

    print("Connected to IRC...")

    while True:
        response = s.recv(1024).decode("utf-8")
        (prefix, command, args)= parsemsg(response)
       
        for p in args: print ("arg["+p.strip()+"]") 
        if command == "PRIVMSG":
                if args[0] == CHAN and args[1].strip() == "!saysomething":
                    s.send("PRIVMSG {} :Im a new message\r\n".format(CHAN).encode("utf-8"))
                    print("PRIVMSG {} :Im a new message\r\n".format(CHAN).encode("utf-8"))
                if args[0] == CHAN and args[1].strip() == "!quit":
                    s.send("PRIVMSG {} :cpsc526bot out!\r\n".format(CHAN).encode("utf-8"))
                    print(NICK + " out!")
                    break
        elif command == "PING":
            s.send("PONG {}: :\r\n".format(prefix).encode("utf-8"))
            print("Line 48: " + "PONG :"+prefix+"\r\n") 
            
        elif command == "433":
            print("Line 61 command: " + str(command))
            connectIRC(s, NICK, CHAN)
        print("Line 62: " + response)
    s.close()
    #sleep(1 / cfg.RATE)

if __name__ == '__main__':
    main()


        
