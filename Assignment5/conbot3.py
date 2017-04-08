
import socket
import time
import irc
import random
import string
import sys
import threading
import select

#HOST = ""              # the Twitch IRC server
#PORT = 1234                         # always use port 6667!
NICK = "conbot"            # your Twitch username, lowercase
PASS = "pwiscpsc1234" # your Twitch OAuth token
#CHAN = "testg"                   # the channel you want to join
comList = ["status","attack","move","quit","shutdown"]

errorList = [ "402","403","431","432",'433',"436","437","461","465","471","473","474","475"]

class inputThread(threading.Thread):
    def __init__(self,cBot,phrase):
        self.commandList = ["status","attack","move","quit","shutdown"]
        self.commandList.append(phrase)
        self.command = "initial"
        self.cBot = cBot
        threading.Thread.__init__ (self)
        
        
    def run(self):  
        print(self.commandList)     
        while True:           
            userCommand = ''
            try:            
                userCommand = input("Please enter a valid command:")
                print(userCommand)
                print(self.commandList)
                if(userCommand not in self.commandList):
                    raise ValueError
                else:
                    self.cBot.command = userCommand.split()
            except ValueError:
                self.run()
            time.sleep(5)
        
class conBot(threading.Thread):
    def __init__(self, nick, host, port, chan, phrase):
        self.chan = chan 
        self.host = host
        self.port = port
        self.NICK = nick
        self.activationPhrase = phrase
        self.command = ["initial Command"]
        self.inThread = threading.Thread(target = inputThread)
        self.comList = ["status","attack","move","quit","shutdown"]
        self.botList = []
        threading.Thread.__init__ ( self ) 
        
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.s.connect((self.host, self.port)) 
        
        except Exception as e:
            #time.sleep(5)
            self.s.connect((self.host,self.port))           
        
        self.counter = 0
        
        self.controller = ""
        self.gameOn = False
        #self.inputThread.run()
        self.connection()
        
    def createNick(self, nick):
        self.NICK = nick + ''.join(random.choice(string.ascii_lowercase) for i in range(5))       
        
        
    def connectIRC(self, s, nick, CHAN):         
        s.send("USER {} {} {} {}:Test\n".format(nick,nick,nick,nick).encode("utf-8"))
        s.send("NICK {}\r\n".format(nick).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
        self.NICK = nick
        
    def moveIRC(self,s,CHAN):
        s.send("USER {} {} {} {}:Test\n".format(self.NICK,self.NICK,self.NICK,self.NICK).encode("utf-8"))
        s.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
    
    def attack(self, h, p):
        sock = socket.socket()
        sock.connect((h,int(p)))
        sock.send("{} {}\r\n".format(self.counter,self.NICK).encode("utf-8"))
        sock.close()
        self.counter = self.counter + 1
    
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
    
    def parsemsg(self,s):
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
        
    def inputTest(self): 
        #while True:        
        time.sleep(5)
        userCommand = ''
        try:            
            userCommand = input("Please enter a valid command:")
            if(userCommand not in self.comList):
                raise ValueError
            else:
                lock = threading.Lock()
                with lock:
                    self.command = userCommand.split()
        except ValueError:
                self.run(cBot)
                
    def processCommand(self):
        print("command = ")
        print(self.command[0])
        if(self.command[0] == self.activationPhrase):
            self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, self.command[0]).encode("utf-8"))
            #self.command = grabInput(self.comList)
            #self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command[0]).encode("utf-8"))
        elif(self.command[0] == "status") :                    
            self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command[0]).encode("utf-8"))    
        elif(self.command[0] == "attack"):
            attackHost = self.command[1]
            attackPort = self.command[2]
            #self.command = grabInput(self.comList)
            #:simdevs!~simdevs@136.159.160.155 PRIVMSG #simdevs :!attack localhost 7788
            self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command).encode("utf-8"))

    def connection(self):
    
        self.connectIRC(self.s,self.NICK,self.chan)        
        self.comList.append(self.activationPhrase)
        getInput = True
        print("Connected to IRC...")
        count =0  
        socket_list = [sys.stdin, self.s]
        isconnected = False
        try:
            while getInput:
                read_socks, write_socks, error_socks = select.select(socket_list,[],[])
                for sock in read_socks:
                    if(sock == self.s):
                        response = self.s.recv(1024).decode("utf-8")
                        (prefix, command, args) = self.parsemsg(response)            
                        print((prefix,command,args))
                        if(command == '353'):
                            print("line 170")
                            #threading.Thread(target = prompt).start()
                            isconnected = True
                            threading.Thread(target = prompt).start()                                
                        elif command == "PRIVMSG":
                            test = args[1].split() 
                            print("prefix: " + prefix)
                            if(isconnected):
                                threading.Thread(target = prompt).start()
                                #threading.Thread(target = prompt).start()
                        elif command == "PING":
                            self.s.send("PONG {}: :\r\n".format(prefix).encode("utf-8"))
                            #if(isconnected):
                            #    threading.Thread(target = prompt).start()                                        
                        elif command == '433':
                            self.createNick(NICK)
                            self.connectIRC(self.s,self.NICK, self.chan)
                        
                    elif (sock == sys.stdin):
                        self.command = sys.stdin.readline().split()
                        print("command = ")
                        print(self.command)
                        if(self.command[0] == self.activationPhrase):
                            self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, self.command[0]).encode("utf-8"))
                        elif(self.command[0] == "status") :                    
                            self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command[0]).encode("utf-8"))
                        elif(self.command[0] == "attack") :                    
                            self.s.send("PRIVMSG {} : {} {} {}\r\n".format(self.chan, "!"+self.command[0],self.command[1],self.command[2]).encode("utf-8"))
                        threading.Thread(target = prompt).start()                                  
                
                    
        
        except Exception as e:
            print("Exception: ")
            print(e)
            print("Reconnecting in 5 seconds ...")
            time.sleep(5)
            self.connection()
        
def prompt():    
    time.sleep(3)
    print("Enter valid command: ")
    #sys.stdout.write("Enter valid command:")
    #sys.stdout.flush()
    
    
def main():
        
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    PHRASE = sys.argv[4]
    
    cBot = conBot(NICK,HOST,PORT,CHAN,PHRASE)
    cBot.start()  
    
  
    
    
    
    
    
    
            
            

if __name__ == '__main__':
    main()


        