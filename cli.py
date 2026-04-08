import argparse
from pathlib import Path


class ArgumentosCLI:
    """
    Responsável pelos parâmetros de execução.
    Tenta ler da linha de comando, se não encontrar pergunta ao usuário.
    """

    def __init__(self):
        self._parser = self._criar_parser()
        self._args = self._parser.parse_args()

        # Atributos usados pelo main.py
        self.origem = self._get_origem()
        self.destino = self._get_destino()

    def _criar_parser(self) -> argparse.ArgumentParser:
        #Configura o parser com os argumentos aceitos
        parser = argparse.ArgumentParser()
        parser.add_argument('origem_pos', nargs='?', metavar='ORIGEM',
                            help='Pasta de entrada (posicional)')
        parser.add_argument('destino_pos', nargs='?', metavar='DESTINO',
                            help='Pasta de saída (posicional)')
        parser.add_argument('--origem', type=str, help='Pasta de entrada')
        parser.add_argument('--destino', type=str, help='Pasta de saída')
        return parser

    def _get_origem(self) -> str:
        #Retorna a pasta de origem.
        #Se não foi informada via CLI, pergunta ao usuário (obrigatório).
        
        origem = self._args.origem or self._args.origem_pos

        # Modo interativo: continua perguntando até o usuário informar algo
        while not origem or not origem.strip():
            origem = input('\n  Pasta de origem (obrigatória): ').strip()
            if not origem:
                print('  [!] A pasta de origem não pode ficar em branco.\n')

        return origem

    def _get_destino(self) -> str:
        """
        Retorna a pasta de destino.
        Se não informada, cria automaticamente 'saida/' ao lado da origem.
        """
        destino = self._args.destino or self._args.destino_pos

        if not destino:
            destino = str(Path(self.origem).parent / 'saida')

        return destino

    def __str__(self) -> str:
        """Exibe a configuração antes de iniciar o processamento."""
        return (
            f'\nConfiguração:\n'
            f'  Origem : {self.origem}\n'
            f'  Destino: {self.destino}\n'
        )
