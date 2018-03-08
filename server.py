import zmq
import sys
import os
import math

def dc(s):
    return s.decode("ascii")


        
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
       op, *msg = s.recv_multipart()
       print(op)

       if op == b"login":
            clientAddress,clientPort,nickname = msg
            csocket = context.socket(zmq.REQ)
            csocket.connect("tcp://{}:{}".format(dc(clientAddress),dc(clientPort)))
            clientes[nickname] =csocket 
            s.send(b"ok")
            print(clientes)


       if op == b"audionote":
            sender,dest, *audio = msg
            s.send(b"ok")
            data = [sender]+audio
            clientes[dest].send_multipart(data)
            respuestaAudio = clientes[dest].recv()
            print(respuestaAudio)
                 
      
if __name__ == '__main__':
    main()
