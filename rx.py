#!/usr/bin/python3

from enquadramento import Enquadramento
import sys

try:
  porta = sys.argv[1]
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

serial = Enquadramento(porta, 10)

# recebe até 128 caracteres
msg = serial.recebe()
print('Recebeu: ', msg)

sys.exit(0)