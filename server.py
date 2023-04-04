import socket
import threading
import json
import time
vl = open('voters.json')
p = open('parties.json')

voterslist = json.load(vl)
partylist = json.load(p)
clientnum = 4
# host = '127.0.0.1'
host = '192.168.42.18'
port = 6009

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

clients = []
clienthist = []

def isvalid(name,voterid):
    print("Voter Validated")
    found  = False
    for voterp in voterslist:
        if name == voterp['name'] and voterid == voterp['voterid'] and (voterp not in clienthist):
            found = True
            break
    return found

def incre(choice,partylist):
    for party in partylist:
        if party['code'] == choice:
            party['votes']=str(int(party['votes'])+1)


def handle(client,partylist):
    message = client.recv(1024).decode()
    try:
        print("Voter recvd")
        choice = int(message)
        # incre(choice)
        for party in partylist:
            if party['code'] == choice:
                party['votes']=str(int(party['votes']+1))
        client.send("Vote Confirmed".encode('ascii'))
        client.send('$$$ Thanks for voting $$$'.encode('ascii'))
        newmsg = client.recv(1024).decode('ascii')
        print(newmsg)
    except Exception as err:
        print(err,message)
        exit()

def receive(client,address):
    global partylist
    print("Connected with {}".format(str(address)))
    client.send('Please Enter Name ? : '.encode('ascii'))
    name = client.recv(1024).decode('ascii')
    client.send('Please Enter Voter ID ? : '.encode('ascii'))
    voterid = client.recv(1024).decode('ascii')

    if(isvalid(name,voterid)):
        clients.append(client)
        clienthist.append(client)
        print("{} logged in".format(name))
        client.send("You are verified and in ! Vote Responsibly".encode('ascii'))
        client.recv(1024).decode("ascii")
        client.send("Enter your choice : ".encode('ascii'))
        handle(client,partylist)
    else :
        client.send('Error'.encode('ascii'))

def result(partylist):
        winner = ""
        cand=""
        max=0
        equal = True
        totalvotes=0
        print("RESULT :-")
        for party in partylist:
            totalvotes = totalvotes + int(party['votes'])
        for party in partylist:
            name = party['party']
            votes = int(party['votes'])
            print(f'{name} : {votes}')
            if max < votes:
                max = votes
                equal = False
        for party in partylist:
            if int(party["votes"])==int(max):
                winner = party['party']
                cand=party['candidate']
        print("The Winner of this Election is " + cand + " from "+ winner + " !!, Congratulations !!!")
        server.close()
        exit()
def main():
    print("Welcome Moderator ...")
    server.listen()
    while True:
        global clientnum
        if clientnum == 0:
            break
        else :
            clientnum = clientnum-1
        time.sleep(1)
        client, address = server.accept()
        thread = threading.Thread(target=receive, args=(client,address))
        thread.start()
main()
result(partylist)
import json
data = partylist
json_dump = json.dumps(data)
json_data = json.loads(json_dump)
print(json_data)
server.close()
exit()