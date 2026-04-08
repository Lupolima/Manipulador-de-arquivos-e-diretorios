from cli import ArgumentosCLI
from diretorio import Diretorio
from organizador import OrganizadorArquivos


print('=' * 60)
print('  ORGANIZADOR AUTOMÁTICO DE ARQUIVOS')
print('=' * 60)

#Lê os parâmetros de linha de comando ou pergunta para usuário
parametros = ArgumentosCLI()
print(parametros)

#Leitura lista todos os arquivos da pasta de entrada, incluindo subpastas
leitura = Diretorio(parametros.origem)
print(leitura)

#Organiza copia e renomeia os arquivos na pasta destino
organizador = OrganizadorArquivos(parametros.destino)
organizador.organizar(leitura.arquivos)

#Relatório gera o arquivo relatorio.txt resumo do que foi feito
organizador.gerar_relatorio()
