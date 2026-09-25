# Previsão de Churn com Machine Learning + Retenção com IA

Projeto em Python que **prevê quais clientes vão cancelar** (churn) com um modelo de Machine Learning treinado em uma base real e pública, e usa a **API do Claude (Anthropic)** para escrever uma mensagem de retenção personalizada de acordo com o risco de cada cliente.

Começou como um pipeline ETL com segmentação por regras fixas (versão 1, em `pipeline/`) e evoluiu para um modelo treinado e avaliado (versão 2, em `ml/`).

## Estrutura

```
etl-python-churn-strategy/
├── ml/
│   ├── 01_exploracao_e_tratamento.ipynb   # análise exploratória e tratamento dos dados
│   ├── 02_modelagem.ipynb                 # Regressão Logística x Random Forest
│   └── 03_risco_e_mensagens.ipynb         # faixa de risco + mensagem com Claude
├── data/
│   └── telco_churn.csv                    # base IBM Telco Customer Churn (7.043 clientes)
├── models/                                # modelo treinado (gerado pelo notebook 03)
├── pipeline/                              # versão 1: ETL com regras fixas de score
└── requirements.txt
```

## Dados

**Telco Customer Churn** (IBM, pública): 7.043 clientes de uma operadora, com dados de contrato, serviços, cobrança e a coluna `Churn` (o cliente cancelou?).

Tratamento (notebook 01):
- `TotalCharges` veio como texto, com **11 valores em branco**. Todos eram clientes com `tenure = 0`, que ainda não tinham pago nenhuma fatura. Como não havia histórico de pagamento, **essas linhas foram removidas** (0,16% da base) em vez de preenchidas com a média, que inventaria um valor.
- Nenhum outlier pelo método IQR nas variáveis numéricas.
- Alvo **desbalanceado**: 26,6% de churn. Por isso a acurácia não é a métrica principal.

## Modelagem

Critério de escolha: **priorizar o recall** (pegar o máximo de clientes que realmente vão cancelar, porque perder um cliente custa mais do que oferecer um desconto a quem ia ficar), acompanhando a **AUC**.

- Pré-processamento em `Pipeline` (One-Hot Encoding + padronização), sem vazamento entre treino e teste.
- `class_weight='balanced'` para compensar o desbalanceamento.
- Separação 80/20 estratificada + validação cruzada de 5 dobras no treino.

| Modelo | Recall (CV) | AUC (CV) | Recall (teste) | Precisão (teste) | AUC (teste) |
|---|---|---|---|---|---|
| **Regressão Logística** (escolhido) | **0,802** | 0,846 | **0,797** | 0,490 | 0,835 |
| Random Forest | 0,769 | 0,847 | 0,781 | 0,517 | 0,833 |

A Regressão Logística foi escolhida por ter **maior recall** com AUC equivalente e por ser **interpretável**: os coeficientes mostram o que aumenta ou reduz o risco.

- Aumentam o churn: contrato mensal, internet por fibra ótica, streaming de TV/filmes.
- Reduzem o churn: tempo como cliente (`tenure`, fator mais forte), contrato de dois anos, internet DSL.
- Observação: `MonthlyCharges` e `TotalCharges` são colineares (`TotalCharges` ≈ `tenure` × `MonthlyCharges`), então seus coeficientes isolados não devem ser interpretados sozinhos.

## Do modelo à ação

O notebook 03 transforma a probabilidade prevista em faixa de risco e confere cada faixa contra o churn real do teste:

| Faixa | Probabilidade | Clientes (teste) | Churn real |
|---|---|---|---|
| Alto | ≥ 70% | 378 | 61,1% |
| Médio | 40% a 70% | 343 | 27,7% |
| Baixo | < 40% | 686 | 7,0% |

Para cada cliente, a faixa e os fatores do perfil (contrato, tempo de casa, serviços, pagamento) vão no prompt enviado ao Claude, que escreve a mensagem de retenção.

## Conclusões

- **O modelo cumpre o objetivo de recall:** no teste, identificou cerca de 80% dos clientes que realmente cancelaram (298 de 374). O custo dessa escolha é que aproximadamente metade dos alertas são falsos positivos (precisão de 0,49), o que é aceitável quando a ação de retenção é barata (uma mensagem ou oferta) comparada ao custo de perder o cliente.
- **As faixas de risco são úteis na prática:** o churn real vai de 7% na faixa Baixa para 61% na Alta, então a equipe pode concentrar esforço e orçamento de retenção onde o risco é maior.
- **O que a empresa pode fazer com isso:** os fatores mais fortes sugerem ações concretas, como incentivar a migração do contrato mensal para o anual, oferecer suporte técnico (quem não tem cancela 41,6%, contra 15,2% de quem tem), especialmente a clientes de fibra, e dar atenção especial aos primeiros meses de relacionamento, quando o risco é mais alto.
- **Limitações:** a base é pública, de uma única operadora dos EUA e de um único momento no tempo. Em um cenário real, o modelo precisaria ser treinado com dados da própria empresa, monitorado ao longo do tempo e ter o limiar de decisão ajustado pelo custo real de cada tipo de erro.

## Como executar

```bash
git clone https://github.com/PedroBLS/etl-python-churn-strategy.git
cd etl-python-churn-strategy
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
jupyter notebook ml/
```

Rode os notebooks na ordem 01 → 02 → 03. Para gerar as mensagens, configure a chave da API como variável de ambiente (nunca no código):

```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sua-chave-aqui"
# Linux / Mac
export ANTHROPIC_API_KEY="sua-chave-aqui"
```

Sem a chave, os notebooks rodam normalmente e apenas pulam a geração das mensagens. A versão 1 (`pipeline/etl_pipeline.ipynb`) continua disponível e é executada a partir da pasta `pipeline/`.

## Próximos passos

- [ ] Ajustar o limiar de decisão pelo custo de retenção x custo de perder o cliente
- [ ] Preparação dos dados em PySpark
- [ ] Dashboard interativo com Streamlit
- [ ] Testes unitários com Pytest

## Tecnologias

Python, Pandas, scikit-learn, Matplotlib, Jupyter, API do Claude (Anthropic).

Desenvolvido por Pedro Brandão Leal dos Santos, com apoio do **Claude Code** na escrita do código.
