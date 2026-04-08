from pathlib import Path


class Diretorio:
    #le e lista os arquivos da pasta de entrada.
    #Percorre a pasta e todas as suas subpastas automaticamente.

    def __init__(self, caminho: str):
        self.caminho = Path(caminho)
        self.arquivos = self._listar()

    def _listar(self) -> list[Path]:
        """
        Percorre o diretório recursivamente e retorna a lista de arquivos.
        ignora diretórios e pega somente arquivos
        """
        if not self.caminho.exists():
            print(f'  [ERRO] Pasta não encontrada: {self.caminho}')
            return []

        if not self.caminho.is_dir():
            print(f'  [ERRO] O caminho informado não é uma pasta: {self.caminho}')
            return []

        return [item for item in self.caminho.rglob('*') if item.is_file()]

    def __str__(self) -> str:
        #Exibir a lista de arquivos encontrados de forma numerada
        if not self.arquivos:
            return '  Nenhum arquivo encontrado na pasta de origem.\n'

        linhas = [f'  {i+1:>3}. {a}' for i, a in enumerate(self.arquivos)]
        return (
            f'\n{len(self.arquivos)} arquivo(s) encontrado(s):\n'
            + '\n'.join(linhas)
            + '\n'
        )
