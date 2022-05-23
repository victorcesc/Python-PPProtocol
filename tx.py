# Seção Meu Drive simplificada com atalhos … 
# Nas próximas semanas, os itens presentes em mais de uma pasta serão substituídos por atalhos. O acesso a pastas e arquivos não mudará.Saiba mais

#!/usr/bin/python3
from enquadramento import Enquadramento
import sys

try:
  porta = sys.argv[1]
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

msg = 'oi eu sou o jhonatan'

serial = Enquadramento(porta, 10)

n = serial.envia(msg.encode('ascii'))
print('Enviou %d bytes' % n)

input('Digite ENTER para terminar:')

sys.exit(0)