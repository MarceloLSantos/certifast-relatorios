import streamlit as st
import pandas as pd

st.set_page_config(page_title="CERTIFAST - RELATÓRIOS", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

@st.cache_data
def load_data():
    tabela_parceiros = "teste" #pd.read_excel('./dados/Parceiros.xlsx', sheet_name='Parceiros', decimal=',', usecols=['Nome Vendedor','Desc. Agente Val.','COMISSAO','% Venda','% Software','% Hardware','E-MAIL'])
    return tabela_parceiros

tabela_parceiros = load_data()

# Pegar dados de Parceiros
# tabela_parceiros = pd.read_excel('./dados/Parceiros.xlsx', sheet_name='Parceiros', decimal=',', usecols=['Nome Vendedor','Desc. Agente Val.','COMISSAO','% Venda','% Software','% Hardware','E-MAIL'])

# Pegar dados da planilha Revenda.xlsx
# colunas_vendas = ['Nome Vendedor',
#                   'Pedido',
#                   'Nome Cliente',
#                   'Dt.Pedido',
#                   'Dt.Verificação',
#                   'Desc.Produto',
#                   'Val. Faturamento',
#                   'Valor Tot. Comiss.']
# tabela_vendas = pd.read_excel('./dados/012024-Revenda.xlsx', sheet_name='CCR CAMPANHA - AR Certifast -', decimal=',', usecols=colunas_vendas, parse_dates=True)

# nome_to_apelido = tabela_parceiros.set_index('Nome Vendedor')['Desc. Agente Val.'].to_dict()
# tabela_vendas['Nome Vendedor'] = tabela_vendas['Nome Vendedor'].replace(nome_to_apelido)

# tabela_vendas.set_index("Nome Vendedor", inplace=True)

# Pegar dados da planilha Validacoes.xlsx
# colunas_validacoes = ['Desc. Agente Val.',
#                       'Pedido',
#                       'Nome Cliente',
#                       'Dt.Pedido',
#                       'Dt.Validação',
#                       'Produto',
#                       'Val. Bruto Soft',
#                       'Val. Bruto Hard',
#                       'Val. Comiss. Soft',
#                       'Val. Comiss. Hard']
# tabela_validacoes = pd.read_excel('./dados/012024-Validacoes.xlsx', sheet_name='AR CERTIFAST (QUEIROZ E MANTO', decimal=',', usecols=colunas_validacoes, parse_dates=True)

# tabela_validacoes.set_index("Desc. Agente Val.", inplace=True)

# Pegar dados de tabela de Repasses
# tabela_repasses = pd.read_excel('dados/Repasses.xlsx')
# print(tabela_repasses)

#SIDEBAR
# logo = "https://certifast.com.br/img/home/novo/certifast-logo.png"
# st.image(logo, width=10)
# filtro_agente = st.sidebar.selectbox("Agente", tabela_parceiros["Desc. Agente Val."])

# st.sidebar.markdown("Desenvolvido por [Studio Cinco Soluções]")
 

st.title("CERTIFAST - RELATÓRIOS") 
# st.markdown("**REVENDAS** - " + filtro_agente)
# tabela_vendas_col_oculta = tabela_vendas[tabela_vendas['Nome Vendedor'] == filtro_agente]
# st.dataframe(tabela_vendas_col_oculta.drop(columns='Nome Vendedor'))
# st.markdown("**VALIDAÇÕES**")
# tabela_validacoes_col_oculta = tabela_validacoes[tabela_validacoes['Desc. Agente Val.'] == filtro_agente]
# st.dataframe(tabela_validacoes_col_oculta.drop(columns='Desc. Agente Val.'))
# st.dataframe(tabela_validacoes)
# st.dataframe(tabela_parceiros)
# st.dataframe(tabela_repasses)

# Atualizar tabela de vendas
# tabela_vendas['PERCENTUAL'] = tabela_parceiros['% Venda'].loc[tabela_parceiros['Nome Vendedor'] == tabela_vendas['Nome Vendedor']]
