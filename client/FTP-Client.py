import socket
import os  #The OS module in Python provides functions for creating and removing a directory (folder), fetching its contents, changing and identifying the current directory,
import glob #to return all file paths that match a specific pattern
from time import sleep
from math import ceil
from getpass import getpass #provides a platform-independent way to enter a password in a command-line program, 

def main():
    PORT = 65432 #enter the listening port
    HOST = '' #enter the Host computer name (this is if it is connected via ethernet)
    s = socket.socket()
    s.connect((HOST, PORT))
    loginAttempts = 0
    while loginAttempts < 3:
        message = s.recv(2048).decode()
        print(message)
        
        username = input("Enter your username: ")
        s.sendall(username.encode())
        
        password = getpass(prompt = "Enter your password: ", stream = None)
        s.send(password.encode())
    
        answer = s.recv(2048).decode()
        
        if answer == 'correct':
            print("Successful login")
            while True:
                string = input("\nEnter commands and file ")
                s.sendall(string.encode())

                if string == 'dir':   
                    x = s.recv(2048).decode()
                    print (x)

                elif string == 'ls':
                    x = s.recv(2048).decode()
                    print(x)

                elif string == 'pwd':
                    x = s.recv(2048).decode()
                    print(x)

                elif string[:4] == 'get ':
                    response = s.recv(2048).decode()
                    print(response + ' bytes')
                    if(response[:4] == 'file'):
                        filename = string[4:]
                        filesize = int(response[27:])
                        packetAmmount = ceil(filesize/2048)
                        if (os.path.isfile('new_' + filename)):
                            x = 1
                            while(os.path.isfile('new_' + str(x) + filename )):
                                x += 1
                            f = open('new_' + str(x) + filename, 'wb')

                        else:
                            f = open("new_" + filename, 'wb')
                        
                        for x in range (0, packetAmmount):
                            data = s.recv(2048)
                            f.write(data)
                        
                        f.close()
                        print("Download is complete")
                    else:
                        print("File does not exist...")
                
                elif string[:4] == 'put ':
                    filename = string[4:]
                    if os.path.isfile(filename):
                        filesize = int(os.path.getsize(filename))
                        s.sendall(('true' + str(filesize)).encode())
                        with open(filename, 'rb') as f:
                            packetAmmount = ceil(filesize/2048)
                            for x in range(0, packetAmmount):
                                bytesToSend = f.read(2048)
                                s.send(bytesToSend)
                        print("File sent!")
                    else:
                        s.sendall('false'.encode())
                        print("File does not exist...")
                
                elif string [:9] == 'compress ':
                    x = s.recv(2048).decode()
                    print(x)

                elif string == 'quit':
                    loginAttempts = 4
                    break

        elif answer == 'disconnect':
            break
        loginAttempts += 1
    print("You have been disconnected...")

main()
#https://www.geeksforgeeks.org/getpass-and-getuser-in-python-password-without-echo/

#  (')>  # 
