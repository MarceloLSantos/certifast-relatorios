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
tabela_parceiros = pd.read_excel('./dados/Parceiros.xlsx', sheet_name=0, thousands=".", decimal=',', usecols=colunas_parceiros)

#SIDEBAR
with st.sidebar:
    logo = "https://certifast.com.br/img/home/novo/certifast-logo.png"
    st.image(logo, width=250)

    filtro_agente = st.selectbox('Agente', tabela_parceiros['Nome Validador'])
    data = st.date_input('Data', key='data')
    mes = format(data.month, '02') if len(str(data.month)) == 1 else data.month
    ano = data.year

if st.session_state.data:
    mes = format(data.month, '02') if len(str(data.month)) == 1 else data.month
    ano = data.year

    pasta = './dados/'
    arquivo_revenda = f'{mes}{ano}-Revenda.xlsx'
    arquivo_validacoes = f'{mes}{ano}-Validacoes.xlsx'
    arquivo_repasses = 'Repasses.xlsx'
    arquivo_parceiros = 'Parceiros.xlsx'
    
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

    # Pegar dados da planilha Revenda.xlsx
    colunas_vendas = ['Nome Vendedor',
                    'Pedido',
                    'Nome Cliente',
                    'Dt.Pedido',
                    'Dt.Verificação',
                    'Desc.Produto',
                    'Val. Faturamento',
                    'Valor Tot. Comiss.']

    try:
        # Tenta ler os arquivos
        tabela_validacoes = pd.read_excel(f'./dados/{mes}{ano}-Validacoes.xlsx', sheet_name=0, thousands=".", decimal=',', usecols=colunas_validacoes, parse_dates=True)
        tabela_vendas = pd.read_excel(f'./dados/{mes}{ano}-Revenda.xlsx', sheet_name=0, decimal=',', usecols=colunas_vendas, parse_dates=True)
    except:
        st.error('ARQUIVO NÃO ENCONTRADO!')
        st.stop()

    tabela_validacoes.rename(columns={'Desc. Agente Val.': 'Nome Validador'}, inplace = True)

    # Mescla com tabela parceiros para calcular percentuais de comissões
    tabela_validacoes = tabela_validacoes.merge(tabela_parceiros, on='Nome Validador')
    tabela_validacoes['Val. Comiss. Soft'] = tabela_validacoes['Val. Bruto Soft'] * tabela_validacoes['% Software']
    tabela_validacoes['Val. Comiss. Hard'] = tabela_validacoes['Val. Bruto Hard'] * tabela_validacoes['% Hardware']

    # Dropa colunas mescladas
    drop_colunas = ['Nome Vendedor',
                    'COMISSAO','% Venda',
                    '% Software',
                    '% Hardware',
                    'E-MAIL']
    tabela_validacoes = tabela_validacoes.drop(columns=drop_colunas)

    # Redefine indice incremental
    tabela_validacoes.index = range(1, len(tabela_validacoes)+1)

    tabela_vendas.index = range(1, len(tabela_vendas)+1)

    nome_to_apelido = tabela_parceiros.set_index('Nome Vendedor')['Nome Validador'].to_dict()
    tabela_vendas['Nome Vendedor'] = tabela_vendas['Nome Vendedor'].replace(nome_to_apelido)

    # Pegar dados da planilha Repasses.xlsx
    tabela_repasses = pd.read_excel('./dados/Repasses.xlsx', decimal=',')

    # TABELA EMISSOES
    tabela_validacoes_col_oculta = tabela_validacoes[tabela_validacoes['Nome Validador'] == filtro_agente]
    tabela_validacoes_col_oculta = tabela_validacoes_col_oculta.drop(columns='Nome Validador')
    total_comissoes_validacoes = tabela_validacoes_col_oculta["Val. Comiss. Soft"].sum() + tabela_validacoes_col_oculta["Val. Comiss. Hard"].sum()
    tabela_validacoes_col_oculta.index = range(1, len(tabela_validacoes_col_oculta)+1)
    # tabela_validacoes_col_oculta.reset_index()

    # TABELA VENDAS
    tabela_vendas_col_oculta = tabela_vendas[tabela_vendas['Nome Vendedor'] == filtro_agente]
    tabela_vendas_col_oculta = tabela_vendas_col_oculta.drop(columns='Nome Vendedor')
    total_comissoes_vendas = tabela_vendas_col_oculta["Valor Tot. Comiss."].sum()
    tabela_vendas_col_oculta.index = range(1, len(tabela_vendas_col_oculta)+1)
    # tabela_vendas_col_oculta.reset_index()

    total_comissoes = total_comissoes_validacoes + total_comissoes_vendas
    contabilidade = 0 if tabela_parceiros['COMISSAO'][tabela_parceiros['Nome Validador'] == filtro_agente].values[0] == 'REVENDEDOR 10' else tabela_repasses["Valor"][1]
    imposto = total_comissoes * tabela_repasses["Valor"][0]
    total_receber = total_comissoes - contabilidade - imposto

    st.markdown('''
    <style>
    .small-font-light {
        font-size: 18px !important;
        font-weight: light;
        text-align: center;
    }
                
    .small-font-bold {
        font-size: 18px !important;
        font-weight: bold;
        text-align: center;
    }
                
    .sub-header {
        font-size:22px !important;
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

    st.divider()

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

    st.divider()
    st.markdown("**EXTRATO DE EMISSÕES**")
    st.dataframe(tabela_validacoes_col_oculta.style.format({'Val. Bruto Soft': 'R$ {:,.2f}',
                                                            'Val. Bruto Hard': 'R$ {:,.2f}',
                                                            'Val. Comiss. Soft': 'R$ {:,.2f}',
                                                            'Val. Comiss. Hard': 'R$ {:,.2f}'}))
    st.divider()
    st.markdown("**EXTRATO DE VENDAS**")
    st.dataframe(tabela_vendas_col_oculta.style.format({'Val. Faturamento': 'R$ {:,.2f}',
                                                        'Valor Tot. Comiss.': 'R$ {:,.2f}'}))
