import streamlit as st
import requests

st.title("Enviar para Google Sheets 🚀")

mensagem = st.text_input("Digite uma mensagem:")

if st.button("Enviar"):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdwYdIOIYzZPJRQLspIA_rqx-C4XvhasGVaDksuuaGn--QLuQ/formResponse"

    dados = {
        "entry.377580072": mensagem
    }

    resposta = requests.post(url, data=dados)

    if resposta.status_code == 200:
        st.success("Enviado com sucesso!")
    else:
        st.error("Erro ao enviar!")
