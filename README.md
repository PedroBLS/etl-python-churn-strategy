# ETL de Retenção de Clientes com IA

Pipeline ETL em Python (Jupyter Notebook) que segmenta clientes por risco de churn e usa a **API do Claude (Anthropic)** para gerar uma mensagem de retenção personalizada para cada um.

## Estrutura

```
etl-python-churn-strategy/
├── pipeline/
│   ├── etl_pipeline.ipynb   # Pipeline completo (Extract, Transform, Load)
│   └── sdw2023.csv          # Base de exemplo com 10 clientes fictícios
├── .gitignore
└── README.md
```

## Fluxo

```
sdw2023.csv
    │
    ▼
[ EXTRACT ]   Lê o CSV com Pandas e faz uma análise exploratória
              (distribuição por plano, estatísticas do UsageScore)
    │
    ▼
[ TRANSFORM ] Segmenta cada cliente por perfil de risco e envia os dados
              à API do Claude, que gera uma mensagem de retenção
    │
    ▼
[ LOAD ]      Salva o resultado em transformed_data.csv
```

## Segmentação por risco de churn

A segmentação é feita por regras de score sobre o `UsageScore` (0 a 100):

| UsageScore | Perfil   | Estratégia da mensagem      |
|------------|----------|-----------------------------|
| < 20       | Em risco | Oferecer benefício especial |
| 20 a 49    | Moderado | Incentivar engajamento      |
| ≥ 50       | Ativo    | Reconhecer e fidelizar      |

## Como executar

```bash
git clone https://github.com/PedroBLS/etl-python-churn-strategy.git
cd etl-python-churn-strategy/pipeline
pip install pandas anthropic jupyter
```

Configure a chave da API (crie em https://console.anthropic.com/) como variável de ambiente, nunca no código:

```bash
# Linux / Mac
export ANTHROPIC_API_KEY="sua-chave-aqui"

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sua-chave-aqui"
```

Abra o notebook a partir da pasta `pipeline/` (o CSV é lido por caminho relativo) e execute as células em ordem:

```bash
jupyter notebook etl_pipeline.ipynb
```

A saída `transformed_data.csv` é gerada na mesma pasta.

## Tecnologias

- Python 3.10+
- Pandas: extração, análise exploratória e manipulação dos dados
- Anthropic SDK: geração das mensagens com o Claude
- Jupyter Notebook

## Próximos passos

- [ ] Visualizações com Matplotlib
- [ ] Envio real das mensagens por e-mail (SMTP)
- [ ] Dashboard interativo com Streamlit
- [ ] Testes unitários com Pytest
