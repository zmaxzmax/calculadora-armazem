import streamlit as st
import pandas as pd

# nesta aba iniciarei as configuraçoes de pagina 
st.set_page_config(page_title="calculadora armazem", layout="centered")

# Funções de cálculo ( parte de distribuição)
def calcular_distribuicao_fardos(total, num_lotes, cristal=None, demerara=None):
    lotes_inteiros = int(num_lotes)
    tem_meio_lote = num_lotes % 1 != 0
    
    if tem_meio_lote:
        tamanho_lote = int(total // (lotes_inteiros + 0.5))
        resto = total - (lotes_inteiros * tamanho_lote)
    else:
        # aqui e para somas de lotes inteiros 
        tamanho_lote = total // lotes_inteiros
        resto = total % lotes_inteiros
    
    dados = []
    
    if cristal is not None:  # Caso Cristal + Demerara
        cristal_restante = cristal
        demerara_restante = demerara if demerara is not None else 0
        
        if not tem_meio_lote:
            #(distribuição para lotes inteiros)
            valor_base = total // lotes_inteiros
            resto = total % lotes_inteiros
            
            # Distribui primeiro todo o cristal
            for i in range(lotes_inteiros):
                # Primeiro lote leva o resto de fardos , a sobra 
                if i == 0:
                    lote_atual = valor_base + resto
                else:
                    lote_atual = valor_base
                
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
            # Lógica para meia ( vou chamar de meio lote)
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
        
        # verificando as informaçoes finais 
        total_calculado = sum([row[3] for row in dados])
        cristal_distribuido = cristal - cristal_restante
        demerara_distribuido = (demerara - demerara_restante) if demerara is not None else 0
        
        if total_calculado == total and cristal_distribuido == cristal and (demerara is None or demerara_distribuido == demerara):
            st.success(f"✓ Distribuição correta! Total: {total_calculado}")
        else:
            st.error(f"ERRO! Faltou distribuir: Cristal: {cristal_restante}/{cristal} | Demerara: {demerara_restante}/{demerara}")
        
        df = pd.DataFrame(dados, columns=["Lote", "Cristal", "Demerara", "Total"])
    
    else:  # Caso de soma para apenas fardo cristal de 30kg
        if not tem_meio_lote:
            dados.append(["Lote 1", f"12*{(tamanho_lote + resto)//12}+{(tamanho_lote + resto)%12}", tamanho_lote + resto])
            for i in range(1, lotes_inteiros):
                dados.append([f"Lote {i+1}", f"12*{tamanho_lote//12}+{tamanho_lote%12}", tamanho_lote])
        else:
            for i in range(lotes_inteiros):
                dados.append([f"Lote {i+1}", f"12*{tamanho_lote//12}+{tamanho_lote%12}", tamanho_lote])
            dados.append(["Meio lote", f"6*{resto//6}+{resto%6}", resto])
        
        df = pd.DataFrame(dados, columns=["Lote", "Fardos (12)", "Total"])
    
    st.write(df.to_html(index=False), unsafe_allow_html=True)

# funçoes 
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

# interface e titalo do app calculadora armazém
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

# codigo alterado, corrigindo erros de calculos, vou considerar ainda essa como a versão 1.0 , data da ultima alteração 16/04/2025. para executar : streamlit run app.py. esse sistema ja esta no meu repositorio da git telefone (11 9 99454425 )