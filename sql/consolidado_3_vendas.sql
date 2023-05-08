SELECT
    v.id_marca, 
    v.marca,
    CAST(EXTRACT(MONTH from CAST(v.data_venda AS DATE FORMAT 'DD/MM/YYYY')) AS string)  AS mes,
    CAST(EXTRACT(YEAR from CAST(v.data_venda AS DATE FORMAT 'DD/MM/YYYY')) AS string)  AS ano,
    SUM(v.qtd_venda) AS qtd_venda 
FROM gb_vendas.vendas_totais v 
GROUP BY v.id_marca, v.marca, v.id_linha, v.linha, v.data_venda