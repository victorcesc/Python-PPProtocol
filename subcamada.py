import poller 


class Subcamada(poller.Callback):
    

    def __init__(self,*args):
        poller.Callback(self,*args)
        self.upper = None
        self.lower = None

    def envia(self,quadro):
        raise NotImplementedError('abstrato')

    def recebe(self,quadro):
        raise NotImplementedError('abstrato')

    def conecta(self,superior):
        self.upper = superior
        superior.lower = self 