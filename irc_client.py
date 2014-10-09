import sys
import socket
import string
import select
import tty,termios

user_input = ""
s = socket.socket()

def heardEnter():
    global user_input
    user_input = ""
    i, o, e = select.select([sys.stdin], [], [], 0)
    for s in i:
        if s == sys.stdin:
            user_input = sys.stdin.readline()
            return True
        return False
            
def socketReady():
    global s

    i, o, e = select.select([s], [], [], 0)

    for x in i:
        if x == s:
            return True
        return False

def main():                                                                                                                                                                                          
                                                                                                                                                                                                     
        HOST="irc.freenode.net"                                                                                                                                                                      
        PORT=6667
        PASS="password"
        NICK="MauBot"
        IDENT="maubot"
        REALNAME="MauritsBot"
        readbuffer=""
        writebuffer=""
        global user_input
        global s

        s.connect((HOST, PORT))
        s.send("NICK %s\r\n" % NICK)
        s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))

        while (1):
                # poll stdin
                if heardEnter():
                    writebuffer = "PRIVMSG #haskell :" + user_input + "\r\n"
                    s.send(writebuffer)
                
                #poll socket
                if socketReady():
                    readbuffer=readbuffer+s.recv(1024)
                    temp=string.split(readbuffer, "\n")
                    readbuffer=temp.pop( )

                    for line in temp:
                        print line
                        if ":MauBot MODE MauBot :+i" in line:
                                s.send("JOIN #haskell\r\n")
                        line=string.rstrip(line)
                        line=string.split(line)

                        if(line[0]=="PING"):
                                s.send("PONG %s\r\n" % line[1])


if __name__=='__main__':
    main()
