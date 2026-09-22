# 🚀 ETL Pipeline — Retenção de Clientes com IA

Pipeline ETL em Python que usa a **API do Claude (Anthropic)** para gerar
mensagens de retenção personalizadas para cada cliente com base em seu perfil de uso.

---

## 📁 Estrutura do Projeto

```
etl-pipeline-claude-ai/
├── sdw2023.csv          # Base de clientes (entrada)
├── transformed_data.csv # Resultado com mensagens geradas (saída)
├── etl_pipeline.py      # Pipeline principal
├── pipeline.log         # Log de execução (gerado automaticamente)
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md
```

---

## ⚙️ Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/etl-pipeline-claude-ai.git
cd etl-pipeline-claude-ai
```

### 2. Instale as dependências
```bash
pip install pandas anthropic
```

### 3. Configure sua chave da API do Claude
Crie sua chave em: https://console.anthropic.com/

```bash
# Linux / Mac
export ANTHROPIC_API_KEY="sua-chave-aqui"

# Windows
set ANTHROPIC_API_KEY=sua-chave-aqui
```

> ⚠️ **Nunca** coloque sua chave diretamente no código. Use sempre variável de ambiente!

### 4. Execute o pipeline
```bash
python etl_pipeline.py
```

---

## 🔄 Fluxo ETL

```
sdw2023.csv
    │
    ▼
[ EXTRACT ]   → Lê o CSV e carrega os dados dos clientes
    │
    ▼
[ TRANSFORM ] → Para cada cliente, a API do Claude gera
                uma mensagem personalizada baseada no perfil
    │
    ▼
[ LOAD ]      → Salva o resultado em transformed_data.csv
```

---

## 🧠 Lógica de Personalização

| UsageScore | Perfil    | Estratégia                  |
|------------|-----------|-----------------------------|
| < 20       | Em risco  | Oferecer benefício especial |
| 20 – 50    | Moderado  | Incentivar engajamento      |
| > 50       | Ativo     | Reconhecer e fidelizar      |

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **Pandas** — manipulação de dados
- **Anthropic SDK** — integração com a API do Claude
- **Logging** — rastreamento de execução com log em arquivo

---

## 🐙 Como subir no GitHub

```bash
# 1. Inicializa o repositório local
git init

# 2. Adiciona todos os arquivos
git add .

# 3. Cria o primeiro commit
git commit -m "feat: pipeline ETL com integração à API do Claude"

# 4. Define a branch principal
git branch -M main

# 5. Conecta ao repositório remoto
git remote add origin https://github.com/SEU_USUARIO/etl-pipeline-claude-ai.git

# 6. Sobe os arquivos
git push -u origin main
```

---

## 💡 Melhorias futuras

- [ ] Adicionar visualizações com Matplotlib
- [ ] Envio real de e-mails com SMTP
- [ ] Dashboard interativo com Streamlit
- [ ] Testes unitários com Pytest
