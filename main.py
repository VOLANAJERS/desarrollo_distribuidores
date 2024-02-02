import streamlit as st
import pandas as pd
import numpy as np

num2curr = lambda x: "${:,.0f}".format(x) if x > 0 else "-"+("${:,.0f}".format(x)).replace("-","")
pagado = lambda X, t, d: ( (X*t*(1+t)**d) / (- 1 + (1+t)**d) ) * d

def costo_seguro(X, d):
    seguros = {4_000 : 26, 21_000 : 29, 51_000 : 30, np.inf: 31}

    ingreso_seguro = 0.0

    key_ant = 0
    for s in seguros.keys():
        if X < s and X > key_ant:
            ingreso_seguro = seguros[s]

        key_ant = s
    
    return ingreso_seguro * d

with st.sidebar:
    
    page = st.selectbox(
    'Selecciona la página',
    ('Desarrollo de distribuidores',))

    
if page == 'Desarrollo de distribuidores':
    
    st.title("Desarrollo de distribuidores")
    col1, col2 = st.columns([1,1])
    duracion_credito_semanas = 16
    
    with col1:
        monto_credito_distribuidor = st.number_input("Monto de tu crédito", 
                                             value = 5_000, 
                                             step = 1_000)
    with col2:
        tasa_credito_distribuidor = st.number_input("Tasa asignada a tu crédito", 
                                             value = 100, 
                                             step = 5)
            
    
    
    tasa_semanal = ((tasa_credito_distribuidor / 52)/100)*1.16

    intereses = pagado(monto_credito_distribuidor, tasa_semanal, duracion_credito_semanas) - monto_credito_distribuidor
    
    IVA = intereses * 0.16
    
    seguro = costo_seguro(monto_credito_distribuidor, duracion_credito_semanas)
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    col1.metric("Interes a pagar", num2curr(intereses))
    col2.metric("IVA a pagar", num2curr(IVA))
    col3.metric("Seguro", str(seguro))
    col4.metric("Total a pagar", num2curr(monto_credito_distribuidor + IVA + intereses + seguro))
    
    
    col1, col2, col3, col4 = st.columns([0.3,0.5,1.5,0.1])
    col1.write("#")
    col1.write("Si coloco")
    col2.number_input(label = "",value = 1, step = 1)
    col3.write("#")
    col3.write("créditos durante la duración del mío")
