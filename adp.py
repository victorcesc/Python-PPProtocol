import sys
from quadro import Quadro
from subcamada import Subcamada


class Aplicacao(Subcamada):
    
    def __init__(self):
        Subcamada.__init__(self, sys.stdin)
        self.id = 0
  
    def recebe(self, dados:Quadro):
      # mostra na tela os dados recebidos da subcamada inferior
      print('RX:', bytes(dados.serialize()))

    def handle(self):
      # lê uma linha do teclado
      
      dados = sys.stdin.readline()
      quadro = Quadro(tiposessao = 0,msgarq = 0,idsessao = self.id,sequencia = 0,data = dados)      
      self.id = self.id + 1

      # envia os dados para a subcamada inferior (self.lower)
      self.lower.envia(quadro)