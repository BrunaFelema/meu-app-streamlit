import streamlit as st
import urllib.parse
import urllib.request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

st.title("Cadastro 🚀")

# ID DA PASTA DO SEU GMAIL PESSOAL
ID_DA_SUA_PASTA = "1kCwwzZbZ-eruwRtoAESgjbTAYoCFa5pU" 
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdwYdIOIYzZPJRQLspIA_rqx-C4XvhasGVaDksuuaGn--QLuQ/formResponse"

mensagem = st.text_input("Digite uma mensagem:")
categoria = st.selectbox("Escolha uma categoria:", ["Trabalho", "Estudo", "Pessoal"])
imagem = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

if st.button("Enviar"):
    if not mensagem or not imagem:
        st.warning("Por favor, preencha a mensagem e envie uma imagem.")
    else:
        # ================= 1. CREDENCIAIS =================
        creds_dict = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        drive_service = build("drive", "v3", credentials=creds)

        link_imagem = ""

        # ================= 2. UPLOAD PARA O DRIVE =================
        file_bytes = io.BytesIO(imagem.read())
        file_bytes.seek(0) 

        file_metadata = {
            "name": imagem.name,
            "parents": [ID_DA_SUA_PASTA] 
        }

        media = MediaIoBaseUpload(file_bytes, mimetype=imagem.type, resumable=True)

        try:
            # Criar o arquivo
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            file_id = file.get("id")

            # Tornar o link acessível
            drive_service.permissions().create(
                fileId=file_id,
                body={"role": "reader", "type": "anyone"}
            ).execute()

            # Link para o Sheets
            link_imagem = f"https://drive.google.com/uc?id={file_id}"

            # ================= 3. ENVIO PARA O GOOGLE FORMS =================
            # Se as respostas aparecerem trocadas no Sheets, troque os números de entry abaixo!
            dados = {
                "entry.1339358369": mensagem,   
                "entry.1984707711": categoria,  
                "entry.377580072": link_imagem  
            }

            data = urllib.parse.urlencode(dados).encode("utf-8")
            req = urllib.request.Request(URL_FORM, data=data)
            urllib.request.urlopen(req)
            
            st.success("Enviado com sucesso! A imagem já deve estar na sua pasta pessoal. 🚀")
            st.balloons()

        except Exception as e:
            st.error(f"Erro: {e}")
