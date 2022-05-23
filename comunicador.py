from socket import *
# import socket
import sys

UDP_IP = sys.argv[1]
UDP_PORT = int(sys.argv[2])


print(UDP_IP)
print(UDP_PORT)
# message = "Victor"

cliente = socket(AF_INET, SOCK_DGRAM,17) # UDP
# cliente.sendto("victor".encode(),(UDP_IP, UDP_PORT))

cliente.bind(('0.0.0.0',5555))


while True:

    try: 
        algo = sys.stdin.readline()
    except KeyboardInterrupt:
        break
    try : 
        cliente.sendto(algo.encode(),(UDP_IP,UDP_PORT))
    except Exception as e:
        print('Erro ao enviar')
    try: 
        dados,addr = cliente.recvfrom(1024)
        print("Recebido: %s vindos de %s" % (dados.encode(),addr))
    except Exception as e:
        print('Erro: ',e)







