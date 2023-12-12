# file: argtest.py
# 
# Script teste para integração com LabTalk
# Desenvolvido por Felipe Cesar Cuellar da Silva <felipecesar@usp.br>
#
# Esse programa serve para listar os argumentos que são enviados pelo LabTalk ao python.
# O primeiro argumento sempre será o caminho para o arquivo em python.
# Os outros argumentos podem ser passados seguindo a sintaxe do Origin no exemplo "argtest.ogs"

import sys

print(f"Quantidade de argumentos: {len(sys.argv)}")
for i in range(len(sys.argv)):
    print(f"Argumento {i+1}: {sys.argv[i]}")
