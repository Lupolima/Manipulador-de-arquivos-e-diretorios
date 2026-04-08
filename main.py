from cli import ArgumentosCLI
from diretorio import Diretorio
from organizador import OrganizadorArquivos


# Passo 1: Configuração
# Lê os parâmetros da linha de comando ou pergunta ao usuário
parametros = ArgumentosCLI()
print(parametros)

# Passo 2: Leitura
# Lista todos os arquivos da pasta de entrada, incluindo subpastas
leitura = Diretorio(parametros.origem)
print(leitura)

# Passo 3: Organização
# Copia e renomeia os arquivos na pasta de destino
organizador = OrganizadorArquivos(parametros.destino)
organizador.organizar(leitura.arquivos)

# Passo 4: Relatório
# Gera o arquivo relatorio.txt com o resumo de tudo que foi feito
organizador.gerar_relatorio()
