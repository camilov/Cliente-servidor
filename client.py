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
WAVE_OUTPUT_FILENAME = "g.wav"



def reproducir(SocketServidor, SocketCliente):
   
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    )
    while True:
        op, sender ,dest, *data=  SocketCliente.recv_multipart()
        if op == b"Conectar":
            SocketCliente.send(b"ok")
            threading.Thread(target= grabar, args=(SocketServidor, dest)).start()
        elif op == b"Conectado":
            stream.write(data)
            SocketCliente.send("ok")
        

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("termino")



def grabar(SocketServidor,dest):


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
  
    while True:

        data = stream.read(CHUNK)
        print(type(data))
        enviar = [b"Conectado",dest,data]
        SocketServidor.send_multipart(enviar)
        

    

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
            #sender = c.recv_multipart()
            #c.send(b"ok")
            #print(sender)
            #reproducir(audio)
            reproducir(s,c)
                    

        if sys.stdin.fileno() in  sockets:
           
            command = input()
            print('Ingrese comando')
            act, *res = command.split(' ',1)

            if act == "login":
                data = [b"login", ec(clientAddress),ec(clientPort),ec(nick)]
                s.send_multipart(data)
                s.recv()

            elif act == "audionote":
                voz = grabar()
                dest,msg = res[0].split(' ', 2)
                data = [b"audionote", ec(nick), ec(dest)]
                s.send_multipart(data+voz)
                respuesta= s.recv()

            elif act == "call":
                
                dest, msg = res[0].split(' ',2)
                envio = [b"call" , ec(nick), ec(dest)]
                s.send_multipart(envio)
                respuesta = s.recv()
                reproducir(s,c)
             
    threading.Thread(target = reproducir, args = (s, c)).start()
                            
                

if __name__ == '__main__':
    main()
