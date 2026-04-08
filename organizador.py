import os
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class OrganizadorArquivos:
    """
    Responsável por copiar, renomear e organizar os arquivos na pasta de saída.
    Também gera o relatório final.
    """

    EXTENSOES_CONHECIDAS = {
        'txt', 'csv', 'json', 'jpg', 'jpeg', 'pdf',
        'png', 'mp4', 'mp3', 'xlsx', 'docx'
    }

    def __init__(self, caminho_destino: str):
        self.destino = Path(caminho_destino)

        # Contador separado por tipo: {'pdf': 2, 'txt': 1, ...}
        self.contadores = defaultdict(int)

        # Histórico de movimentações para o relatório: [(origem, destino), ...]
        self.mapeamento = []

        # Erros ocorridos sem interromper o programa (Requisito 5)
        self.erros = []

    # -------------------------------------------------------------------------
    # ORGANIZAÇÃO
    # -------------------------------------------------------------------------

    def organizar(self, arquivos: list[Path]) -> None:
        """
        Recebe a lista de arquivos e organiza cada um na pasta de destino.
        Cria as subpastas necessárias automaticamente (Requisito 2).
        """
        try:
            self.destino.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f'  [ERRO] Sem permissão para criar a pasta de destino.')
            return

        print(f'\nOrganizando {len(arquivos)} arquivo(s)...\n')

        for arquivo in arquivos:
            self._processar_arquivo(arquivo)

    def _processar_arquivo(self, arquivo_path: Path) -> None:
        """
        Processa um único arquivo:
          1. Verifica se está acessível
          2. Define o tipo (extensão ou 'outros')
          3. Gera o novo nome padronizado  ex: pdf_001.pdf  (Requisito 3)
          4. Copia para a subpasta correta
        """
        try:
            # Requisito 5: verifica permissão antes de tentar copiar
            if not os.access(arquivo_path, os.R_OK):
                self.erros.append(f'Sem permissão de leitura: {arquivo_path.name}')
                return

            # Requisito 2: classifica pela extensão
            ext = arquivo_path.suffix.lower().lstrip('.')
            tipo = ext if ext in self.EXTENSOES_CONHECIDAS else 'outros'

            # Requisito 3: nome no padrão tipo_001.ext
            self.contadores[tipo] += 1
            novo_nome = f'{tipo}_{self.contadores[tipo]:03d}{arquivo_path.suffix.lower()}'

            # Cria a subpasta e resolve conflito de nomes se necessário
            pasta_destino = self.destino / tipo
            pasta_destino.mkdir(exist_ok=True)
            caminho_saida = self._resolver_conflito(pasta_destino / novo_nome)

            # Copia preservando as datas do arquivo original
            shutil.copy2(arquivo_path, caminho_saida)

            self.mapeamento.append((str(arquivo_path), str(caminho_saida)))
            print(f'  [OK] {arquivo_path.name} -> {caminho_saida}')

        except PermissionError:
            self.erros.append(f'Sem permissão para copiar: {arquivo_path.name}')
            print(f'  [ERRO] Sem permissão: {arquivo_path.name}')

        except OSError as e:
            self.erros.append(f'Erro ao processar {arquivo_path.name}: {e}')
            print(f'  [ERRO] Falha de sistema: {arquivo_path.name}')

        except Exception as e:
            self.erros.append(f'Erro inesperado em {arquivo_path.name}: {e}')
            print(f'  [ERRO] Erro inesperado: {arquivo_path.name}')

    def _resolver_conflito(self, caminho: Path) -> Path:
        """
        Requisito 5: se o arquivo destino já existir,
        adiciona sufixo _c01, _c02... até achar um nome disponível.
        """
        if not caminho.exists():
            return caminho

        contador = 1
        while True:
            novo = caminho.parent / f'{caminho.stem}_c{contador:02d}{caminho.suffix}'
            if not novo.exists():
                return novo
            contador += 1

    # -------------------------------------------------------------------------
    # RELATÓRIO
    # -------------------------------------------------------------------------

    def gerar_relatorio(self) -> None:
        """
        Requisito 4: gera o arquivo relatorio.txt dentro da pasta de saída,
        com total, resumo por tipo, mapeamento completo e erros.
        """
        caminho = self.destino / 'relatorio.txt'
        total = sum(self.contadores.values())

        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write('=' * 55 + '\n')
                f.write('      RELATÓRIO DE ORGANIZAÇÃO DE ARQUIVOS\n')
                f.write(f'      Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}\n')
                f.write('=' * 55 + '\n\n')

                f.write(f'Total de arquivos processados: {total}\n')

                f.write('\nResumo por tipo:\n')
                for tipo, qtd in sorted(self.contadores.items()):
                    f.write(f'  {tipo}: {qtd}\n')

                f.write('\nMapeamento:\n')
                for antigo, novo in self.mapeamento:
                    f.write(f'  {antigo} -> {novo}\n')

                if self.erros:
                    f.write(f'\nArquivos com erro ({len(self.erros)}):\n')
                    for erro in self.erros:
                        f.write(f'  [ERRO] {erro}\n')
                else:
                    f.write('\nNenhum erro encontrado.\n')

            print(f'\nRelatório salvo em: {caminho}')

        except PermissionError:
            print(f'  [ERRO] Sem permissão para criar o relatório.')
        except OSError as e:
            print(f'  [ERRO] Falha ao gravar o relatório: {e}')