import streamlit as st
import pandas as pd
from datetime import date
import os

# configurações da pagina principal
st.set_page_config(page_title="calculadora armazem", layout="wide")

# CSS para ajustar o layout da página e formatação para impressão( não deu certo vou fazer ajustes depois)
st.markdown("""
<style>
    /* Ajustando a largura da área da página */
    .css-1d391kg { 
        width: 50%;  /* Ajusta a largura da página */
        margin: 0 auto;  /* Centraliza o conteúdo */
        padding: 20px;  /* Adiciona algum espaçamento */
    }

    /* Estilo para impressão */
    @media print {
        body {
            width: 100%;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        .css-1d391kg {
            width: 100%;
            margin: 0;
            padding: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Estilo do cabeçalho e forma que consegui para inserir a logo da agrovale.
st.markdown("""
<style>
    table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        font-size: 16px;
    }
    th, td {
        padding: 8px 12px;
        border: 1px solid #ddd;
    }
    th {
        background-color: #f0f2f6;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stMarkdown h3 {
        font-size: 24px;
        color: #444;
        border-bottom: 1px solid #ccc;
        padding-bottom: 5px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do session_state
if 'resultado_fardo' not in st.session_state:
    st.session_state.resultado_fardo = None
if 'resultado_cristal' not in st.session_state:
    st.session_state.resultado_cristal = None
if 'resultado_sacos' not in st.session_state:
    st.session_state.resultado_sacos = None

# Cabeçalho ajustado (logo + título centralizado) 
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo_agrovale.png.png", width=150)

with col2:
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: #1b4d3e; font-size: 36px; margin: 0;">CALCULADORA DE CARGAS</h1>
    </div>
    """, unsafe_allow_html=True)

# logica do codgo para somas
def calcular_distribuicao_fardos(total, num_lotes, cristal=None, demerara=None):
    lotes_inteiros = int(num_lotes)
    tem_meio_lote = num_lotes % 1 != 0
    
    if tem_meio_lote:
        tamanho_lote = int(total / (lotes_inteiros + 0.5))
        resto = total - (lotes_inteiros * tamanho_lote)
    else:
        tamanho_lote = total // lotes_inteiros
        resto = total % lotes_inteiros
    
    dados = []

    if cristal is not None:
        cristal_restante = cristal
        demerara_restante = demerara if demerara is not None else 0

        if not tem_meio_lote:
            for i in range(lotes_inteiros):
                lote_atual = tamanho_lote + (resto if i == 0 else 0)
                
                if cristal_restante > 0:
                    if cristal_restante >= lote_atual:
                        dados.append([f"Lote {i+1}", f"12*{lote_atual//12}+{lote_atual%12}", "0", lote_atual])
                        cristal_restante -= lote_atual
                    else:
                        demerara_no_lote = lote_atual - cristal_restante
                        dados.append([f"Lote {i+1}", 
                                    f"12*{cristal_restante//12}+{cristal_restante%12}",
                                    f"12*{demerara_no_lote//12}+{demerara_no_lote%12}", 
                                    lote_atual])
                        cristal_restante = 0
                        demerara_restante -= demerara_no_lote
                else:
                    dados.append([f"Lote {i+1}", "0", f"12*{lote_atual//12}+{lote_atual%12}", lote_atual])
                    demerara_restante -= lote_atual
        else:
            for i in range(lotes_inteiros + 1):
                if i < lotes_inteiros:
                    lote_atual = tamanho_lote
                    lote_nome = f"Lote {i+1}"
                else:
                    lote_atual = resto
                    lote_nome = "Meio lote"

                if cristal_restante > 0:
                    if cristal_restante >= lote_atual:
                        dados.append([lote_nome, f"12*{lote_atual//12}+{lote_atual%12}", "0", lote_atual])
                        cristal_restante -= lote_atual
                    else:
                        demerara_no_lote = lote_atual - cristal_restante
                        dados.append([lote_nome, 
                                    f"12*{cristal_restante//12}+{cristal_restante%12}",
                                    f"12*{demerara_no_lote//12}+{demerara_no_lote%12}" if i < lotes_inteiros else f"6*{demerara_no_lote//6}+{demerara_no_lote%6}", 
                                    lote_atual])
                        cristal_restante = 0
                        demerara_restante -= demerara_no_lote
                else:
                    dados.append([lote_nome, "0", 
                                f"12*{lote_atual//12}+{lote_atual%12}" if i < lotes_inteiros else f"6*{lote_atual//6}+{lote_atual%6}", 
                                lote_atual])
                    demerara_restante -= lote_atual

        total_calculado = sum([row[3] for row in dados])
        if total_calculado == total and (cristal - cristal_restante) == cristal and (demerara - demerara_restante) == demerara:
            st.success(f"✓ Distribuição correta! Total: {total_calculado}")
        else:
            st.error(f"ERRO! Faltou distribuir: Cristal: {cristal_restante}/{cristal} | Demerara: {demerara_restante}/{demerara}")

        df = pd.DataFrame(dados, columns=["Lote", "Cristal", "Demerara", "Total"])
    else:
        if not tem_meio_lote:
            base = total // lotes_inteiros
            resto = total % lotes_inteiros
            dados.append(["Lote 1", f"12*{(base + resto)//12}+{(base + resto)%12}", base + resto])
            for i in range(1, lotes_inteiros):
                dados.append([f"Lote {i+1}", f"12*{base//12}+{base%12}", base])
        else:
            base = int(total / (lotes_inteiros + 0.5))
            resto = total - (base * lotes_inteiros)
            for i in range(lotes_inteiros):
                dados.append([f"Lote {i+1}", f"12*{base//12}+{base%12}", base])
            dados.append(["Meio lote", f"6*{resto//6}+{resto%6}", resto])

        df = pd.DataFrame(dados, columns=["Lote", "Lastro x Altura", "Total"])

    st.write(df.to_html(index=False), unsafe_allow_html=True)

def calcular_sacos(total_sacos, num_lotes_sacos):
    lotes_inteiros = int(num_lotes_sacos)
    tem_meio_lote = num_lotes_sacos % 1 != 0
    
    if tem_meio_lote:
        tamanho_lote = int(total_sacos / (lotes_inteiros + 0.5))
        resto = total_sacos - (lotes_inteiros * tamanho_lote)
    else:
        tamanho_lote = total_sacos // lotes_inteiros
        resto = total_sacos % lotes_inteiros
    
    dados = []

    if not tem_meio_lote:
        dados.append(["Lote 1", f"5*{(tamanho_lote + resto)//5}+{(tamanho_lote + resto)%5}", tamanho_lote + resto])
        for i in range(1, lotes_inteiros):
            dados.append([f"Lote {i+1}", f"5*{tamanho_lote//5}+{tamanho_lote%5}", tamanho_lote])
    else:
        for i in range(lotes_inteiros):
            dados.append([f"Lote {i+1}", f"5*{tamanho_lote//5}+{tamanho_lote%5}", tamanho_lote])
        dados.append(["Meio lote", f"5*{resto//5}+{resto%5}", resto])

    df = pd.DataFrame(dados, columns=["Lote", "Lastro x Altura", "Total"])
    st.write(df.to_html(index=False), unsafe_allow_html=True)

# Interface para aparecer fardo cristal + demerara, so cristal e sacaria
tab1, tab2, tab3 = st.tabs(["Fardo Cristal + Demerara", "Apenas Fardos", "Sacaria"])

with tab1:
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col1:
        st.subheader("Calcular carga")
        total_fardo = st.number_input("Total:", min_value=1, step=1, value=1070, key="total_fardo")
        lotes_fardo = st.number_input("Nº Lotes (use ,5 para meia):", min_value=0.5, step=0.5, value=10.5, key="lotes_fardo")
        cristal = st.number_input("Cristal:", min_value=0, step=1, value=500, key="cristal")
        demerara = st.number_input("Demerara:", min_value=0, step=1, value=570, key="demerara")
        
        if st.button("Calcular Fardo", key="btn_fardo"):
            if (cristal + demerara) != total_fardo:
                st.error("A quantidade de fardo informada nao bate com a soma total da carga, verifique a quantidade de cristal e demerara!")
            else:
                with col2:
                    calcular_distribuicao_fardos(total_fardo, lotes_fardo, cristal, demerara)
    
    with col3:
        st.subheader("Informações Adicionais:")
        data1 = st.date_input("Date:", value=date.today(), format="DD/MM/YYYY", key="data1")
        placa1 = st.text_input("Placa do caminhão:", key="placa1")
        observacao1 = st.text_area("Observações:", height=100, key="observacao1")

with tab2:
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col1:
        st.subheader("Calcular carga")
        total_cristal = st.number_input("Total de Fardos:", min_value=1, step=1, value=1070, key="total_cristal")
        lotes_cristal = st.number_input("Nº Lotes (use ,5 para meia):", min_value=0.5, step=0.5, value=10.5, key="lotes_cristal")
        
        if st.button("Calcular Fardos Cristal", key="btn_cristal"):
            with col2:
                calcular_distribuicao_fardos(total_cristal, lotes_cristal)
    
    with col3:
        st.subheader("Informações Adicionais:")
        data2 = st.date_input("Date:", value=date.today(), format="DD/MM/YYYY", key="data2")
        placa2 = st.text_input("Placa do caminhão:", key="placa2")
        observacao2 = st.text_area("Observações:", height=100, key="observacao2")

with tab3:
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col1:
        st.subheader("Calcular carga")
        total_sacos = st.number_input("Total de Sacos:", min_value=1, step=1, value=300, key="total_sacos")
        lotes_sacos = st.number_input("Nº Lotes Sacos:", min_value=0.5, step=0.5, value=11.0, key="lotes_sacos")
        
        if st.button("Calcular Sacos", key="btn_sacos"):
            with col2:
                calcular_sacos(total_sacos, lotes_sacos)
    
    with col3:
        st.subheader("Informações Adicionais:")
        data3 = st.date_input("Data:", value=date.today(), format="DD/MM/YYYY", key="data3")
        placa3 = st.text_input("Placa do caminhão:", key="placa3")
        observacao3 = st.text_area("Observações:", height=100, key="observacao3")

# para finalizar parte do rondapé
st.markdown("""
<hr style="margin-top: 40px; margin-bottom: 10px;">

<div style="text-align: center; color: gray; font-size: 14px;">
    APP Calculadora de Cargas <b>2.0</b> 
</div>
""", unsafe_allow_html=True)
