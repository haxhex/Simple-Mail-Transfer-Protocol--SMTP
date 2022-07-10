
import os
import re
import sys
from socket import *

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

IP = "127.0.0.1"
PORT = 8080
DISCONNECT_MSG= "QUIT"  

def main():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((IP, PORT))
    print(style.BLUE + f">>> [CONNECTED] Client connected to server at {IP}:{PORT}")
    # check for handshake
    recv = clientSocket.recv(1024)
    print(style.RED + ">>> " + recv.decode("utf-8"))
    if recv[:3] != b'220':
        print(style.BLue + '>>> Unable to connect to server. Please try again later.')
        clientSocket.close()
        sys.exit()
        
    
    # Send HELLO command and print server response
    helloCommand = 'HELLO toby.flenderson'
    print(style.BLUE + ">>> " + helloCommand)
    clientSocket.send(helloCommand.encode())
    recv1 = clientSocket.recv(1024)
    print(style.RED + ">>> " + recv1.decode("utf-8"))
    if recv1[:3] != b'250':
        print(style.BLue + '>>> Unable to connect to server. Please try again later.')
        clientSocket.close()
        sys.exit()
    path = "com/yahoo/toby.flenderson/Inbox"
    clientSocket.send(path.encode())
    
    x = 0   
    connected = True
    while connected: 
        # input Sender email
        while True:
            inputFrom = input(style.BLUE + '>>> From: ')
            mailFrom = 'MAIL FROM: <' + inputFrom + '>'
            clientSocket.send(mailFrom.encode())
            okFrom = clientSocket.recv(1024)
            print(style.RED + ">>> " + okFrom.decode("utf-8"))
            if okFrom[:3] != b"250":
                print (style.BLUE + '>>> Please enter a valid email address.')
                continue
            else: break
            
    
        # input email recipients separated by comma and space
        while True:
            if x == 1:
                break
            to = input(style.BLUE + '>>> To: ')
            toList = to.split(", ")
            
            for tos in toList: 
                rcp = 'RCPT TO: <' + tos + '>'
                clientSocket.send(rcp.encode())
                okTo = clientSocket.recv(1024)
                print(style.RED + ">>> " + okTo.decode("utf-8"))
                # helper function to check if valid email
                if okTo[:3] != b"250":
                    # print (style.BLUE + '>>> One or more email addresses are invalid. Please re-enter')
                    x = 0
                else: 
                    x = 1                 
                if x == 0:
                    break
                        
        clientSocket.send('DATA'.encode())
        okData = clientSocket.recv(1024)
        print(style.BLUE + ">>> DATA")
        print(style.RED + ">>> " + okData.decode("utf-8"))
        if okData[:3] != b"354":
            print (style.BLUE + '>>> There is an error.')
            
        writeFrom = ('From: ' + inputFrom)
        clientSocket.send(writeFrom.encode())
        clientSocket.recv(1024)
        
        writeTo = ('To: ' + to)
        clientSocket.send(writeTo.encode())
        clientSocket.recv(1024)
            
        readSubject = input(style.BLUE + '>>> Subject: ')
        sub = 'Subject: ' + readSubject + '\n'
        clientSocket.send(sub.encode())
        clientSocket.recv(1024)
            
        sys.stdout.write(style.BLUE + '>>> Message: ')
            
        # read email msg until "."
        while True:
            readData = input()
            if readData == '':
                readData = '\r'
            clientSocket.sendall(readData.encode())
            okEnd = clientSocket.recv(1024)
            if okEnd[:3] == b'250':
                print(style.RED + ">>> " + okEnd.decode("utf-8"))
                sendMsg = input(style.BLUE + ">>> ")
                if sendMsg == "SEND":
                    clientSocket.send(sendMsg.encode())
                    okSend = clientSocket.recv(1024)
                    print(style.RED + ">>> " + okSend.decode("utf-8"))
                    if okSend[:3] != b'250':
                        print("There was a problem in sending.")
                clientSocket.send('QUIT'.encode())
                quitMsg = clientSocket.recv(1024)
                # print(style.RED + ">>> " + quitMsg.decode("utf-8"))
                if quitMsg[:3] != b'221':
                    print (style.BLUE + '>>> There was an error. Quitting.')
                    sys.exit()
                else:
                    msg = input(style.BLUE + ">>> ")
                    clientSocket.send(msg.encode("utf-8"))
                    if msg == DISCONNECT_MSG:
                        connected = False
                        print(style.RED + ">>> " + quitMsg.decode("utf-8"))    
                        clientSocket.close()
                    # exit()
                # else:
                    rep1 = True
                    while rep1:
                        com = input(style.WHITE + "> ")
                        if com == "SMTP()":
                            rep1 = False
                            main()
                            break
                        
            else:
                continue
if __name__ == '__main__':
    rep = True
    while rep:
        com = input(style.WHITE + "> ")
        if com == "SMTP()":
            rep = False
            main()
            break