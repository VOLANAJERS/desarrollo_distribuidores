import streamlit as st
import pandas as pd
import numpy as np

num2curr = lambda x: "${:,.0f}".format(x) if x > 0 else "-"+("${:,.0f}".format(x)).replace("-","")
pagado = lambda X, t, d: ( (X*t*(1+t)**d) / (- 1 + (1+t)**d) ) * d

def find_rate(X_con_intereses, X, d):
    pagado = lambda X, t, d: ( (X*t*(1+t)**d) / (- 1 + (1+t)**d) ) * d
    tasas = list(range(1, 147, 1))
    res = []
    for r in tasas:
        r /= 52
        res.append(abs(X_con_intereses - pagado(X,(r/100),d)))
    return tasas[np.argmin(res)]

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
    porc_comision = 0.145
    
    with col1:
        monto_credito_distribuidor = st.number_input("Monto de tu crédito", 
                                             value = 5_000, 
                                             step = 1_000)
    with col2:
        tasa_credito_distribuidor = st.number_input("Tasa asignada a tu crédito", 
                                             value = 100, 
                                             step = 5)
            
    
    
    tasa_semanal = ((tasa_credito_distribuidor / 52)/100)

    intereses = pagado(monto_credito_distribuidor, tasa_semanal, duracion_credito_semanas) - monto_credito_distribuidor
    
    IVA = intereses * 0.16
    
    seguro = costo_seguro(monto_credito_distribuidor, duracion_credito_semanas)
    
    total_a_pagar = monto_credito_distribuidor + intereses + seguro + IVA
    
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    col1.metric("Interes a pagar", num2curr(intereses))
    col2.metric("IVA a pagar", num2curr(IVA))
    col3.metric("Seguro", str(seguro))
    col4.metric("Total a pagar", num2curr(total_a_pagar))
    
    
    col1, col2, col3, col4, col5 = st.columns([0.3,0.3,0.7, 0.4, 0.8])
    col1.write("#")
    col1.write("Si colocas")
    cantidad_creditos_colocar = col2.number_input(label = "",value = 1, step = 1)
    col3.write("#")
    col3.write("créditos con un monto de:")
    monto_medio_a_colocar = col4.number_input(label = "", value = 3000, step = 1000)
    col5.write("#")
    col5.write("c/u durante tu crédito")
    
    monto_medio_a_colocar
    tasa_media_a_colocar = 1.41
    
    pago_a_colocar = pagado(monto_medio_a_colocar, (tasa_media_a_colocar/52) * 1.16, duracion_credito_semanas) + costo_seguro(monto_medio_a_colocar, duracion_credito_semanas)
    comision = (pago_a_colocar / duracion_credito_semanas) * porc_comision * cantidad_creditos_colocar * duracion_credito_semanas
    
    nuevo_total_a_pagar = total_a_pagar - comision
    nuevo_total_a_pagar_intereses = total_a_pagar - comision - IVA - seguro
    nueva_tasa = find_rate(nuevo_total_a_pagar_intereses, monto_credito_distribuidor, duracion_credito_semanas)
    # TODO
    
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    #col1.metric("Comisión durante el crédito", num2curr(comision))
    col1.metric("Intereses con descuento", num2curr(intereses - comision), num2curr(- comision))
    col2.metric("Nuevo total a pagar", num2curr(nuevo_total_a_pagar ), num2curr(nuevo_total_a_pagar - total_a_pagar))
    col3.metric("Nueva tasa", f"{nueva_tasa}%",f"{nueva_tasa - tasa_credito_distribuidor}%")
    
