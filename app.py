import streamlit as st
from google import genai
import pandas as pd
import datetime

# CONFIGURAÇÃO DA API
API_KEY = "AIzaSyBK8SxFybVq703YsNEasICUWac15hF77Qs"
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Papel e Companhia", layout="wide")

# HEADER
st.markdown("""
<div style='background-color:#003366;padding:20px;border-bottom:5px solid #ffcc00'>
    <h1 style='color:#ffcc00;text-align:center;'>PAPEL E COMPANHIA</h1>
    <h3 style='color:#ffcc00;text-align:center;'>Painel Inteligente de Cadastro | COD 01</h3>
</div>
""", unsafe_allow_html=True)

st.write("")

produto = st.text_input("Nome do Produto")

if st.button("GERAR CADASTRO"):

    if produto == "":
        st.warning("Digite o nome do produto.")
    else:
        with st.spinner("Gerando conteúdo com IA..."):

            prompt = f"""
            Gere o conteúdo COD 01 para o produto {produto}.
            Use ### para separar:
            1 - Ficha Técnica ###
            2 - Logística ###
            3 - Características ###
            4 - Meta Search SEO ###
            6 - Meta Descrição
            """

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            partes = response.text.split("###")

            if len(partes) >= 5:

                ficha = partes[0].strip()
                logistica = partes[1].strip()
                caracteristicas = partes[2].strip()
                meta_search = partes[3].strip()
                meta_desc = partes[4].strip()

                st.subheader("Ficha Técnica")
                st.text_area("", ficha, height=150)

                st.subheader("Logística")
                st.text_area("", logistica, height=120)

                st.subheader("Características")
                st.text_area("", caracteristicas, height=150)

                st.subheader("Meta Search SEO")
                st.text_area("", meta_search, height=100)
                st.caption(f"{len(meta_search)} caracteres")

                st.subheader("Meta Descrição")
                st.text_area("", meta_desc, height=100)
                st.caption(f"{len(meta_desc)} caracteres")

                data = {
                    "Produto": produto,
                    "Ficha Técnica": ficha,
                    "Logística": logistica,
                    "Características": caracteristicas,
                    "Meta Search": meta_search,
                    "Meta Descrição": meta_desc
                }

                df = pd.DataFrame([data])

                st.download_button(
                    "Baixar CSV",
                    df.to_csv(index=False),
                    file_name=f"cadastro_{produto}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.csv",
                    mime="text/csv"
                )

