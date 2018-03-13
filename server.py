import zmq
import sys
import os
import math

def dc(s):
    return s.decode("ascii")

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
       op, *msg = s.recv_multipart()
       print(op)

       if op == b"login":
            clientAddress,clientPort,nickname = msg
            csocket = context.socket(zmq.REQ)
            csocket.connect("tcp://{}:{}".format(dc(clientAddress),dc(clientPort)))
            clientes[nickname] =csocket 
            s.send(b"ok")
            print(clientes)
    
       if op == b"call":
            sender, dest,*n = msg
            s.send(b"ok")
            dataMia = [b"Conectar",dest]
            clientes[sender].send_multipart(dataMia)
            respuestaMia = clientes[sender].recv()
            print(respuestaMia)
            dataCliente = [b"Conectar",sender]
            clientes[dest].send_multipart(dataCliente)
            respuestaCliente = clientes[dest].recv()
            print(respuestaCliente)

       if op == b"Conectado":
            dest,data = msg
            s.send(b"recibido")
            print(dest)
            datos = [b"Conectado",data]
            clientes[dest].send_multipart(datos)
            respuesta = clientes[dest].recv()
            print(respuesta)
if __name__ == '__main__':
    main()
