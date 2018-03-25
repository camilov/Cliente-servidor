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
    
       

       if op == b"callg":
            sender, group,*n = msg
            s.send(b"ok")

            
       if op == b"call":
            sender, dest,*n = msg
            s.send(b"ok")


            if dest == b'grupo':
                listco[sender] = dc(sender)
                print("lista conectado1")
                #for d in listco:
                #    print(d)
                for i in listco:
                    for c in clientes:
                        if i == c:
                            data7 = [b"Conectar",c]
                            clientes[sender].send_multipart(data7)

            elif dest != b'grupo':
                listgd[sender] = dc (sender)
                print("lista conectados2 ")
                for i in listgd:
                    print(i)




        ##    for usuario in clientes:
        ##        print(b"usuario"+usuario)
        ##        if sender != usuario:
        ##            data7 = [b"Conectar",usuario]
        ##            clientes[sender].send_multipart(data7)
        ##            respuestaCliente = clientes[sender].recv()
        ##            for usuario2 in clientes:
        ##                print(b"usuario2"+usuario2)
        #                if usuario != usuario2 and usuario != sender:

        ##                    data6 = [b"Conectar",usuario2]
        ##                    clientes[usuario].send_multipart(data6)
        ##                    respuestaCliente = clientes[usuario].recv()
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
