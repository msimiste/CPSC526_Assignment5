import socket
import time
import random
import string
import sys

#HOST = ""              # the Twitch IRC server
#PORT = 1234                         # always use port 6667!
NICK = "testBot"            # your Twitch username, lowercase
PASS = "pwiscpsc1234" # your Twitch OAuth token
#CHAN = "testg"                   # the channel you want to join

errorList = [ "402","403","431","432",'433',"436","437","461","465","471","473","474","475"]

class clientBot(object):
    def __init__(self, nick, host, port, chan):
        self.chan = chan 
        self.host = host
        self.port = port
        self.NICK = nick
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.s.connect((self.host, self.port)) 
        
        except Exception as e:
            time.sleep(5)
            self.s.connect((self.host,self.port))           
        
        self.counter = 0
        self.activationPhrase = ""
        self.controller = ""
        self.gameOn = False
        
    def createNick(self, nick):
        self.NICK = nick + ''.join(random.choice(string.ascii_lowercase) for i in range(5))       
        
        
    def connectIRC(self, s, nick, CHAN):         
        s.send("USER {} {} {} {}:Test\n".format(nick,nick,nick,nick).encode("utf-8"))
        s.send("NICK {}\r\n".format(nick).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
        self.NICK = nick
        
    def moveIRC(self,s,CHAN):
        try:            
            s.send("USER {} {} {} {}:Test\n".format(self.NICK,self.NICK,self.NICK,self.NICK).encode("utf-8"))
            s.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
            s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
            time.sleep(5)
            s.send("PRIVMSG {} : {}\r\n".format(self.controller,"!MOVE! move successful").encode("utf-8"))
        except Exception as e:
            s.send("PRIVMSG {} : {}\r\n".format(self.controller,"!MOVE! move unsuccessful").encode("utf-8"))
            
    def attack(self, h, p):
        try:
            sock = socket.socket()
            sock.connect((h,int(p)))
            sock.send("{} {}\r\n".format(self.counter,self.NICK).encode("utf-8"))
            sock.close()
            self.counter = self.counter + 1
            self.s.send("PRIVMSG {} : !ATTACK! attack was successfull\r\n".format(self.controller).encode("utf-8"))
        except Exception as e:
            self.s.send("PRIVMSG {} : !ATTACK! attack was unsucccessful\r\n".format(self.controller).encode("utf-8"))
            
            
    def move(self, host, port, chan):
        self.host = host
        self.port = int(port)
        self.chan = chan
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print("line 52")
        print(self.host)
        print(self.port)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((self.host,self.port))
        self.moveIRC(self.s,self.chan)
        
    def setController(self, prefix):
        arguments = prefix.split("!~")
        self.controller = arguments[0]
            
    def parseController(self,prefix):
        arguments = prefix.split("!~")
        return arguments[0]

def main():    
    connection()
    
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
    
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    PHRASE = sys.argv[4]
       
    cBot = clientBot(NICK,HOST,PORT,CHAN)
    cBot.createNick(cBot.NICK)
    cBot.connectIRC(cBot.s,cBot.NICK,cBot.chan)
    cBot.activationPhrase = PHRASE
   
    print("Connected to IRC...")
    
    try:
        while True:
            response = cBot.s.recv(1024).decode("utf-8")
            print("response: ")
            print(response)
            (prefix, command, args)= parsemsg(response)            
            for p in args:
                if(":Nickname is already in use" in p):
                    cBot.connectIRC(cBot.s,cBot.NICK,cBot.chan)                
                print ("arg["+p.strip()+"]")
            print((prefix,command,args))
            if command == "PRIVMSG":
                    test = args[1].split()
                    if args[0] == cBot.chan and args[1].split()[0] == cBot.activationPhrase:
                        cBot.setController(prefix)
                        cBot.gameOn = True
                        print("GameON")
                        print(cBot.controller)
                    if args[0] == cBot.chan and args[1].split()[0] == "!status":
                        if(cBot.gameOn and (cBot.parseController(prefix) == cBot.controller)):
                            cBot.s.send("PRIVMSG {} : {} {}\r\n".format(cBot.controller,"!STATUS!", cBot.NICK).encode("utf-8"))
                    if args[0] == cBot.chan and args[1].split()[0] == "!attack":
                        if(cBot.gameOn and (cBot.parseController(prefix) == cBot.controller)):
                            attackhost = args[1].split()[1].strip()
                            attackPort = args[1].split()[2].strip()
                            cBot.attack(attackhost,attackPort)                    
                    if args[0] == cBot.chan and args[1].split()[0] == "!move":
                        if(cBot.gameOn and (cBot.parseController(prefix) == cBot.controller)):
                            cBot.s.send("QUIT : pz out\r\n".encode("utf-8"))
                            newHost = args[1].split()[1].strip()
                            newPort = args[1].split()[2].strip()
                            newChan = args[1].split()[3].strip()
                            print("line 148: " + newChan)
                            cBot.move(newHost,newPort,newChan)
            elif command == "KICK" :
                cBot.connectIRC(cBot.s,cBot.NICK, cBot.chan)                              
            elif command == "PING":
                cBot.s.send("PONG {}: :\r\n".format(prefix).encode("utf-8"))            
                
            elif command =='433':
                print("line 161")
                cBot.createNick(NICK)
                cBot.connectIRC(cBot.s,cBot.NICK, cBot.chan)        
    except Exception as e:
        print("Reconnecting in 5 seconds ...")
        time.sleep(5)
        connection()         

if __name__ == '__main__':
    main()


        
