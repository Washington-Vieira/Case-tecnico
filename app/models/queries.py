CONSULTA_CONSUMO_POR_PRODUTO = """
SELECT 
    v.produto_id,
    SUM(v.qtde_vendida) AS total_consumo
FROM 
    public.venda v
WHERE 
    EXTRACT(MONTH FROM v.data_emissao) = 2 
    AND EXTRACT(YEAR FROM v.data_emissao) = 2025
GROUP BY 
    v.produto_id
ORDER BY 
    v.produto_id;
"""

CONSULTA_PENDENTES = """
SELECT 
    pc.produto_id,
    pc.descricao_produto,
    pc.qtde_pendente
FROM 
    public.pedido_compra pc
WHERE 
    pc.qtde_pendente > 0
    AND NOT EXISTS (
        SELECT 1 
        FROM public.entradas_mercadoria em 
        WHERE em.produto_id = pc.produto_id 
        AND em.ordem_compra = pc.ordem_compra
    )
ORDER BY 
    pc.produto_id;
"""

CONSULTA_NAO_CONSUMIDOS_NAO_RECEBIDOS = """
SELECT 
    pc.produto_id,
    pc.descricao_produto,
    pc.qtde_pedida
FROM 
    public.pedido_compra pc
WHERE 
    pc.data_pedido BETWEEN '2025-02-01' AND '2025-02-28'
    AND NOT EXISTS (
        SELECT 1 
        FROM public.entradas_mercadoria em 
        WHERE em.produto_id = pc.produto_id 
        AND em.ordem_compra = pc.ordem_compra
    )
    AND NOT EXISTS (
        SELECT 1 
        FROM public.venda v 
        WHERE v.produto_id = pc.produto_id 
        AND v.data_emissao BETWEEN '2025-02-01' AND '2025-02-28'
    )
ORDER BY 
    pc.produto_id;
"""

CONSULTA_TRANSFORMACAO = """
SELECT 
    CONCAT(pc.produto_id, ' - ', COALESCE(pc.descricao_produto, '')) AS produto,
    SUM(pc.qtde_pedida) AS qtde_requisitada,
    TO_CHAR(pc.data_pedido, 'DD/MM/YYYY') AS data_solicitacao
FROM 
    public.pedido_compra pc
GROUP BY 
    pc.produto_id,
    pc.descricao_produto,
    pc.data_pedido
HAVING 
    SUM(pc.qtde_pedida) > 10
ORDER BY 
    qtde_requisitada DESC;
"""

CONSULTA_VENDAS_POR_PRODUTO_CONSUMO = """
SELECT 
    v.produto_id,
    COALESCE(p.descricao_produto, 'Sem descrição') AS descricao_produto,
    SUM(v.qtde_vendida) AS total_vendido,
    SUM(v.qtde_vendida * v.valor_unitario) AS valor_total
FROM 
    public.venda v
LEFT JOIN 
    public.pedido_compra p ON v.produto_id = p.produto_id
WHERE 
    v.data_emissao BETWEEN '2025-02-01' AND '2025-02-28'
GROUP BY 
    v.produto_id, p.descricao_produto
ORDER BY 
    total_vendido DESC;
"""

CONSULTA_PEDIDOS_PENDENTES = """
SELECT 
    pc.produto_id,
    pc.descricao_produto,
    pc.qtde_pedida,
    pc.qtde_entregue,
    pc.qtde_pendente,
    TO_CHAR(pc.data_pedido, 'DD/MM/YYYY') AS data_pedido
FROM 
    public.pedido_compra pc
WHERE 
    pc.data_pedido BETWEEN '2025-02-01' AND '2025-02-28'
    AND pc.qtde_pendente > 0
ORDER BY 
    pc.qtde_pendente DESC;
"""

CONSULTA_ENTRADAS_DE_MERCADORIAS = """
SELECT 
    em.produto_id,
    em.descricao_produto,
    em.nro_nfe,
    SUM(em.qtde_recebida) AS total_recebido,
    SUM(em.qtde_recebida * em.custo_unitario) AS custo_total,
    TO_CHAR(em.data_entrada, 'DD/MM/YYYY') AS data_entrada
FROM 
    public.entradas_mercadoria em
WHERE 
    em.data_entrada BETWEEN '2025-02-01' AND '2025-02-28'
GROUP BY 
    em.produto_id, em.descricao_produto, em.nro_nfe, em.data_entrada
ORDER BY 
    em.data_entrada, em.produto_id;
"""

CONSULTA_DETECCAO_ANAMALIA = """
SELECT 
    'Vendas' AS tabela,
    COUNT(*) AS registros_com_problema,
    'Valores nulos ou negativos' AS tipo_problema
FROM 
    public.venda
WHERE 
    data_emissao BETWEEN '2025-02-01' AND '2025-02-28'
    AND (qtde_vendida <= 0 OR valor_unitario <= 0 OR produto_id IS NULL)
UNION
SELECT 
    'Pedidos de Compra' AS tabela,
    COUNT(*) AS registros_com_problema,
    'Valores nulos ou negativos' AS tipo_problema
FROM 
    public.pedido_compra
WHERE 
    data_pedido BETWEEN '2025-02-01' AND '2025-02-28'
    AND (qtde_pedida <= 0 OR qtde_pendente < 0 OR produto_id IS NULL)
UNION
SELECT 
    'Entradas de Mercadoria' AS tabela,
    COUNT(*) AS registros_com_problema,
    'Valores nulos ou negativos' AS tipo_problema
FROM 
    public.entradas_mercadoria
WHERE 
    data_entrada BETWEEN '2025-02-01' AND '2025-02-28'
    AND (qtde_recebida <= 0 OR custo_unitario <= 0 OR produto_id IS NULL);
"""