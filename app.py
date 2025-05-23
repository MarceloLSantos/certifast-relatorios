import datetime
import json
import os
import string
import requests
import streamlit as st
import pandas as pd

def formatarMoeda(valor=0):
    return format(valor, '_.2f').replace(".",",").replace("_",".")

def formatarPercentual(valor):
    return format(valor, '_.2f').replace(".",",").replace("_",".")
def autenticar_usuario(username, password):
    # URL da API PHP
    url = "https://sistema.certifast.com.br/api/autenticar/"

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'My Python API Script'
    }
    # Dados a serem enviados para a API
    data = {
    'username': username,
    'password': password,
    'api_python': 'certifast@api-python'
    }
    data_json = json.dumps(data)

    # Fazendo a requisição POST para a API
    response = requests.post(url, data_json, headers=headers)

    # Verificando a resposta da API
    if response.status_code == 200:
        resultado = json.loads(response.text)
        st.session_state.nivel_acesso = int(resultado['id_nivel_acesso'])
        st.session_state.nome = resultado['nome_usuario']
        st.session_state.codrev = resultado['cod_rev']
        st.session_state.id_usuario = resultado['id_usuario']
        return resultado
    else:
        return False
    
def log_out():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state["logged_in"] = False
    st.success("Deslogado com sucesso")

st.set_page_config(page_title="CERTIFAST RELATÓRIOS", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# Formatações
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

#SIDEBAR
with st.sidebar:
    if 'forcar_upload' not in st.session_state:
        st.session_state.forcar_upload = False

    logo = 'https://certifast.com.br/img/home/novo/certifast-logo.png'
    st.image(logo, width=250)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in == False:
        st.text_input("E-mail", key="username")
        st.text_input("Senha", key="password", type="password")

        if st.button("Login", key="login"):
            resultado = autenticar_usuario(st.session_state.username, st.session_state.password)
            if resultado:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

    if st.session_state.logged_in == True:
        st.markdown(f"#### Olá, {st.session_state.nome}")
        st.divider()

        if st.session_state.nivel_acesso == 1:
            opcoes_arquivos = ['RELATÓRIOS', 'UPLOAD', 'DELETAR']
            filtro_arquivos = st.selectbox('OPÇÕES', opcoes_arquivos, key='filtro_arquivos')
            
        # Obtém a data atual
        hoje = datetime.date.today()

        # Calcula o primeiro dia do mês anterior
        if hoje.month == 1:
            primeiro_dia_mes_anterior = datetime.date(hoje.year - 1, 12, 1)
        else:
            primeiro_dia_mes_anterior = datetime.date(hoje.year, hoje.month - 1, 1)

        # Define o valor padrão do st.date_input
        data_padrao = primeiro_dia_mes_anterior

        data = st.date_input('DATA', key='data', value=data_padrao)
        mes = format(data.month, '02') if len(str(data.month)) == 1 else data.month
        ano = data.year

        # Pegar dados de Parceiros
        colunas_parceiros = ['Nome Vendedor',
                            'Nome Validador',
                            'COMISSAO',
                            '% Venda',
                            '% Software',
                            '% Hardware',
                            'E-MAIL',
                            'CODREV',
                            'Imposto',
                            'Contabilidade',
                            'Verificação']
        
        try:
            tabela_parceiros = pd.read_excel(f'./dados/Parceiros-{mes}{ano}.xlsx', sheet_name=0, thousands=".", decimal=',', usecols=colunas_parceiros)
            st.session_state.forcar_upload = False
        except:
            st.error(f'DADOS NÃO DISPONÍVEIS')
            st.session_state.forcar_upload = True

        if 'filtro_arquivos' not in st.session_state:
            st.session_state.filtro_arquivos = 'RELATÓRIOS'
        
        if st.session_state.filtro_arquivos == 'RELATÓRIOS' and st.session_state.forcar_upload == False:
            if st.session_state.nivel_acesso == 1:
                opcoes = tabela_parceiros['Nome Validador'].unique()
                opcoes = opcoes.tolist()
                opcoes.insert(0, 'CONSOLIDADO')            
            else:
                opcoes = tabela_parceiros[tabela_parceiros['CODREV'] == int(st.session_state.codrev)]['Nome Validador'].unique()

            filtro_agente = st.selectbox('RELATÓRIOS', opcoes, key='filtro_agente')

        st.button("Logout", key="logout", on_click=log_out)
        
if st.session_state.logged_in == True:
    # deletar arquivos
    if st.session_state.filtro_arquivos == 'DELETAR':
        def excluir_arquivo(arquivo):
            os.remove(f'./dados/{arquivo}')
            st.success(f'Arquivo {arquivo} excluído com sucesso')

        # Listar todos os arquivos excel da pasta dados e permitir o usuário escolher qual deseja excluir
        arquivos = os.listdir('./dados')
        # Listar arquivos que iniciem com valor numérico e terminem com extensão .xlsx
        arquivos = [arquivo for arquivo in arquivos if arquivo.endswith('.xlsx')]
        # Ordenar em ordem alfabetica
        arquivos.sort()
        st.markdown('<p class="sub-header color-blue">EXCLUIR ARQUIVOS</p>', unsafe_allow_html=True)
        arquivo_selecionado = st.selectbox('Selecione o arquivo para excluir', arquivos, key='arquivo_selecionado')
        st.button("Excluir", key="excluir", on_click=excluir_arquivo, args=(arquivo_selecionado,))
        st.stop()

    if st.session_state.filtro_arquivos == 'UPLOAD' and st.session_state.forcar_upload == True:
        # Inserir opção de upload de arquivos do tipo excel
        st.markdown('<p class="sub-header color-blue">UPLOAD DE VENDAS E VALIDAÇÕES</p>', unsafe_allow_html=True)
        st.error('OBS: ENVIE OS ARQUIVOS DE VENDAS E VALIDAÇÕES NO FORMATO R-MMAAAA.xlsx E V-MMAAAA.xlsx')
        # As planilhas são enviadas em um unico file_uploader com nome no formato V-mmyy e R-mmyy
        st.file_uploader('Arraste os arquivos excel para esta área', accept_multiple_files=True, type=['xlsx'], key='files_vendas_e_validacoes')

        if st.session_state.files_vendas_e_validacoes:
            for file in st.session_state.files_vendas_e_validacoes:
                # if file.name.startswith('V-') and file.name.endswith('.xlsx') or file.name.startswith('R-') and file.name.endswith('.xlsx'):
                    # Salvar na pasta dados e renomear para o formato MMYYY-Validacoes.xlsx ou MMYYY-Revenda.xlsx
                with open(f'./dados/{file.name}', 'wb') as f:
                    f.write(file.getbuffer())

                # Renomear o arquivo para o formato V-MMAA.xlsx paraMMYYY-Validacoes.xlsx usando mesmo mes e ano do original e fazer o mesmo para o arquivo R-MMAA.xlsx para MMYYY-Revenda.xlsx
                mes = file.name[2:4]
                ano = file.name[4:8]
                if file.name.startswith('V-'):
                    # Verificar se o arquivo ja esiste e deletar se existir
                    if os.path.exists(f'./dados/{mes}{ano}-Validacoes.xlsx'):
                        os.remove(f'./dados/{mes}{ano}-Validacoes.xlsx')
                    os.rename(f'./dados/{file.name}', f'./dados/{mes}{ano}-Validacoes.xlsx')

                if file.name.startswith('R-'):
                    # Verificar se o arquivo ja esiste e deletar se existir
                    if os.path.exists(f'./dados/{mes}{ano}-Revenda.xlsx'):
                        os.remove(f'./dados/{mes}{ano}-Revenda.xlsx')
                    os.rename(f'./dados/{file.name}', f'./dados/{mes}{ano}-Revenda.xlsx')

                if file.name.startswith('P-'):
                    #Verificar se o arquivo ja esiste e deletar se existir
                    if os.path.exists(f'./dados/Parceiros-{mes}{ano}.xlsx'):
                        os.remove(f'./dados/Parceiros-{mes}{ano}.xlsx')
                    os.rename(f'./dados/{file.name}', f'./dados/Parceiros-{mes}{ano}.xlsx')                        

            # st.session_state.files_vendas_e_validacoes = []
            st.success('ARQUIVOS ENVIADOS COM SUCESSO')
            st.session_state.forcar_upload = False
        st.stop()

    if st.session_state.filtro_arquivos == 'RELATÓRIOS' and st.session_state.forcar_upload == False:
        if st.session_state.filtro_agente in opcoes:
            mes = format(data.month, '02') if len(str(data.month)) == 1 else data.month
            ano = data.year

            if st.session_state.data:
                mes = format(data.month, '02') if len(str(data.month)) == 1 else data.month
                ano = data.year

            pasta = './dados/'
            arquivo_revenda = f'{mes}{ano}-Revenda.xlsx'
            arquivo_validacoes = f'{mes}{ano}-Validacoes.xlsx'
            # arquivo_repasses = 'Repasses.xlsx'
            arquivo_parceiros = f'Parceiros-{mes}{ano}.xlsx'
            
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

                tabela_validacoes.rename(columns={'Desc. Agente Val.': 'Nome Validador'}, inplace = True)

                # Mescla com tabela parceiros para calcular percentuais de comissões
                tabela_validacoes = tabela_validacoes.merge(tabela_parceiros, on='Nome Validador')
                tabela_validacoes['Val. Comiss. Soft'] = tabela_validacoes['Val. Bruto Soft'] * tabela_validacoes['% Software']
                tabela_validacoes['Val. Comiss. Hard'] = tabela_validacoes['Val. Bruto Hard'] * tabela_validacoes['% Hardware']

                # Dropa colunas mescladas
                drop_colunas = ['Nome Vendedor',
                                '% Venda',
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
                # tabela_repasses = pd.read_excel('./dados/Repasses.xlsx', decimal=',')

                if st.session_state.filtro_agente == 'CONSOLIDADO':
                    opcoes = tabela_parceiros['Nome Validador'].unique()

                    # Definir um dataframe vazio df_pagamentos para armazenar os pagamentos consolidados
                    df_pagamentos = pd.DataFrame()

                    # CONSOLIDADO EMISSOES
                    st.markdown('<p class="sub-header color-blue">CONSOLIDADO DE PAGAMENTOS</p>', unsafe_allow_html=True)

                    for opcao in opcoes:
                        # TABELA EMISSOES
                        tabela_validacoes_col_oculta = tabela_validacoes[tabela_validacoes['Nome Validador'] == opcao]
                        tabela_validacoes_col_oculta = tabela_validacoes_col_oculta.drop(columns='Nome Validador')
                        total_comissoes_validacoes = tabela_validacoes_col_oculta["Val. Comiss. Soft"].sum() + tabela_validacoes_col_oculta["Val. Comiss. Hard"].sum()
                        tabela_validacoes_col_oculta.index = range(1, len(tabela_validacoes_col_oculta)+1)

                        # TABELA VENDAS
                        tabela_vendas_col_oculta = tabela_vendas[tabela_vendas['Nome Vendedor'] == opcao]
                        tabela_vendas_col_oculta = tabela_vendas_col_oculta.drop(columns='Nome Vendedor')
                        total_comissoes_vendas = tabela_vendas_col_oculta["Valor Tot. Comiss."].sum()
                        tabela_vendas_col_oculta.index = range(1, len(tabela_vendas_col_oculta)+1)

                        total_comissoes = total_comissoes_validacoes + total_comissoes_vendas

                        # NÃO EXISTEM MAIS tabela_repasses
                        # Criar variavel contabilidade que deve conter o valor da coluna 'Contabilidade' da tabela_parceiros onde o Nome Validador seja igual ao opcao
                        contabilidade = tabela_parceiros['Contabilidade'][tabela_parceiros['Nome Validador'] == opcao].values[0]
                    
                        # contabilidade = 0 if tabela_parceiros['COMISSAO'][tabela_parceiros['Nome Validador'] == opcao].values[0] == 'REVENDEDOR 10' else tabela_repasses["Valor"][1]
                        imposto = total_comissoes * tabela_parceiros['Imposto'][tabela_parceiros['Nome Validador'] == opcao].values[0]
                        total_receber = total_comissoes - contabilidade - imposto

                        if total_receber > 0 or total_receber < 0:
                            df_pagamentos = pd.concat([df_pagamentos, pd.DataFrame({'Agente': [opcao],
                                                                                    'Faixa': [tabela_parceiros['COMISSAO'][tabela_parceiros['Nome Validador'] == opcao].values[0]],
                                                                                    'Qtde Vendas': [len(tabela_vendas_col_oculta)],
                                                                                    'Qtde Validações': [len(tabela_validacoes_col_oculta)],
                                                                                    'Comissão Vendas': [total_comissoes_vendas],
                                                                                    'Comissão Validações': [total_comissoes_validacoes],
                                                                                    'Contabilidade': [contabilidade],
                                                                                    'Imposto': [imposto],
                                                                                    'Total a receber': [total_receber]})], ignore_index=True)

                    #Redefine indice incremental
                    df_pagamentos.index = range(1, len(df_pagamentos)+1)
                    st.dataframe(df_pagamentos.style.format({'Comissão Vendas': 'R$ {:,.2f}',
                                                                        'Comissão Validações': 'R$ {:,.2f}',
                                                                        'Comissão Total': 'R$ {:,.2f}',
                                                                        'Contabilidade': 'R$ {:,.2f}',
                                                                        'Imposto': 'R$ {:,.2f}',
                                                                        'Total a receber': 'R$ {:,.2f}'}))
                else:
                    # TABELA EMISSOES
                    tabela_validacoes_col_oculta = tabela_validacoes[tabela_validacoes['Nome Validador'] == filtro_agente]
                    tabela_validacoes_col_oculta = tabela_validacoes_col_oculta.drop(columns='Nome Validador')
                    total_comissoes_validacoes = tabela_validacoes_col_oculta["Val. Comiss. Soft"].sum() + tabela_validacoes_col_oculta["Val. Comiss. Hard"].sum()
                    tabela_validacoes_col_oculta.index = range(1, len(tabela_validacoes_col_oculta)+1)

                    # TABELA VENDAS
                    tabela_vendas_col_oculta = tabela_vendas[tabela_vendas['Nome Vendedor'] == filtro_agente]
                    tabela_vendas_col_oculta = tabela_vendas_col_oculta.drop(columns='Nome Vendedor')
                    total_comissoes_vendas = tabela_vendas_col_oculta["Valor Tot. Comiss."].sum()
                    tabela_vendas_col_oculta.index = range(1, len(tabela_vendas_col_oculta)+1)

                    total_comissoes = total_comissoes_validacoes + total_comissoes_vendas
                    contabilidade = tabela_parceiros['Contabilidade'][tabela_parceiros['Nome Validador'] == filtro_agente].values[0]

                    # contabilidade = 0 if tabela_parceiros['COMISSAO'][tabela_parceiros['Nome Validador'] == filtro_agente].values[0] == 'REVENDEDOR 10' else tabela_repasses["Valor"][1]
                    imposto = total_comissoes * tabela_parceiros['Imposto'][tabela_parceiros['Nome Validador'] == filtro_agente].values[0]
                    total_receber = total_comissoes - contabilidade - imposto

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
                    #Dropar colunas 'COMISSÃO' e 'CODREV'
                    tabela_validacoes_col_oculta = tabela_validacoes_col_oculta.drop(columns=['COMISSAO', 'CODREV'])
                    st.dataframe(tabela_validacoes_col_oculta.style.format({'Val. Bruto Soft': 'R$ {:,.2f}',
                                                                            'Val. Bruto Hard': 'R$ {:,.2f}',
                                                                            'Val. Comiss. Soft': 'R$ {:,.2f}',
                                                                            'Val. Comiss. Hard': 'R$ {:,.2f}'}))
                    st.divider()
                    st.markdown("**EXTRATO DE VENDAS**")
                    st.dataframe(tabela_vendas_col_oculta.style.format({'Val. Faturamento': 'R$ {:,.2f}',
                                                                        'Valor Tot. Comiss.': 'R$ {:,.2f}'}))
            except:
                st.error('RELATÓRIO AINDA NÃO DISPONÍVEL PARA ESTE MÊS')
                st.stop()
