import pandas as pd
import numpy as np
from datetime import datetime

# Leitura do arquivo CSV
dados = pd.read_csv("C:/Users/ana.gusmao/Desktop/Airbnb_Open_Data.csv")

# Renomear as colunas
dados.columns = ["id", "nome", "host_id", "identificacao_host", "host_name", "regiao", 
                 "bairro", "lat", "long", "pais", "cod_pais", "reserva_inst", 
                 "politica_cancel", "tipo_quarto", "ano_const", "preco", "taxa_servico", 
                 "min_noites", "n_coments", "ult_review", "coments_mes", "taxa_coments", 
                 "list_host", "disponibilidade_365", "regras", "licenca"]

# Substituir valores vazios por 'NA' nas colunas especificadas
dados[['identificacao_host', 'host_name', 'reserva_inst', 'politica_cancel', 'tipo_quarto']] = \
    dados[['identificacao_host', 'host_name', 'reserva_inst', 'politica_cancel', 'tipo_quarto']].replace('', 'NA')

# Remover símbolos de dólar e converter as colunas 'preco' e 'taxa_servico' para numérico
dados['preco'] = dados['preco'].replace('[\$,]', '', regex=True).astype(float)
dados['taxa_servico'] = dados['taxa_servico'].replace('[\$,]', '', regex=True).astype(float)

# Converter 'reserva_inst' para string
dados['reserva_inst'] = dados['reserva_inst'].astype(str)

# Converter 'ult_review' para datetime
dados['d_last_review'] = pd.to_datetime(dados['ult_review'], format="%m/%d/%Y", errors='coerce')

# Substituir valores NaN em colunas de string por 'NA'
dados = dados.apply(lambda x: x.fillna('NA') if x.dtype == 'object' else x)

# Calcular a diferença de dias entre hoje e a última revisão
dados['d_ult_coment'] = (pd.to_datetime('today') - dados['d_last_review']).dt.days

# Reordenar colunas
dados = dados[['id', 'nome', 'host_id', 'identificacao_host', 'host_name', 'regiao', 
               'bairro', 'lat', 'long', 'pais', 'cod_pais', 'reserva_inst', 
               'politica_cancel', 'tipo_quarto', 'ano_const', 'preco', 'taxa_servico', 
               'min_noites', 'n_coments', 'ult_review', 'd_last_review', 'd_ult_coment', 
               'coments_mes', 'taxa_coments', 'list_host', 'disponibilidade_365', 'regras', 'licenca']]

# Selecionar colunas específicas para df2
df2 = dados[['id', 'host_id', 'identificacao_host', 'regiao', 'reserva_inst', 
             'politica_cancel', 'tipo_quarto', 'preco', 'taxa_servico', 'min_noites', 
             'n_coments', 'd_ult_coment', 'coments_mes', 'taxa_coments', 'disponibilidade_365']]

# Criar a coluna 'range_nota' com base na 'taxa_coments'
df2['range_nota'] = np.where(df2['taxa_coments'] >= 4, 'alta',
                             np.where((df2['taxa_coments'] > 1) & (df2['taxa_coments'] < 4), 'media', 'baixa ou NA'))

# Calcular a correlação de Spearman
df_alta = df2[df2['range_nota'] == 'alta']
correlacao_spearman = df_alta['identificacao_host'].astype('category').cat.codes.corr(df_alta['taxa_coments'], method='spearman')

# Calcular a correlação de Pearson entre 'preco' e 'taxa_coments'
correlacao = df2['preco'].corr(df2['taxa_coments'], method='pearson')

# Exibir as correlações
print(f"Correlação de Spearman: {correlacao_spearman}")
print(f"Correlação de Pearson: {correlacao}")

