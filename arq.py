import sys
from subcamada import Subcamada

# ack = 0
# Data = 1
#verifica o id conexao correspondente que esta recebendo
class Arq(Subcamada):
    
    def __init__(self):
        Subcamada.__init__(self, *args)
        self._fsm = self.state_ocioso
  
    def recebe(self, quadro):
        pass
      # dados recebidos da subcamada inferior

    def envia(self,quadro):
        pass

    def state_ocioso(self, tipo):
        if tipo == 0

    def state_espera(self,type):
        

    def handle(self):
      # lê uma linha do teclado
      dados = sys.stdin.readline()

      # converte para bytes ... necessário somente
      # nesta aplicação de teste, que lê do terminal
      dados = dados.encode('utf8') 

      # envia os dados para a subcamada inferior (self.lower)
      self.lower.envia(dados)