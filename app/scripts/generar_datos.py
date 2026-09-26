import json
import uuid
import random
import numpy as np
from datetime import datetime, timedelta

def generate_financial_data(num_records=1000, anomaly_rate=0.05):
    """
    Genera un dataset sintético aplicando distribuciones normales para 
    transacciones estándar y distribuciones uniformes extremas para anomalías.
    """
    records = []
    
    # Parámetros poblacionales (ej. ticket medio de 50€ con desviación de 15€)
    mu_amount, sigma_amount = 50.0, 15.0
    
    for _ in range(num_records):
        is_anomaly = random.random() < anomaly_rate
        
        if not is_anomaly:
            # Comportamiento normal: Distribución Gaussiana
            amount = round(np.random.normal(mu_amount, sigma_amount), 2)
            amount = max(1.0, amount) # Evitar negativos
        else:
            # Comportamiento anómalo (Fraude/Riesgo): Valores extremos
            amount = round(random.uniform(500.0, 3000.0), 2)
            
        # Generación de token simulado (HMAC-SHA256 footprint)
        mock_token = uuid.uuid4().hex + uuid.uuid4().hex 
        
        # Enmascaramiento estricto PCI-DSS (primeros 4, últimos 4)
        bin_bank = random.choice(["4532", "5541", "4916"])
        last_four = f"{random.randint(1000, 9999)}"
        masked_pan = f"{bin_bank}-XXXXXXXX-{last_four}"
        
        records.append({
            "transaction_id": f"TX-{uuid.uuid4().hex[:8].upper()}",
            "customer_id": f"CUST-{random.randint(100, 999)}",
            "amount": amount,
            "currency": "EUR",
            "tokenized_card": mock_token,
            "masked_pan": masked_pan,
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 10000))).isoformat(),
            "is_synthetic_anomaly": is_anomaly # Flag para validación de tests
        })
        
    return records

if __name__ == "__main__":
    dataset = generate_financial_data(500)
    with open("mock_payloads.json", "w") as f:
        json.dump(dataset, f, indent=4)
    print(f"Dataset generado con éxito: {len(dataset)} registros estructurados.")