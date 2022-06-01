# Seção Meu Drive simplificada com atalhos … 
# Nas próximas semanas, os itens presentes em mais de uma pasta serão substituídos por atalhos. O acesso a pastas e arquivos não mudará.Saiba mais

#!/usr/bin/python3
from enq import Enquadramento
import sys

try:
  porta = sys.argv[1]
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

msg = '~} 1 2 3~'

serial = Enquadramento(porta, 10)

serial.envia(msg.encode('ascii'))
# serial.envia(msg)


input('Digite ENTER para terminar:')

sys.exit(0)