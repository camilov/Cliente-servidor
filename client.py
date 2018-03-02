import zmq
import sys
import pyaudio
import wave


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "g.wav"




def reproducir(name):
    name = sys.argv[4]
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    wf = wave.open(name, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()


def grabar():


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    


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
            data = c.recv()
            print(data)
            c.send_json({"result":"ok"})

        if sys.stdin.fileno() in  sockets:

            command = input()
            act, *res = command.split(' ',1)

            if act == "login":
                s.send_json({"op":"login","clientAddress":clientAddress,"clientPort":clientPort,"nick":nick})
                recibe = s.recv_json()
                print(recibe)
            elif act == "audionote":
                dest,msg = res[0].split(' ', 2)
                data = ({"op":"audionote","sender":nick,"dest":dest,"message":msg})               
                s.send_json(data)
                answer = s.recv_json()
                print(answer)
                

if __name__ == '__main__':
    main()
