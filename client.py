import socket
import threading
import json

vl = open('voters.json')
p = open('parties.json')

voterslist = json.load(vl)
partylist = json.load(p)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.42.18', 6009))
def PrintParty():
    for party in partylist:
        print("[{}] --> {} : {} ".format(party['code'],party['party'],party['candidate']))

def receive():
    while True:
        try:
            message = client.recv(2048).decode('ascii')
            if message == 'Please Enter Name ? : ':
                print(message)
                name = input()
                client.send(name.encode('ascii'))

            elif message =='Please Enter Voter ID ? : ':
                print(message)
                voterid = input()
                client.send(voterid.encode('ascii'))

            elif message =='Enter your choice : ':
                print(message)
                PrintParty()
                vote = input()
                client.send(vote.encode('ascii'))

            elif '$$$ Thanks for voting $$$' in message:
                client.send(f'{name} signed out'.encode('ascii'))
                client.close()
                break

            else:
                client.send("Recieved".encode("ascii"))
                print(message)

        except Exception as inst:
            print("An error occured!")
            print(inst)
            client.close()
            break

receive()