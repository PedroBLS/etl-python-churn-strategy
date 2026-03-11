import pandas as pd
import anthropic
import os
import logging
from datetime import datetime


# CONFIGURAÇÃO DE LOGS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure sua chave de API como variável de ambiente:
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# 1. EXTRACT

def extract_users(file_path: str) -> list[dict]:
    """Lê o CSV e retorna uma lista de dicionários com os dados dos usuários."""
    logger.info(f"Extraindo dados de '{file_path}'...")
    df = pd.read_csv(file_path)
    logger.info(f"{len(df)} usuários carregados com sucesso.")
    return df.to_dict(orient="records")

# 2. TRANSFORM 

def generate_message_with_claude(user: dict) -> str:
    """
    Usa a API do Claude para gerar uma mensagem de retenção
    personalizada com base no perfil do usuário.
    """
    prompt = f"""
Você é um especialista em Customer Success de uma empresa de SaaS.
Gere uma mensagem de retenção curta, amigável e personalizada em português
para o seguinte cliente:

- Nome: {user['Name']}
- Plano: {user['Plan']}
- Score de uso (0-100): {user['UsageScore']}
- Meses como cliente: {user['MonthsActive']}
- Último login: {user['LastLogin']}

Regras:
- Score abaixo de 20: cliente em risco, ofereça um benefício especial.
- Score entre 20 e 50: cliente moderado, incentive o engajamento.
- Score acima de 50: cliente ativo, reconheça e fidelize.
- Máximo de 3 frases. Não use emojis em excesso. Seja direto e humano.
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def transform_users(users: list[dict]) -> list[dict]:
    """Itera sobre os usuários e adiciona a mensagem gerada pelo Claude."""
    logger.info("Iniciando transformação com a API do Claude...")
    for i, user in enumerate(users, start=1):
        logger.info(f"  [{i}/{len(users)}] Gerando mensagem para {user['Name']}...")
        try:
            user["Message"] = generate_message_with_claude(user)
        except Exception as e:
            logger.error(f"  Erro ao gerar mensagem para {user['Name']}: {e}")
            user["Message"] = "Erro ao gerar mensagem."
    logger.info("Transformação concluída!")
    return users


# 3. LOAD

def save_data(users: list[dict], output_path: str) -> None:
    """Salva os dados transformados em um novo arquivo CSV."""
    df = pd.DataFrame(users)
    df.to_csv(output_path, index=False)
    logger.info(f"Dados salvos em '{output_path}' com sucesso! ✅")


# EXECUÇÃO DO PIPELINE

if __name__ == "__main__":
    start = datetime.now()
    logger.info("=" * 50)
    logger.info("  INICIANDO PIPELINE ETL")
    logger.info("=" * 50)

    # Caminhos dos arquivos
    INPUT_FILE  = "consumer.csv"
    OUTPUT_FILE = "transformed_data.csv"

    # Etapas do ETL
    users = extract_users(INPUT_FILE)
    users = transform_users(users)
    save_data(users, OUTPUT_FILE)

    elapsed = datetime.now() - start
    logger.info(f"Pipeline finalizado em {elapsed.seconds}s. 🚀")
