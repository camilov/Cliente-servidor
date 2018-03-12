import zmq
import time
import sys
import os
import json


def main():
	if len(sys.argv) != 2:
		print ("Error")
		exit()

	port = sys.argv[1]

	context = zmq.Context()
	s = context.socket(zmq.REP)
	s.bind("tcp://*:{}".format(port))

	#Asignando puerto a clientes de entrada
	peta=4000

	listausuarios={}


	while True:
		msg = s.recv_json()
		if msg["op"]=="Registrarse":
			peta+=1
			#Añadiendo cada usuario que se conecta al diccionario
			usuarionuevo = context.socket(zmq.REQ)
			usuarionuevo.connect("tcp://{}:{}".format(msg["ip"], peta))
			listausuarios[msg["nombreenv"]] = usuarionuevo
			#Enviandole el puerto al usuario para crear el canal.
			s.send_json(peta)

		elif msg["op"]=="LlamarGrupo":

			s.send_json("Listo")
			for usertoconect in listausuarios:
				if usertoconect != msg["nombreenv"]:
					emisor = listausuarios[msg["nombreenv"]]
					emisor.send_json({"op": "Estableciendo", "receptor": usertoconect})
					emisor.recv_string()
					receptor = listausuarios[usertoconect]
					receptor.send_json({"op":"Estableciendo","receptor": msg["nombreenv"]})
					receptor.recv_string()

		elif msg["op"]=="Llamar":
			s.send_json("Listo")
			usertoconect=s.recv_json()
			s.send_json("Listo")

			if listausuarios.get(usertoconect)!= None:				

				emisor = listausuarios[msg["nombreenv"]]
				emisor.send_json({"op": "Estableciendo", "receptor": usertoconect})
				emisor.recv_string()
				receptor = listausuarios[usertoconect]
				receptor.send_json({"op":"Estableciendo","receptor": msg["nombreenv"]})
				receptor.recv_string()
			else:
				print("Usuario no conectado")
				
				
		elif msg["op"] == "Online":			
				s.send_json("Listo")
				receptor=listausuarios[msg["touser"]]
				receptor.send_json(msg)
				receptor.recv_string()
				print("conectando")


		else:
			print("Operacion no permitida")

if __name__=='__main__':
    main()

