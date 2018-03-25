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
    listco = {}
    listgd = {}

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
            print("lista de conectados: ")
            for cliente in clientes:
                print(cliente)


       if op == b"call":
            sender, dest,*n = msg
            s.send(b"ok")

            if dest == b'agregar': 
                    
                listgd[sender] = dc(sender)
                print("lista de conectados en tu grupo1")
                for i in listgd:
                    print(i)
            if dest == b'grupo':
                
                for i in listgd:
                    for c in clientes:
                        if  i == c and sender != c:
                            data8 = [b"Conectar",c]
                            clientes[sender].send_multipart(data8)
                            respuestaCliente = clientes[sender].recv()
                            print(respuestaCliente)
                            for c2 in clientes:
                                for x in listgd:
                                    if i == c and c != c2 and c2 == x and  c != sender:
                                        data9 = [b"Conectar",c2]
                                        clientes[c].send_multipart(data9)
                                        respuesta = clientes[c].recv()
                                        print(respuestaCliente)
       if op == b"Conectado":
            dest,data = msg
            s.send(b"Conectados")
            print(dest)
            datos = [b"Conectado",data]
            clientes[dest].send_multipart(datos)
            respuesta = clientes[dest].recv()
            print(respuesta)



if __name__ == '__main__':
    main()
