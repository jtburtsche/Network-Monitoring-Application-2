import os
import socket
import struct
import threading
import time
import zlib
import random
import json
import string
import requests
import ntplib
import dns.resolver
import dns.exception
from inputimeout import inputimeout, TimeoutOccurred
from socket import gaierror
from time import ctime
from typing import Tuple, Optional, Any
from colorama import Fore, Style, Back

def create_message(type, data, data2, data3, id):
    message: Dict[str, Any] = {"type": type, "data": data, "data2": data2, "data3": data3, "id": id}
    return json.dumps(message)

def parse_message(message):
    return json.loads(message)

def set_operation(status):
    global operation

    operation = status

def tcp_client():
    global current_data
    global operation
    pause = "0"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = '127.0.0.1'
    server_port = 1251

    try:
        sock.connect((server_address, server_port))

        print(f"connection made: {server_address}{server_port}")
        connection_message = f"Connection Made: {server_address}{server_port}"
        sock.sendall(connection_message.encode())

        response = sock.recv(1024)
        print(f"Received: {response.decode()}")

        while(1):

            print(f"Sending: Confirmation")
            sock.sendall(current_data.encode())

            response = sock.recv(1024)
            print(f"Received: Confirmation")

            sock.sendall(operation.encode())

            try:
                switch = inputimeout(prompt='Enter 0 to pause or the id # to resume/switch: ', timeout=5)

            except TimeoutOccurred:
                switch = operation



            if switch == "0":
                set_operation("Pause")



            if switch != "0":
                set_operation(switch)
                current_operation = switch
                for i in range(len(operations)):
                    if operations[i]["id"] == current_operation:
                        current_data = create_message(operations[i]["type"], operations[i]["data"], operations[i]["data2"], operations[i]["data3"], operations[i]["id"])



            time.sleep(10)


    except:
        print("Hmm there seems to be an error with your echo server/client. You sure you have monitoring_service.py running?")

    finally:
        sock.close()


print(Fore.BLUE + "############################################################################################################" + Style.RESET_ALL)

print("\nWelcome to my Network Monitoring System\n")
print("Please enter one of the following commands for the corresponding information:")
print("0-EXIT, 1-Create Configuration, 2-Load Configurations, 3-Display Results")

print("Type of Operations: PING, HTTP, HTTPS, NTP, DNS, TCP, UDP")
print("Choose an ID of 1-5")

print(Fore.BLUE + "############################################################################################################" + Style.RESET_ALL)
global operations
operations = []
global current_data

while(1):
    val = input("\nEnter command: ")

    if val == '0':
        print("See you later")
        break

    if val == '1':
        type = input("Enter type of operation: ")
        data = input("Enter Data: ")

        if type == "TCP":
            data2 = input("Enter data2: ")
            data3 = "None"

        elif type == "UDP":
            data2 = input("Enter data2: ")
            data3 = "None"

        elif type == "DNS":
            data2 = input("Enter data2: ")
            data3 = input("Enter data3: ")

        else:
            data2 = "None"
            data3 = "None"

        id = input("enter ID: ")

        new_operation = create_message(type, data, data2, data3, id)
        operations.append(parse_message(new_operation))
        #set_operation("Start")
        #tcp_client(new_operation)


    if val == '2':
        for i in range(len(operations)):
            print(f"{operations[i]['id']}: {operations[i]}")


    if val =='3':
        print("Press ctrl + c to exit")
        current_operation = input("Enter the id that you want to run: ")
        set_operation(current_operation)
        for i in range(len(operations)):
            if operations[i]["id"] == current_operation:
                current_data = create_message(operations[i]["type"], operations[i]["data"], operations[i]["data2"], operations[i]["data3"], operations[i]["id"])
                print(current_data)
        tcp_client()

        exit(0)

