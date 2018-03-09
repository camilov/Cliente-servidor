import zmq
import sys
import pyaudio
import wave


WIDTH = 2
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "g.wav"


def wire():
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        stream.write(data, CHUNK)

    print("* done")

    return data

    stream.stop_stream()
    stream.close()

    p.terminate()


def wireCallback():
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()

    p.terminate()




def reproducir(frames):
   
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    )

    for data in frames:    
        stream.write(data)
        

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("termino")



def grabar():


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    
    tiempo = int(RATE / CHUNK * RECORD_SECONDS)
    for i in range(0, tiempo):   
        data = stream.read(CHUNK)
        frames.append(data)
        

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames
    
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
            sender, *audio = c.recv_multipart()
            c.send(b"ok")
            reproducir(audio)

                    

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

                
            
                

if __name__ == '__main__':
    main()
