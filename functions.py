import streamlit as st
import requests
import json
from st_pages import hide_pages
# from time import sleep

def log_in():
    st.session_state["logged_in"] = True
    hide_pages([])
    st.success("Logged in!")
    # sleep(0.5)

def log_out():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state["logged_in"] = False
    st.success("Deslogado com sucesso")

def reset_nivel_acesso(flag=False):
    if st.session_state.nivel_acesso <= 2:
        st.session_state.editar_pedido = True
        st.session_state.excluir_pedido = True
    else:
        st.session_state.editar_pedido = flag
        st.session_state.excluir_pedido = flag

def reset_page():
    st.session_state.data_selecionada = None
    st.session_state.arquivo_selecionado = None

def exibe_login():
    with st.sidebar:
        hide_pages(["page1", "page2" ])

        st.title("Login")
        username = st.text_input("Usuário", key="username")
        password = st.text_input("Senha", key="password", type="password")

        if st.button("Login", key="login"):
            resultado = autenticar_usuario(username, password)
            if resultado:
                st.session_state["logged_in"] = True
                hide_pages([])
                st.success("Login bem-sucedido!")
                # sleep(1.0)
            else:
                st.error("Usuário ou senha inválidos.")

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

def formatarMoeda(valor=0):
    # return format(valor, '.2f')
    return format(valor, '_.2f').replace(".",",").replace("_",".")

def formatarPercentual(valor):
    return format(valor, '_.2f').replace(".",",").replace("_",".")