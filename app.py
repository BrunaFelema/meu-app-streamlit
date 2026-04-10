import streamlit as st
import urllib.parse
import urllib.request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

st.title("Cadastro 🚀")

mensagem = st.text_input("Digite uma mensagem:")
categoria = st.selectbox("Escolha uma categoria:", ["Trabalho", "Estudo", "Pessoal"])

imagem = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

if st.button("Enviar"):

    # ================= GOOGLE DRIVE =================
    creds_dict = st.secrets["gcp_service_account"]

    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    drive_service = build("drive", "v3", credentials=creds)

    link_imagem = ""

    if imagem is not None:
        file_bytes = io.BytesIO(imagem.read())

        file_metadata = {
            "name": imagem.name
        }

        media = MediaIoBaseUpload(file_bytes, mimetype=imagem.type, resumable=True)

        try:
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            file_id = file.get("id")

            # tornar público
            drive_service.permissions().create(
                fileId=file_id,
                body={"role": "reader", "type": "anyone"}
            ).execute()

            link_imagem = f"https://drive.google.com/uc?id={file_id}"

        except Exception as e:
            st.error(e)

    # ================= GOOGLE FORMS =================
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdwYdIOIYzZPJRQLspIA_rqx-C4XvhasGVaDksuuaGn--QLuQ/formResponse"

    dados = {
    "entry.1339358369": mensagem,
    "entry.1984707711": categoria,
    "entry.377580072": link_imagem
}

    try:
        url_final = url + "?" + urllib.parse.urlencode(dados)
        urllib.request.urlopen(url_final)
        st.success("Enviado com sucesso! 🚀")

    except Exception as e:
        st.error(e)
