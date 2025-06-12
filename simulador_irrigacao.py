import random
import time
from datetime import datetime
from pymongo import MongoClient

# Conectando ao MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client.irrigacao
colecao = db.leituras

# Função para gerar leitura simulada
def gerar_leitura():
    linhas = []
    sensor_id = 1

    for line_id in range(1, 10):  # 9 linhas
        sensores = []
        num_sensores = random.randint(1, 3)  # 1 a 3 sensores por linha
        total_umidade = 0

        for _ in range(num_sensores):
            umidade = round(random.uniform(40, 55), 1)
            sensores.append({
                "sensor_id": sensor_id,
                "humidity": umidade
            })
            total_umidade += umidade
            sensor_id += 1

        media = round(total_umidade / num_sensores, 1)
        linhas.append({
            "line_id": line_id,
            "avg_humidity": media,
            "valve_state": random.choice([True, False]),
            "sensors": sensores
        })

    return {
        "device_id": "3J9pR7",
        "timestamp": datetime.utcnow(),
        "rtc_synced": True,
        "connectivity": {
            "wifi": True,
            "aws": True
        },
        "lines": linhas
    }

# Loop infinito para envio a cada 10 segundos
print("Enviando dados para o MongoDB a cada 10 segundos. Pressione Ctrl+C para parar.")
try:
    while True:
        dado = gerar_leitura()
        colecao.insert_one(dado)
        print(f"Leitura enviada em {dado['timestamp']}")
        time.sleep(10)
except KeyboardInterrupt:
    print("\nParado pelo usuário.")
#Comentando alteração via GIT --Guilherme
