import streamlit as st
import pandas as pd

# Configuração da pagina 
st.set_page_config(page_title="calculadora armazem", layout="centered")

# Funções de cálculo (aqui faço as funçoes)
def calcular_distribuicao_fardos(total, num_lotes, cristal=None, demerara=None):
    lotes_inteiros = int(num_lotes)
    tem_meio_lote = num_lotes % 1 != 0
    
    if tem_meio_lote:
        tamanho_lote = int(total // (lotes_inteiros + 0.5))
        resto = total - (lotes_inteiros * tamanho_lote)
    else:
        tamanho_lote = total // lotes_inteiros
        resto = total % lotes_inteiros
    
    primeiro_lote = tamanho_lote + (resto if not tem_meio_lote else 0)
    outros_lotes = tamanho_lote
    
    dados = []
    
    if cristal is not None:  # Caso Cristal + Demerara
        cristal_restante = cristal
        
        if not tem_meio_lote and cristal_restante >= primeiro_lote:
            dados.append(["Lote 1", f"12*{primeiro_lote//12}+{primeiro_lote%12}", "0", primeiro_lote])
            cristal_restante -= primeiro_lote
        elif not tem_meio_lote:
            demerara_lote1 = primeiro_lote - cristal_restante
            dados.append(["Lote 1", 
                         f"12*{cristal_restante//12}+{cristal_restante%12}", 
                         f"12*{demerara_lote1//12}+{demerara_lote1%12}", 
                         primeiro_lote])
            cristal_restante = 0
        
        for i in range(1 if tem_meio_lote else 0, lotes_inteiros + (1 if tem_meio_lote else 0)):
            if cristal_restante <= 0:
                dados.append([f"Lote {i+1}" if not tem_meio_lote else f"Lote {i}", 
                             "0", 
                             f"12*{outros_lotes//12}+{outros_lotes%12}", 
                             outros_lotes])
            else:
                if cristal_restante >= outros_lotes:
                    dados.append([f"Lote {i+1}" if not tem_meio_lote else f"Lote {i}", 
                                 f"12*{outros_lotes//12}+{outros_lotes%12}", 
                                 "0", 
                                 outros_lotes])
                    cristal_restante -= outros_lotes
                else:
                    demerara_lote = outros_lotes - cristal_restante
                    dados.append([f"Lote {i+1}" if not tem_meio_lote else f"Lote {i}", 
                                 f"12*{cristal_restante//12}+{cristal_restante%12}",
                                 f"12*{demerara_lote//12}+{demerara_lote%12}", 
                                 outros_lotes])
                    cristal_restante = 0
        
        if tem_meio_lote:
            dados.append(["Meio lote", "0", f"6*{resto//6}+{resto%6}", resto])
        
        demerara_distribuido = total - (cristal - cristal_restante)
        if cristal_restante == 0 and demerara_distribuido == demerara:
            st.success(f"✓ CERTO! Cristal: {cristal} | Demerara: {demerara} | Total: {total}")
        else:
            st.error(f"ERRO! Cristal: {cristal-cristal_restante}/{cristal} | Demerara: {demerara_distribuido}/{demerara}")
        
        df = pd.DataFrame(dados, columns=["Lote", "Cristal", "Demerara", "Total"])
    
    else:  # Caso apenas Fardos Cristal (nesse caso so pra calculo do fardo cristal)
        if not tem_meio_lote:
            dados.append(["Lote 1", f"12*{(primeiro_lote//12)}+{primeiro_lote%12}", primeiro_lote])
            for i in range(1, lotes_inteiros):
                dados.append([f"Lote {i+1}", f"12*{outros_lotes//12}+{outros_lotes%12}", outros_lotes])
        else:
            for i in range(lotes_inteiros):
                dados.append([f"Lote {i+1}", f"12*{outros_lotes//12}+{outros_lotes%12}", outros_lotes])
            dados.append(["Meio lote", f"6*{resto//6}+{resto%6}", resto])
        
        df = pd.DataFrame(dados, columns=["Lote", "Fardos (12)", "Total"])
    
    st.write(df.to_html(index=False), unsafe_allow_html=True)

def calcular_sacos(total_sacos, num_lotes_sacos):
    lotes_inteiros = int(num_lotes_sacos)
    tem_meio_lote = num_lotes_sacos % 1 != 0
    
    if tem_meio_lote:
        tamanho_lote = int(total_sacos // (lotes_inteiros + 0.5))
        resto = total_sacos - (lotes_inteiros * tamanho_lote)
    else:
        tamanho_lote = total_sacos // lotes_inteiros
        resto = total_sacos % lotes_inteiros
    
    primeiro_lote = tamanho_lote + (resto if not tem_meio_lote else 0)
    outros_lotes = tamanho_lote
    
    dados = []
    
    if not tem_meio_lote:
        dados.append(["Lote 1", f"5*{(primeiro_lote//5)}+{primeiro_lote%5}", primeiro_lote])
        for i in range(1, lotes_inteiros):
            dados.append([f"Lote {i+1}", f"5*{outros_lotes//5}+{outros_lotes%5}", outros_lotes])
    else:
        for i in range(lotes_inteiros):
            dados.append([f"Lote {i+1}", f"5*{outros_lotes//5}+{outros_lotes%5}", outros_lotes])
        dados.append(["Meio lote", f"5*{resto//5}+{resto%5}", resto])
    
    df = pd.DataFrame(dados, columns=["Lote", "Sacos (5)", "Total"])
    st.write(df.to_html(index=False), unsafe_allow_html=True)

# qui vou da inicio com o titalo ( talvez eu mude depois )
st.title("🚚 CALCULADORA DE CARGAS ARMAZÉM 2025")

tab1, tab2, tab3 = st.tabs(["Fardo Cristal + Demerara", "Apenas Fardos Cristal", "Apenas Sacos"])

with tab1:
    st.header("Cálculo Fardo Cristal + Demerara")
    total_fardo = st.number_input("Total:", min_value=1, step=1, value=1070, key="total_fardo")
    lotes_fardo = st.number_input("Nº Lotes:", min_value=0.5, step=0.5, value=10.5, key="lotes_fardo")
    cristal = st.number_input("Cristal:", min_value=0, step=1, value=500, key="cristal")
    demerara = st.number_input("Demerara:", min_value=0, step=1, value=570, key="demerara")
    
    if st.button("Calcular Fardo", key="btn_fardo"):
        if (cristal + demerara) != total_fardo:
            st.error("Soma incorreta!")
        else:
            calcular_distribuicao_fardos(total_fardo, lotes_fardo, cristal, demerara)

with tab2:
    st.header("Cálculo Apenas Fardos Cristal")
    total_cristal = st.number_input("Total Fardos:", min_value=1, step=1, value=1070, key="total_cristal")
    lotes_cristal = st.number_input("Nº Lotes:", min_value=0.5, step=0.5, value=10.5, key="lotes_cristal")
    
    if st.button("Calcular Fardos Cristal", key="btn_cristal"):
        calcular_distribuicao_fardos(total_cristal, lotes_cristal)

with tab3:
    st.header("Cálculo Apenas Sacos")
    total_sacos = st.number_input("Total Sacos:", min_value=1, step=1, value=300, key="total_sacos")
    lotes_sacos = st.number_input("Nº Lotes Sacos:", min_value=0.5, step=0.5, value=11.0, key="lotes_sacos")
    
    if st.button("Calcular Sacos", key="btn_sacos"):
        calcular_sacos(total_sacos, lotes_sacos)

st.markdown("---")
st.markdown("**Desenvolvido por Lucas Cardoso dia 15/04/2025**")
st.markdown("Sistema de calculo de cargas armazém agrovale 2025/2026")

#sistema simples concluido por mim lucas cardoso de freitas na data do dia 15 de abril de 2025 vou considerara esse app como a versao 1.0 depois posso estar fazendo alguns ajustes e melhorando o codigo. lembrando que desemvolvi todo em streamlit execuçao= streamlit run app.py