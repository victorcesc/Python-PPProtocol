from arq import Arq
from pypoller import poller
import sys
import argparse
from sessao import Sessao
from subcamada import Subcamada
from enq import Enquadramento
from adp import Aplicacao
from serial import Serial

parser = argparse.ArgumentParser()
parser.add_argument('porta', help='define a porta serial a ser usada')
parser.add_argument('--debug', help='mostra depuração do código', action='store_true')
parser.add_argument('--master', help='define como o inicializador de conexão', action='store_true')
parser.add_argument('--idSessao', help='define o id da sessão')
args = parser.parse_args()

Timeout = 7 

# nome da porta serial informada como primeiro argumento
# de linha de comando
porta = args.porta

# cria objeto Enquadramento
enq = Enquadramento(porta, Timeout)

# Cria objeto Aplicacao
app = Aplicacao()

arq = Arq(Timeout)

sessao = Sessao(Timeout)
# sessao.enable()
# sessao.enable_timeout()
# Conecta as subcamadas
# Deve ser feito a partir da subcamada inferior
# enq.conecta(app)
enq.conecta(arq)
arq.conecta(sessao)
sessao.conecta(app)
# cria o Poller e registra os callbacks
sched = poller.Poller()

sched.adiciona(enq)
sched.adiciona(app)

if args.debug:
    app.debug = True
    sessao.debug = True
    arq.debug = True
    enq.debug = True

if args.master:
    sessao.master = 1
    if args.idSessao:
        app.START(int(args.idSessao))
    else:
        app.START(0)

# sched.adiciona(arq)
# enq.enable()
# enq.enable_timeout()
# entrega o controle ao Poller

try:
    sched.despache()
except:
    sys.exit()