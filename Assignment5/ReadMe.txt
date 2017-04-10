Name:   Mike Simister       StudentID: 10095107
        Shivangi Gokani     StudentID: 10101523
      
Tutorial Section: T02, T01

The programs bot.py and conbot.py are a bot and controllerBot respectively.

To run the bot,conbot program:

(1) From the directory containing the bot.py file:

	(1a)From cmd line type: python3 bot.py <hostname> <port> <channel> <secret-phrase>
	(1b)From cmd line type: python3 conbot.py <hostname> <port> <channel> <secret-phrase>
	
	
(2) After successfully running conbot, you should be able to exectute the following commands

        Command: status
        This command will make the controller issue a command that will result in the bots identifying themselves to
        the controller. The controller will then print out the list of bots (their nicks), and their total number.
        
        Command: attack <host-name> <port>
        This command will take two arguments: a host-name and a port number. The controller will then instruct the
        bots to attack the given host-name at the given port number. Every bot will then connect to the given host/port
        and send a message containing two entries: a counter and the nick of the bot. On the next attack the counter
        should be increased by 1. After the attack is complete, the bots must send diagnostic messages back to the
        controller about the attack (eg. success/failure), and the controller will then display them to the user on standard
        output. The controller will also display the total number of successful and unsuccessful attacks.
        
        Command: move <host-name> <port> <channel>
        This command will instruct all bots to disconnect from the current IRC server and connect to a new IRC server
        as specified through the arguments. The controller should display how many bots were moved as a result of this
        command.
        
        Command: quit
        The controller will disconnect from the IRC and then terminate. The bots are unaffected.
        
        Command: shutdown
        This command will shut down the botnet. All bots should terminate. The controller will remain running, and
        connected to the IRC server. The controller


(3)Known bugs:

	(4a)Occasionally when connecting the conbot.py program the following exception:
    
        Connecting to IRC...
        Exception: 
        not enough values to unpack (expected 2, got 1)
        
        In all observed cases the program continued, reconnected and functioned properly after the 2nd attempt.
        That is it automatically re-connected there is no need to restart the program. However that is also an 
        option.

	

