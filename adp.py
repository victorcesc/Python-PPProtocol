import sys
from quadro import Quadro
from subcamada import Subcamada


class Aplicacao(Subcamada):
    
    def __init__(self):
        Subcamada.__init__(self, sys.stdin)
        self.id = 0
        self.sequencia = 0 #Sequencia de transmissao = 1
  
    def recebe(self, dados:Quadro):
      # mostra na tela os dados recebidos da subcamada inferior
      print('RX:', bytes(dados.serialize()))

    def handle(self):
      # lê uma linha do teclado
      
      dados = sys.stdin.readline()
      
      quadro = Quadro(tiposessao = 0,msgarq = 0,idsessao = self.id,sequencia = self.sequencia,data = dados)      
      self.id = self.id + 1
      self.sequencia = not self.sequencia
      # envia os dados para a subcamada inferior (self.lower)
      print("TX :", quadro.serialize())
      self.lower.envia(quadro)