import psycopg2
import pandas as pd

DB_PARAMS = {
    "dbname": "systock",
    "user": "systock",
    "password": "systock123",
    "host": "db",
    "port": "5432"
}

def executar_consulta(query):
    """Executa uma consulta SQL e retorna os resultados como um DataFrame."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        conn.set_client_encoding('UTF8')
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        raise Exception(f"Erro ao executar consulta: {e}")