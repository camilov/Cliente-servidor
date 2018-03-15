import zmq
import sys
import pyaudio
import wave
import time
import threading


WIDTH = 2
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5




def reproducir(SocketServidor,SocketCliente):
   
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    )
    while True:
        op,client = SocketCliente.recv_multipart()
        print(client)
        if op == b"Conectar":
            SocketCliente.send(b"recibido")
            threading.Thread(target= grabar, args=(SocketServidor, client)).start()
        if op == b"Conectado":
            stream.write(client)
            SocketCliente.send(b"escuchando")

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("termino")



def grabar(SocketServidor,dest,):


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
  
    while True:
                
        data = stream.read(CHUNK)
        enviar = [b"Conectado",dest,data]
        SocketServidor.send_multipart(enviar)
        respuestaServer = SocketServidor.recv()
        print(respuestaServer)
        
    

    stream.stop_stream()
    stream.close()
    p.terminate()

    
    
def ec(str):
    return str.encode(encoding="ascii")

def main():
    if len(sys.argv) < 4:
        print("faltan argumentos");
        exit()
    serverAddress = sys.argv[1]
    serverPort = sys.argv[2]
    clientAddress= sys.argv[3]
    clientPort = sys.argv[4]
    nick = sys.argv[5]
    

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(serverAddress,serverPort))

    c = context.socket(zmq.REP)
    c.bind("tcp://{}:{}".format(clientAddress,clientPort))

    poller = zmq.Poller() 
    poller.register(sys.stdin, zmq.POLLIN)
    poller.register(c, zmq.POLLIN)
  

    while True:
        sockets  = dict(poller.poll())

        if c in sockets:
            reproducir(s,c)

        if sys.stdin.fileno() in  sockets:
           
            command = input()
            print('Ingrese comando')
            act, *res = command.split(' ',1)

            if act == "login":
                data = [b"login", ec(clientAddress),ec(clientPort),ec(nick)]
                s.send_multipart(data)
                s.recv()

            elif act == "call":     
                dest, msg = res[0].split(' ',2)
                envio = [b"call" , ec(nick), ec(dest)]
                s.send_multipart(envio)
                respuesta = s.recv()
                print(respuesta)            
                

if __name__ == '__main__':
    main()
