import faker
import random
import datetime

# Criar um gerador de dados fictícios com suporte a caracteres especiais
fake = faker.Faker("pt_BR")  # Define português do Brasil para garantir acentos

# Definir período entre 01/02/2025 e 28/02/2025
START_DATE = datetime.date(2025, 2, 1)
END_DATE = datetime.date(2025, 2, 28)

# Lista de produtos fictícios
PRODUCTS = [
    ("P1001", "Rolamento Industrial"),
    ("P1002", "Motor Elétrico"),
    ("P1003", "Correia Transportadora"),
    ("P1004", "Eixo Mecânico"),
    ("P1005", "Engrenagem de Aço"),
    ("P1006", "Sensor de Pressão"),
    ("P1007", "Lubrificante Industrial"),
]

# Gerador de datas aleatórias dentro do período definido
def random_date():
    return fake.date_between_dates(date_start=START_DATE, date_end=END_DATE)

# Criar o arquivo SQL com encoding UTF-8 explícito
with open("../init-db/02_script_dados_systock.sql", "w", encoding="utf-8-sig") as f:
    
    # 🔹 Adicionar comando TRUNCATE antes da inserção dos dados
    f.write("TRUNCATE TABLE venda, pedido_compra, entradas_mercadoria RESTART IDENTITY CASCADE;\n\n")

    # 🔹 Tabela de Pedidos de Compra - 50 registros
    f.write("INSERT INTO pedido_compra (pedido_id, data_pedido, item, produto_id, descricao_produto, ordem_compra, qtde_pedida, filial_id, data_entrega, qtde_entregue, qtde_pendente, preco_compra, fornecedor_id) VALUES\n")
    pedidos = []  # Lista para armazenar os pedidos gerados
    for i in range(50):
        pedido_id = 200 + i
        data_pedido = random_date()
        item = fake.random_int(min=1, max=5)
        produto_id, descricao_produto = random.choice(PRODUCTS)
        ordem_compra = 6000 + i  # Ordem de compra única
        qtde_pedida = fake.random_int(min=15, max=100) if i < 10 else fake.random_int(min=1, max=50)  # Primeiros 10 com qtde alta para consulta 4
        filial_id = 1
        data_entrega = f"'{random_date()}'" if random.random() > 0.5 else "NULL"
        qtde_entregue = fake.random_int(min=0, max=qtde_pedida) if i < 40 else 0  # Últimos 10 sem entrega para consulta 2 e 3
        qtde_pendente = qtde_pedida - qtde_entregue
        preco_compra = round(random.uniform(10.00, 500.00), 2)
        fornecedor_id = fake.random_int(min=1, max=50)

        pedidos.append((ordem_compra, produto_id, qtde_pendente))  # Armazena ordem_compra, produto_id e qtde_pendente

        separator = "," if i < 49 else ";"
        f.write(f"({pedido_id}, '{data_pedido}', {item}, '{produto_id}', '{descricao_produto}', {ordem_compra}, {qtde_pedida}, {filial_id}, {data_entrega}, {qtde_entregue}, {qtde_pendente}, {preco_compra}, {fornecedor_id}){separator}\n")

    # 🔹 Tabela de Entradas de Mercadoria - 50 registros
    f.write("\nINSERT INTO entradas_mercadoria (data_entrada, nro_nfe, item, produto_id, descricao_produto, qtde_recebida, filial_id, custo_unitario, ordem_compra) VALUES\n")
    for i in range(50):
        # Apenas os primeiros 30 pedidos têm entradas para garantir pendências na consulta 2 e 3
        if i < 30:
            ordem_compra, produto_id, _ = pedidos[i]
            data_entrada = random_date()
            nro_nfe = fake.random_int(min=1000, max=9999)
            item = fake.random_int(min=1, max=5)
            descricao_produto = next(desc for pid, desc in PRODUCTS if pid == produto_id)
            qtde_recebida = fake.random_int(min=10, max=100)
            filial_id = 1
            custo_unitario = round(random.uniform(10.00, 500.00), 2)
        else:
            # Gera entradas sem relação com pedidos para teste de integridade
            ordem_compra = 7000 + i  # Ordem de compra não existente
            produto_id, descricao_produto = random.choice(PRODUCTS)
            data_entrada = random_date()
            nro_nfe = fake.random_int(min=1000, max=9999)
            item = fake.random_int(min=1, max=5)
            qtde_recebida = fake.random_int(min=10, max=100)
            filial_id = 1
            custo_unitario = round(random.uniform(10.00, 500.00), 2)

        separator = "," if i < 49 else ";"
        f.write(f"('{data_entrada}', 'NF{nro_nfe}', {item}, '{produto_id}', '{descricao_produto}', {qtde_recebida}, {filial_id}, {custo_unitario}, {ordem_compra}){separator}\n")

    # 🔹 Tabela de Vendas - 50 registros
    f.write("\nINSERT INTO venda (venda_id, data_emissao, horariomov, produto_id, qtde_vendida, valor_unitario, filial_id, item, unidade_medida) VALUES\n")
    for i in range(50):
        venda_id = 300 + i
        data_emissao = random_date()
        horariomov = fake.time(pattern="%H:%M:%S")
        produto_id, descricao_produto = random.choice(PRODUCTS)
        # Gera quantidades variadas, incluindo anomalias para consulta 3.4
        qtde_vendida = 0 if i < 5 else fake.random_int(min=-5, max=0) if i < 10 else fake.random_int(min=1, max=50)
        valor_unitario = round(random.uniform(10.00, 500.00), 2)
        filial_id = 1
        item = fake.random_int(min=1, max=5)
        unidade_medida = random.choice(["UN"])

        separator = "," if i < 49 else ";"
        f.write(f"({venda_id}, '{data_emissao}', '{horariomov}', '{produto_id}', {qtde_vendida}, {valor_unitario}, {filial_id}, {item}, '{unidade_medida}'){separator}\n")

print("✅ Arquivo '02_script_dados_systock.sql' gerado com sucesso e pronto para uso!")