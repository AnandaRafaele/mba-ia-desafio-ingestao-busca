# Desafio MBA Engenharia de Software com IA - Full Cycle

## Requisitos

- Python 3.10+ (recomendado usar `venv`)
- Docker e Docker Compose

## Setup

1. Suba o PostgreSQL com pgVector:

```bash
docker compose up -d
```

2. Crie o arquivo `.env` a partir do template:

```bash
cp .env.example .env
```

3. Preencha o `.env` (mínimo para Gemini):

- `GOOGLE_API_KEY`
- `GOOGLE_EMBEDDING_MODEL=models/embedding-001`
- `MODEL_NAME=gemini-2.5-flash-lite`
- `DATABASE_URL` (exemplo compatível com o `docker-compose.yml`):
  - `postgresql+psycopg://postgres:postgres@localhost:5432/rag`
- `PG_VECTOR_COLLECTION_NAME` (ex.: `gpt5_collection`)
- `PDF_PATH` (ex.: `./document.pdf`)

## Instalação

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

1. Ingestão do PDF (gera chunks, embeddings e salva no Postgres/pgVector):

```bash
python src/ingest.py
```

2. Chat via CLI (busca `k=10`, monta prompt e chama a LLM):

```bash
python src/chat.py
```

Exemplo de uso:

```
Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
<resposta baseada no PDF>
```

Para sair:

- pressione ENTER em branco, ou digite `sair`, `exit` ou `quit`
