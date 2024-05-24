from pathlib import Path

import streamlit as st
import pandas as pd

def ler_dados():
    # if not 'dados' in st.session_state:
    pasta_dados = Path(__file__).parent / 'dados'

    # Pegar dados de Parceiros
    colunas_parceiros = ['Nome Vendedor',
                            'Desc. Agente Val.',
                            'COMISSAO','% Venda',
                            '% Software','% Hardware',
                            'E-MAIL']
    tabela_parceiros = pd.read_excel(pasta_dados / 'Parceiros.xlsx', sheet_name='Parceiros', thousands=".", decimal=',', usecols=colunas_parceiros)

    # Pegar dados da planilha Revenda.xlsx
    colunas_vendas = ['Nome Vendedor',
                    'Pedido',
                    'Nome Cliente',
                    'Dt.Pedido',
                    'Dt.Verificação',
                    'Desc.Produto',
                    'Val. Faturamento',
                    'Valor Tot. Comiss.']
    tabela_vendas = pd.read_excel(pasta_dados / '012024-Revenda.xlsx', sheet_name='CCR CAMPANHA - AR Certifast -', decimal=',', usecols=colunas_vendas, parse_dates=True)
    tabela_vendas.index = range(1, len(tabela_vendas)+1)

    nome_to_apelido = tabela_parceiros.set_index('Nome Vendedor')['Desc. Agente Val.'].to_dict()
    tabela_vendas['Nome Vendedor'] = tabela_vendas['Nome Vendedor'].replace(nome_to_apelido)

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
    tabela_validacoes = pd.read_excel(pasta_dados / '012024-Validacoes.xlsx', sheet_name='AR CERTIFAST (QUEIROZ E MANTO', thousands=".", decimal=',', usecols=colunas_validacoes, parse_dates=True)
    tabela_validacoes.index = range(1, len(tabela_validacoes)+1)

    # Pegar dados de tabela de Repasses
    tabela_repasses = pd.read_excel(pasta_dados / 'Repasses.xlsx')

    dados = {'tabela_parceiros': tabela_parceiros,
                'tabela_vendas': tabela_vendas,
                'tabela_validacoes': tabela_validacoes,
                'tabela_repasses': tabela_repasses}
    st.session_state['dados'] = dados