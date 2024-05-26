import streamlit as st
import pandas as pd

st.set_page_config(page_title="CERTIFAST - RELATÓRIOS", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Pegar dados de Parceiros
colunas_parceiros = ['Nome Vendedor',
                     'Nome Validador',
                     'COMISSAO','% Venda',
                     '% Software',
                     '% Hardware',
                     'E-MAIL']
tabela_parceiros = pd.read_excel('./dados/Parceiros.xlsx', sheet_name='Parceiros', thousands=".", decimal=',', usecols=colunas_parceiros)

# Pegar dados da planilha Validacoes.xlsx
colunas_validacoes = ['Desc. Agente Val.',
                      'Pedido',
                      'Nome Cliente',
                      'Dt.Pedido',
                      'Dt.Validação',
                      'Produto',
                      'Val. Bruto Soft',
                      'Val. Bruto Hard',
                      'Val. Comiss. Soft',
                      'Val. Comiss. Hard']
tabela_validacoes = pd.read_excel('./dados/012024-Validacoes.xlsx', sheet_name='AR CERTIFAST (QUEIROZ E MANTO', thousands=".", decimal=',', usecols=colunas_validacoes, parse_dates=True)
tabela_validacoes.index = range(1, len(tabela_validacoes)+1)

# Pegar dados da planilha Revenda.xlsx
colunas_vendas = ['Nome Vendedor',
                  'Pedido',
                  'Nome Cliente',
                  'Dt.Pedido',
                  'Dt.Verificação',
                  'Desc.Produto',
                  'Val. Faturamento',
                  'Valor Tot. Comiss.']
tabela_vendas = pd.read_excel('./dados/012024-Revenda.xlsx', sheet_name='CCR CAMPANHA - AR Certifast -', decimal=',', usecols=colunas_vendas, parse_dates=True)
tabela_vendas.index = range(1, len(tabela_vendas)+1)

nome_to_apelido = tabela_parceiros.set_index('Nome Vendedor')['Desc. Agente Val.'].to_dict()
tabela_vendas['Nome Vendedor'] = tabela_vendas['Nome Vendedor'].replace(nome_to_apelido)

# tabela_vendas.set_index("Nome Vendedor", inplace=True)

# Pegar dados de tabela de Repasses
tabela_repasses = pd.read_excel('dados/Repasses.xlsx')
# print(tabela_repasses)

#SIDEBAR
# filtro_agente = st.sidebar.selectbox("Agente", tabela_parceiros["Nome Validador"])

logo = "https://certifast.com.br/img/home/novo/certifast-logo.png"
st.image(logo, width=250)
# st.write(f"**{filtro_agente}**")
st.divider()

# TABELA EMISSOES
tabela_validacoes_col_oculta = tabela_validacoes #[tabela_validacoes['Nome Validador'] == filtro_agente]
tabela_validacoes_col_oculta = tabela_validacoes_col_oculta.drop(columns='Nome Validador')
total_comissoes_validacoes = tabela_validacoes_col_oculta["Val. Comiss. Soft"].sum() + tabela_validacoes_col_oculta["Val. Comiss. Hard"].sum()
tabela_validacoes_col_oculta.index = range(1, len(tabela_validacoes_col_oculta)+1)
# tabela_validacoes_col_oculta.reset_index()

# TABELA VENDAS
tabela_vendas_col_oculta = tabela_vendas #[tabela_vendas['Nome Vendedor'] == filtro_agente]
tabela_vendas_col_oculta = tabela_vendas_col_oculta.drop(columns='Nome Vendedor')
total_comissoes_vendas = tabela_vendas_col_oculta["Valor Tot. Comiss."].sum()
tabela_vendas_col_oculta.index = range(1, len(tabela_vendas_col_oculta)+1)
# tabela_vendas_col_oculta.reset_index()

total_comissoes = total_comissoes_validacoes + total_comissoes_vendas
contabilidade = tabela_repasses["Valor"][1]
imposto = total_comissoes * tabela_repasses["Valor"][0]
total_receber = total_comissoes - contabilidade - imposto

st.markdown('''
<style>
.small-font-light {
    font-size: 14px !important;
    font-weight: light;
    text-align: center;
}
            
.small-font-bold {
    font-size: 14px !important;
    font-weight: bold;
    text-align: center;
}
            
.sub-header {
    font-size:18px !important;
    font-weight: bold;
    text-align: center;
}
            
.color-green {
    color: #00bb00;
}
            
.color-blue {
    color: #0000bb;
}
            
.color-red {
    color: #dd0000;
}
</style>
''', unsafe_allow_html=True)

# CONSOLIDADO EMISSOES
st.markdown('<p class="sub-header color-blue">VALIDAÇÕES DE SOFTWARE E HARDWARE</p>', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns([0.16,0.16,0.16,0.16,0.16,0.16])
col7, col8, col9, col10, col11, col12 = st.columns([0.16,0.16,0.16,0.16,0.16,0.16])

col1.markdown('<p class="small-font-bold">Quantidade</p>', unsafe_allow_html=True)
col2.markdown('<p class="small-font-bold">Bruto Software</p>', unsafe_allow_html=True)
col3.markdown('<p class="small-font-bold">Bruto Hardware</p>', unsafe_allow_html=True)
col4.markdown('<p class="small-font-bold">Comissão Software</p>', unsafe_allow_html=True)
col5.markdown('<p class="small-font-bold">Comissão Hardware</p>', unsafe_allow_html=True)
col6.markdown('<p class="small-font-bold">Total Comissão</p>', unsafe_allow_html=True)

col7.markdown('<p class="small-font-light">{:,.0f}</p>'.format(tabela_validacoes_col_oculta["Pedido"].count()), unsafe_allow_html=True)
col8.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(tabela_validacoes_col_oculta["Val. Bruto Soft"].sum()), unsafe_allow_html=True)
col9.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(tabela_validacoes_col_oculta["Val. Bruto Hard"].sum()), unsafe_allow_html=True)
col10.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(tabela_validacoes_col_oculta["Val. Comiss. Soft"].sum()), unsafe_allow_html=True)
col11.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(tabela_validacoes_col_oculta["Val. Comiss. Hard"].sum()), unsafe_allow_html=True)
col12.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(total_comissoes_validacoes), unsafe_allow_html=True)

# CONSOLIDADO VENDAS
st.markdown('<p class="sub-header color-green">VENDAS DE CERTIFICADOS</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.33, 0.33, 0.33])
col7, col8, col9 = st.columns([0.33, 0.33 ,0.33])

col1.markdown('<p class="small-font-bold">Quantidade</p>', unsafe_allow_html=True)
col2.markdown('<p class="small-font-bold">Faturamento</p>', unsafe_allow_html=True)
col3.markdown('<p class="small-font-bold">Comissão</p>', unsafe_allow_html=True)

col7.markdown('<p class="small-font-light">{:,.0f}</p>'.format(tabela_vendas_col_oculta["Pedido"].count()), unsafe_allow_html=True)
col8.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(tabela_vendas_col_oculta["Val. Faturamento"].sum()), unsafe_allow_html=True)
col9.markdown('<p class="small-font-light">R$ {:,.2f}</p>'.format(total_comissoes_vendas), unsafe_allow_html=True)

# CUSTOS E REPASSES
# st.markdown('<p class="sub-header color-red">CUSTOS E REPASSES | FECHAMENTO DO MÊS</p>', unsafe_allow_html=True)
col1, col2 = st.columns([0.66, 0.33])
col4, col5, col6 = st.columns([0.33, 0.33, 0.33])
col7, col8, col9 = st.columns([0.33, 0.33 ,0.33])

col1.markdown('<p class="sub-header color-red">CUSTOS E REPASSES</p>', unsafe_allow_html=True)
col2.markdown('<p class="sub-header color-red">FECHAMENTO DO MÊS</p>', unsafe_allow_html=True)

col4.markdown('<p class="small-font-bold">Contabilidade</p>', unsafe_allow_html=True)
col5.markdown('<p class="small-font-bold">Imposto</p>', unsafe_allow_html=True)
col6.markdown('<p class="small-font-bold">Pagar/Receber</p>', unsafe_allow_html=True)
 
col7.markdown('<p class="small-font-bold color-red">R$ {:,.2f}</p>'.format(contabilidade), unsafe_allow_html=True)
col8.markdown('<p class="small-font-bold color-red">R$ {:,.2f}</p>'.format(imposto), unsafe_allow_html=True)
col9.markdown('<p class="small-font-bold color-green">R$ {:,.2f}</p>'.format(total_receber), unsafe_allow_html=True)