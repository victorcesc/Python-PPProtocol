import sys
from quadro import Quadro
from subcamada import Subcamada

class Aplicacao(Subcamada):
    
    def __init__(self):
        Subcamada.__init__(self, sys.stdin)
        self.idsessao = 0 #idsessao
        self.sequencia = 0 
        self.debug = False
  
    def recebe(self, dados:Quadro):
        # mostra na tela os dados recebidos da subcamada inferior
        print('Recebido:', dados.data)

    def handle(self):
        # lê uma linha do teclado
      
        dados = sys.stdin.readline()
        # chamada do STOP da sessao...
        if dados == "##stop":
            self.STOP()        
        
        self.sequencia = not self.sequencia
        quadro = Quadro(tiposessao = 0,msgarq = 0,idsessao = self.idsessao,sequencia = self.sequencia,data = dados)      
        #
        # self.idsessao = self.idsessao + 1
        # envia os dados para a subcamada inferior (self.lower)
        print("Enviando:", quadro.data)
        self.lower.envia(quadro)

    def START(self):
        # se for o master inicia uma conexao
        start = Quadro(tiposessao = 1,sequencia = 0,
                idsessao = self.idsessao,
                data="start")
        if self.debug:
            print('[SESSÃO]: iniciando sessão com id =', start.idSessao)
        self.lower.envia(start)
        #self.sequencia = 1

    def STOP(self):
        stop = Quadro(tiposessao = 1,sequencia = 0,
                idsessao = self.idsessao,
                data="stop")
        if self.debug:
            print('[SESSÃO]: STOP sessão com id =', stop.idSessao)
        self.lower.envia(stop)