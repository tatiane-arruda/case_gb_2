    SELECT
        v.id_marca, 
        v.marca, 
        v.id_linha, 
        v.linha, 
        SUM(v.qtd_venda) AS qtd_venda
    FROM gb_vendas.vendas_totais v
    GROUP BY v.id_marca, v.marca, v.id_linha, v.linha