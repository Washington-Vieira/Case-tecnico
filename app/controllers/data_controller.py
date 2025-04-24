from models.database import executar_consulta
from models.queries import (
    CONSULTA_CONSUMO_POR_PRODUTO,
    CONSULTA_PENDENTES,
    CONSULTA_NAO_CONSUMIDOS_NAO_RECEBIDOS,
    CONSULTA_TRANSFORMACAO,
    CONSULTA_VENDAS_POR_PRODUTO_CONSUMO,
    CONSULTA_PEDIDOS_PENDENTES,
    CONSULTA_ENTRADAS_DE_MERCADORIAS,
    CONSULTA_DETECCAO_ANAMALIA,
)

def obter_consumo():
    """Obtém o consumo por produto."""
    return executar_consulta(CONSULTA_CONSUMO_POR_PRODUTO)

def obter_pendentes():
    """Obtém os produtos com requisição pendente."""
    return executar_consulta(CONSULTA_PENDENTES)

def obter_nao_consumidos_nao_recebidos():
    """Obtém produtos não consumidos e não recebidos."""
    return executar_consulta(CONSULTA_NAO_CONSUMIDOS_NAO_RECEBIDOS)

def obter_transformacao():
    """Obtém transformações de dados."""
    return executar_consulta(CONSULTA_TRANSFORMACAO)

def obter_vendas_por_produto():
    """Obtém vendas por produto."""
    return executar_consulta(CONSULTA_VENDAS_POR_PRODUTO_CONSUMO)

def obter_pedidos_pendentes():
    """Obtém pedidos pendentes."""
    return executar_consulta(CONSULTA_PEDIDOS_PENDENTES)

def obter_entradas_mercadorias():
    """Obtém entradas de mercadorias."""
    return executar_consulta(CONSULTA_ENTRADAS_DE_MERCADORIAS)

def obter_anomalias():
    """Obtém detecção de anomalias."""
    return executar_consulta(CONSULTA_DETECCAO_ANAMALIA)