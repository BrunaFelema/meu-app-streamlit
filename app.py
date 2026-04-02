import streamlit as st
import urllib.parse
import urllib.request

st.title("Enviar para Google Sheets 🚀")

mensagem = st.text_input("Digite uma mensagem:")

if st.button("Enviar"):
    url_base = "https://docs.google.com/forms/d/e/1FAIpQLSdwYdIOIYzZPJRQLspIA_rqx-C4XvhasGVaDksuuaGn--QLuQ/formResponse?entry.377580072="

    mensagem_codificada = urllib.parse.quote(mensagem)

    url_final = url_base + mensagem_codificada

    urllib.request.urlopen(url_final)

    st.success("Enviado com sucesso!")
