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
            print("lista de conectados: ")
            for cliente in clientes:
                print(cliente)
    
       if op == b"call":
            sender, dest,*n = msg
            s.send(b"ok")
            
         #camilo,cristian,villegas
         #sender,usuario,dest
         #conectados camilo y villegas
         #
            for usuario in clientes:
                if usuario != sender and usuario != dest:
                    dataMia = [b"Conectar",dest]
                    clientes[sender].send_multipart(dataMia)
                    respuestaMia = clientes[sender].recv()
                    print(respuestaMia)

                    dataCliente = [b"Conectar",sender]
                    clientes[dest].send_multipart(dataCliente)
                    respuestaCliente = clientes[dest].recv()
                    print(respuestaCliente)

                    
                    data = [b"Conectar",sender]
                    clientes[usuario].send_multipart(data)
                    respuestaCliente = clientes[usuario].recv()
                    print(respuestaCliente)

                    data2 = [b"Conectar",dest]
                    clientes[usuario].send_multipart(data2)
                    respuestaCliente = clientes[usuario].recv()
                    print(respuestaCliente)

                    data3 = [b"Conectar",usuario]
                    clientes[dest].send_multipart(data3)
                    respuestaCliente = clientes[dest].recv()
                    print(respuestaCliente)

                    data4 = [b"Conectar",usuario]
                    clientes[sender].send_multipart(data4)
                    respuestaCliente = clientes[sender].recv()
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
