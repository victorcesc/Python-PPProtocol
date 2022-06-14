from pypoller import poller
from quadro import Quadro

class Subcamada(poller.Callback):

    def __init__(self, *args):
        poller.Callback.__init__(self, *args)
        self.upper = None
        self.lower = None

    def envia(self, quadro):
        self.lower.envia(quadro)

    def recebe(self, quadro):
        self.lower.recebe(quadro)

    def conecta(self, superior):
        self.upper = superior
        superior.lower = self 