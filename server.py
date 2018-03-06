import zmq
import sys
import os
import math



def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("loading {}".format(filename))
        files[filename] = files
    return files
        
def main():
    if len(sys.argv) != 2:
        print("Faltan argumentos");
        exit()
    port= sys.argv[1]
    
        

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))##crea el socket



    

    clientes= {}

    print("server ready")
    while True:
       msg = s.recv_json()

       if msg["op"] == "login":
            nickname = msg["nick"] 
            clientAddress = msg["clientAddress"]
            clientPort = msg["clientPort"]
            csocket = context.socket(zmq.REQ)
            csocket.connect("tcp://{}:{}".format(clientAddress,clientPort))
            clientes[nickname] =csocket 
            s.send_json({"result": "OK"})
            print(clientes)


       if msg["op"] == "audionote":
            
            sender = msg["sender"]
            dest = msg["dest"]
            s.send_json({"resp":"ok"})
            audio = s.recv_multipart()
            s.send_json({"resp":"ok"})
            data = {"sender":sender}
            clientes[dest].send_json(data)
            answer = clientes[dest].recv_json()
            clientes[dest].send_multipart(audio)
            answer2 = clientes[dest].recv_json()

           
                 
      
if __name__ == '__main__':
    main()
