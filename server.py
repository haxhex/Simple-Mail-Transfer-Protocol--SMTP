import os.path
import re
from socket import *
import sys
import threading
import datetime

global boolean
boolean = True
Boolean = True
save_path = 'email/'
DISCONNECT_MSG= "QUIT"
IP = "127.0.0.1"
PORT = 8080

def is_valid(emailAddr):
    username, rem = emailAddr.split("@")
    dom1, dom2 = rem.split(".")
    is_valid = False
    if dom2 == "com":
        if dom1 == "gmail":
            is_valid = os.path.exists("com/gmail/" + username)
        elif dom1 == "yahoo":
            is_valid = os.path.exists("com/yahoo/" + username)
    return is_valid      

def handle_client(connectionSocket, addr):
    # receive HELLO from client
    while True:
        try:
            hello = connectionSocket.recv(1024)
            print(hello)
            name = hello.decode("utf-8").split(" ")[1]
            if hello[:5] == b'HELLO':
                helmsg = "250 Hello " + name + '. Pleased to meet you.'
                connectionSocket.send(bytes(helmsg, "utf-8"))
                save_path = connectionSocket.recv(1024).decode('utf-8')
                break
        except:
            print('HELLO error. Try again.')
            sys.exit()
    def driver():
        boolean = True    
        while boolean:         
            while boolean:
                # receive mail command
                command = connectionSocket.recv(1024)
                # check if command input is out of order
                _check1 = re.match(r'RCPT(\s+|$)TO:', command.decode("utf-8"))
                _check2 = re.match(r'DATA', command.decode("utf-8"))
                from_email = command.decode("utf-8").split("<")[1].replace(">", "")

                if _check1:
                    connectionSocket.send(b'503 Bad sequence of commands')
                    continue
                if _check2:
                    connectionSocket.send(b'503 Bad sequence of commands')
                    continue
                elif not is_valid(from_email):
                    connectionSocket.send(b"Error, Entered email address does not exist.")
                    continue
                else:
                    From = command.replace(b"MAIL FROM", b"From")
                    print(From)
                    connectionSocket.send(bytes('250 ' + from_email + " ... Sender OK" , "utf-8"))

                _bool = True
                to_list = []
                rcpt_list = []

                while boolean:

                    # receive receipt
                    receipt = connectionSocket.recv(1024)
                    # checks for out of order commands 
                    check = re.match(r'DATA', receipt.decode("utf-8"))
          
                    if receipt[:7] == 'Subject':
                        receipt = 'DATA'
                        _bool = False
                        continue
                    if _bool is False:
                        if check:
                            break

                    elif not is_valid(receipt.decode("utf-8").split("<")[1].replace(">", "")):
                        connectionSocket.send(b"Error, Entered email address does not exist.")
                        continue      
                    else:
                        _bool = False
                        name_of_file = datetime.datetime.now().strftime('%m-%d-%Y %H-%M-%S')
                        to = receipt.replace(b"RCPT TO: ", b"")
                        rcpt_list.append(to)
                        toMail = receipt.decode("utf-8").split("<")[1].replace(">", "")
                        uname = toMail.split("@")[0];
                        domi = toMail.split("@")[1];
                        domi1, domi2 = domi.split(".")
                        print(domi2 + "/" + domi1 + "/" + uname + "/"+"Inbox")
                        save_path = domi2 + "/" + domi1 + "/" + uname + "/"+"Inbox"
                        if not os.path.exists(save_path):
                            os.makedirs(save_path)
                        save_name = os.path.join(save_path, name_of_file)
                        file1 = open(save_name, "a")
                        to_list.append(file1)
                        connectionSocket.send(bytes('250 ' + toMail + " ... Reciptient OK", "utf-8"))
                        continue
                # write From and To in files
                while boolean:
                    if not check:
                        # receive DATA cmd 
                        datacmd = connectionSocket.recv(1024)
                        print(datacmd)
                        check = re.match(r'DATA', datacmd.decode("utf-8"))

                    if not check:
                        connectionSocket.send(b'500 Syntax error: command unrecognized')
                        continue
                    else:
                        connectionSocket.send(b"354 Enter mail, end with '.' on a line by itself")
                    
                    while boolean:
                        # receive msg until QUIT      
                        data = connectionSocket.recv(1024)
                        print(data)
                        if data.decode("utf-8") == '.':
                            connectionSocket.send(b'250 Message accepted for delivery')
                            boolean = False
                        
                            for files in to_list:
                                file1 = files
                                if data.decode("utf-8") != ".":
                                    file1.write(data.decode("utf-8") + "\n")
                                file1.close()
                            sendMsg = connectionSocket.recv(1024)
                            if sendMsg.decode("utf-8") == "SEND":
                                connectionSocket.send(b'250, Email sent.')

                            quitCmd = connectionSocket.recv(1024)
                            print(quitCmd)
                            if re.match(r'QUIT', quitCmd.decode("utf-8")):
                                connectionSocket.send(b'221 Bye')
                                msg = connectionSocket.recv(1024).decode("utf-8")
                                if msg == DISCONNECT_MSG:
                                    boolean = False
                                    break
                                else:
                                    print("Contuinue....")
                                    driver()
                        else:
                            connectionSocket.send(data)
                            for files in to_list:
                                file1 = files
                                file1.write(data.decode("utf-8") + "\n")
                                continue
    driver()
    connectionSocket.close()



def main():
    try:
        print("[STARTING] Server is starting...")
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((IP, PORT))
        serverSocket.listen()
        print(f"[STARTING] Server is listening on {IP} : {PORT}")
    except:
        print('Socket connection error. Try again.')
        sys.exit()
        
    print ("Connection Establish")   

    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            connectionSocket.send(bytes("220 Connection accepted from " + gethostname(), "utf-8"))
            thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except:
            print('Socket connection error.')
            sys.exit()
        
    
if __name__ == '__main__':
    main()

