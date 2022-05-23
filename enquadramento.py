import sys
from serial import Serial
from pypoller import poller

class Enquadramento(poller.Callback):

    def __init__(self, porta_serial, tout):
        self._porta_serial = porta_serial
        self._tout = tout
        poller.Callback.__init__(self,self._porta_serial, self._tout)

        try:
            self._serial = Serial(self._porta_serial, 9600, timeout=self._tout)
        except Exception as e:
            print('Não conseguiu acessar a porta serial', e)
            sys.exit(0)

    def envia(self, dados):
        self.delimita(dados)
        n_bytes = self._serial.write(dados)
        return n_bytes

    def recebe(self):
        dados = self._serial.read(128)
        return dados

    def delimita(self, dados):
        d = bytearray()
        d.append(0x7e)
        d += dados
        d.append(0x7e)
        print(d)

    def handle(self):
        dados = self._serial.read(1)
        self.buffer += dados
        
#     def handle_idle(self, bytes):
        
#         pass
    
#     def handle_rx(self, bytes):

#         pass

#     def handle_prep(self, bytes):
#         pass

#     def handle_esc(self, bytes):
#         pass

#     def handle_timeout(self):
#         'O tratador de evento timeout'
#         self._cnt += 1
#         print(f'Timeout: cnt={self._cnt}')
#         if self._cnt == 3:
#           # desativa o timeout deste callback, e também o evento leitura !
#           self.disable_timeout()         
#           self.disable()

# ####################################   

# # instancia um callback
# cb = CallbackStdin(3)

# # cria o poller (event loop)
# sched = poller.Poller()

# # registra o callback no poller
# sched.adiciona(cb)

# # entrega o controle pro loop de eventos
# sched.despache()