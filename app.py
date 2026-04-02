import streamlit as st
import requests

st.title("Cadastro 🚀")

mensagem = st.text_input("Digite uma mensagem:")

categoria = st.selectbox(
    "Escolha uma categoria:",
    ["Trabalho", "Estudo", "Pessoal"]
)

if st.button("Enviar"):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdwYdIOIYzZPJRQLspIA_rqx-C4XvhasGVaDksuuaGn--QLuQ/formResponse"

    dados = {
        "entry.377580072": mensagem,
        "entry.1339358369": categoria
    }

    resposta = requests.post(url, data=dados)

    if resposta.status_code == 200:
        st.success("Enviado com sucesso!")
    else:
        st.error("Erro ao enviar!")
