-- 1. Tabla de Bóveda de Tarjetas (Aislada por seguridad)
-- Solo almacena el PAN enmascarado y el hash irreversible.
CREATE TABLE vault_cards (
    token_id CHAR(64) PRIMARY KEY, -- Hash HMAC-SHA256
    customer_id VARCHAR(50) NOT NULL,
    masked_pan VARCHAR(19) NOT NULL, -- Formato: 4532-XXXXXXXX-8921
    expiry_date VARCHAR(5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla Transaccional Principal
-- Relacionada con la bóveda solo por el token. Optimizado para análisis de datos.
CREATE TABLE transactions_history (
    transaction_id VARCHAR(50) PRIMARY KEY,
    token_id CHAR(64) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency CHAR(3) DEFAULT 'EUR',
    status VARCHAR(20) CHECK (status IN ('COMPLETED', 'FAILED', 'ERROR', 'PENDING')),
    risk_score DECIMAL(5, 2) DEFAULT NULL, -- Preparado para el motor cuantitativo futuro
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (token_id) REFERENCES vault_cards(token_id)
);

-- 3. Tabla de Auditoría (Requisito PCI-DSS v4 Req 10)
-- Registra únicamente la latencia y los endpoints, sin body requests.
CREATE TABLE security_audit_logs (
    log_id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    http_method VARCHAR(10) NOT NULL,
    response_status INT NOT NULL,
    latency_ms DECIMAL(8, 2) NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar extracciones de Data Analysis
CREATE INDEX idx_transactions_amount ON transactions_history(amount);
CREATE INDEX idx_transactions_time ON transactions_history(executed_at);