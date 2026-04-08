# 📁 Organizador Automático de Arquivos

Aplicação em Python que percorre uma pasta de entrada, organiza os arquivos por tipo/extensão em uma pasta de saída com nomes padronizados e gera um relatório detalhado ao final.

---

## 🗂️ Estrutura do projeto

```
├── main.py          # Ponto de entrada — orquestra cli e organizador
├── cli.py           # Parsing de argumentos da linha de comando (argparse)
├── diretorio.py     # Leitura e validação recursiva de diretórios (pathlib)
├── organizador.py   # Classe OrganizadorArquivos — processamento e relatório
└── README.md
```

Cada módulo tem uma responsabilidade única:

| Arquivo | Classe | Responsabilidade |
|---|---|---|
| `main.py` | — | Ponto de entrada; conecta os módulos em sequência |
| `cli.py` | `ArgumentosCLI` | Interpreta os argumentos do terminal |
| `diretorio.py` | `Diretorio` | Lista arquivos e valida a pasta de origem |
| `organizador.py` | `OrganizadorArquivos` | Classifica, renomeia, copia e gera relatório |

---

## ✅ Requisitos atendidos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | Leitura recursiva de diretórios | ✅ |
| 2 | Organização por extensão | ✅ |
| 3 | Renomeação padronizada (`tipo_001.ext`) | ✅ |
| 4 | Geração de relatório em `relatorio.txt` | ✅ |
| 5 | Tratamento de erros (permissão, conflito, arquivo inacessível) | ✅ |

---

## 🐍 Tecnologias utilizadas

- **Python 3** (sem dependências externas)
- `pathlib` — manipulação de caminhos
- `shutil` — cópia de arquivos com metadados
- `os` — verificação de permissões
- `collections.defaultdict` — contadores por tipo
- `datetime` — timestamp no relatório
- `argparse` — interface de linha de comando

---

## 🚀 Como executar

### Forma posicional (simples)
```bash
python main.py ./entrada ./saida
```

### Forma com flags nomeadas
```bash
python main.py --origem ./entrada --destino ./saida
```

### Modo interativo (sem argumentos)
```bash
python main.py
```
O programa perguntará a pasta de origem (obrigatória) e usará `saida/` como destino padrão se o campo for deixado em branco.

> A pasta de destino é criada automaticamente se não existir.

---

## 📂 Estrutura de entrada esperada

```
entrada/
├── contratos/
│   ├── contrato1.pdf
│   └── contrato2.pdf
├── imagens/
│   ├── foto1.jpg
│   └── foto2.jpg
├── dados/
│   ├── clientes.csv
│   └── produtos.json
├── anotacoes.txt
└── arquivo_sem_extensao
```

---

## 📂 Estrutura de saída gerada

```
saida/
├── pdf/
│   ├── pdf_001.pdf
│   └── pdf_002.pdf
├── jpg/
│   ├── jpg_001.jpg
│   └── jpg_002.jpg
├── csv/
│   └── csv_001.csv
├── json/
│   └── json_001.json
├── txt/
│   └── txt_001.txt
├── outros/
│   └── outros_001
└── relatorio.txt
```

---

## 📄 Exemplo de conteúdo do relatório

```
=======================================================
      RELATÓRIO DE ORGANIZAÇÃO DE ARQUIVOS
      Gerado em: 07/04/2026 às 20:35:00
=======================================================

Total de arquivos processados: 8

Resumo por tipo:
  csv: 1
  jpg: 2
  json: 1
  outros: 1
  pdf: 2
  txt: 1

Mapeamento:
  entrada/contratos/contrato1.pdf -> saida/pdf/pdf_001.pdf
  entrada/contratos/contrato2.pdf -> saida/pdf/pdf_002.pdf
  entrada/imagens/foto1.jpg -> saida/jpg/jpg_001.jpg
  entrada/imagens/foto2.jpg -> saida/jpg/jpg_002.jpg
  entrada/dados/clientes.csv -> saida/csv/csv_001.csv
  entrada/dados/produtos.json -> saida/json/json_001.json
  entrada/anotacoes.txt -> saida/txt/txt_001.txt
  entrada/arquivo_sem_extensao -> saida/outros/outros_001

Nenhum erro encontrado durante o processamento.
```

---

## ⚠️ Tratamento de erros

O programa **não para** ao encontrar erros em arquivos individuais. Os seguintes problemas são tratados e registrados no relatório:

- Pasta de origem inexistente
- Falta de permissão de leitura/escrita
- Arquivo inacessível ou corrompido
- Conflito de nomes no destino (adiciona sufixo `_c01`, `_c02`, etc.)

---

## 🔤 Extensões reconhecidas

`txt`, `csv`, `json`, `jpg`, `jpeg`, `pdf`, `png`, `mp4`, `mp3`, `xlsx`, `docx`

Qualquer outra extensão (ou arquivo sem extensão) é direcionado para a pasta `outros/`.
