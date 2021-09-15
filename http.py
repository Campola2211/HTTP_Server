#Nicholas Campola
#Http.py is a server that gets http request packets and based on the request will return error information or the page requested.
#I pledge that I have neither given nor received unauthorized help on this assignment

import datetime
import socket
import sys

#Host of the server
HOST = "10.142.0.2"

#Port to open
PORT = 4040

#Initializing Status
status = 0

try:
    #Choosing a timezone
    now = datetime.datetime.now(datetime.timezone.utc)

    #Get Current Time
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    #Create IPV4 TCP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Set socket to reuse port     
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Bind port and host for socket
    sock.bind((HOST,PORT))

    #Listen for a client
    sock.listen()

    while(True):
        #Gets connection and address of client
        conn, addr = sock.accept()

        #Receving http request
        data = conn.recv(4096)

        #Decoding http request
        block = data.decode()

        #Split request based on newlines
        lines = block.split("\n")

        #Split the first line based on space
        words = lines[0].split()

        #Needs to have three words in array to be properly formatted
        if(len(words) != 3):
            status = 400
            desc = "Bad Request"
            
        #First word needs to be GET
        elif(words[0] != "GET"):
            status = 405
            desc = "Method Not Allowed"
            
        #Seconds word needs to be HTTP/1.1
        elif(words[2] != "HTTP/1.1"):
            status = 505
            desc = "HTTP Version Not Supported"
            
        #Passes previous checks, written in correct format
        else:
            #Means they are requesting home page
            if(words[1] == "/"):
                filename = "index.html"
                
            #Asking for a specific page    
            else:
                #Remove / to search for exact document to send
                filename = words[1].replace("/","")
            
            #Try to find file
            try:
                http = open(filename,"r")
            #File does not exist
            except FileNotFoundError:
                status = 404
                desc = "Not Found"

            #Access Denied to file
            except PermissionError:
                status = 403
                desc = "Forbidden"

            #File can be accessed and is found
            else:
                status = 200
                desc = "OK"

        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        #Status line of request
        statLine = "HTTP/1.1 " + str(status) + " " + desc + "\n"
            
        #Date line of request
        dateLine = "Date: " + date + "\n"
            
        #Initialize content line
        content = ""

        #If webpage can be accessed
        if(status == 200):
            #Copy each line to content
            for line in http:
                content = content + str(line)

        #Else send generic html  page
        else:
            content = "<html><head><title>" + str(status) + " " + desc + "</title></head><body><h1>" + statLine + "</h1><p>Date: " + date + "</p></body></html>"
        #Send all the lines in order for request
        miscLine = "Server: Mine\nContent-Type: text/html; charset=UTF-8\nContent-Length: " + str(len(content.encode())) + "\n"
        conn.sendall(statLine.encode())
        conn.sendall(dateLine.encode())
        conn.sendall(miscLine.encode())
        conn.sendall("\n".encode())
        conn.sendall(content.encode())
except:
    #If anything goes wrong at all
    status = 500
    desc = "Internal Server Error"
    #Initialize timezone and date
    now = datetime.datetime.now(datetime.timezone.utc)
    date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    #Construct and send troubleshooting request
    statLine = "HTTP/1.1 " + str(status) + " " + desc + "\n"
    dateLine = "Date: " + date + "\n"
    content = content = "<html><head><title>" + str(status) + " " + desc + "</title></head><body><h1>" + statLine + "</h1><p>Date: " + date + "</p></body></html>"
    miscLine = "Server: Mine\nContent-Type: text/html; charset=UTF-8\nContent-Length: " + str(len(content.encode())) + "\n"
    conn.sendall(statLine.encode())
    conn.sendall(dateLine.encode())
    conn.sendall(miscLine.encode())
    conn.sendall("\n".encode())
    fileLine = "<html><head><title>" + str(status) + " " + desc + "</title></head><body><h1>" + statLine + "</h1><p>" + dateLine + "</p><p>" + miscLine + "</p></body></html>"
    conn.sendall(fileLine.encode())


