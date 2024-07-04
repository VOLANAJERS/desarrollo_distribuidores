import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

num2curr = lambda x: "${:,.0f}".format(x) if x > -0.00000000001 else "-"+("${:,.0f}".format(x)).replace("-","")
pagado = lambda X, t, d: ( (X*t*(1+t)**d) / (- 1 + (1+t)**d) ) * d

def getGanancias(monto_credito_distribuidor, tasa_credito_distribuidor, monto_medio_a_colocar):

    duracion_credito_semanas = 16
    porc_comision = 0.145

    pago_iterar = []
    ganancia_iterar = []

    for cantidad_creditos_colocar in range(11): # variable

        tasa_semanal = ((tasa_credito_distribuidor / 52)/100)

        intereses = pagado(monto_credito_distribuidor, tasa_semanal, duracion_credito_semanas) - monto_credito_distribuidor

        IVA = intereses * 0.16

        seguro = costo_seguro(monto_credito_distribuidor, duracion_credito_semanas)

        total_a_pagar = monto_credito_distribuidor + intereses + seguro + IVA

        
        tasa_media_a_colocar = 1.41

        pago_a_colocar = pagado(monto_medio_a_colocar, (tasa_media_a_colocar/52) * 1.16, duracion_credito_semanas) + costo_seguro(monto_medio_a_colocar, duracion_credito_semanas)
        comision = (pago_a_colocar / duracion_credito_semanas) * porc_comision * cantidad_creditos_colocar * duracion_credito_semanas

        nuevo_total_a_pagar_intereses = total_a_pagar - comision - IVA - seguro

        nuevo_intereses = intereses - comision

        nuevo_IVA = nuevo_intereses * 0.16

        nuevo_total_a_pagar = monto_credito_distribuidor + nuevo_intereses + seguro + nuevo_IVA #total_a_pagar - comision

        nueva_tasa = find_rate(nuevo_total_a_pagar_intereses, monto_credito_distribuidor, duracion_credito_semanas)

        nueva_tasa = nueva_tasa if nuevo_intereses > 0 else 0

        nuevo_intereses = nuevo_intereses if nuevo_intereses > 0 else 0

        pago_iterar.append(nuevo_total_a_pagar)

        diff = (monto_credito_distribuidor - nuevo_total_a_pagar)
        ganancia_iterar.append(diff if diff > 0 else 0)
        
        #=====================================
    ganancia_iterar = np.array(ganancia_iterar)
    ganancia_iterar[ganancia_iterar >= monto_credito_distribuidor] = monto_credito_distribuidor
    
    fig = go.Figure()

    fig.add_trace(
    go.Bar(x=np.array(range(len(pago_iterar))), 
           y=pago_iterar, name="Total a pagar",
          marker = dict(color = '#FFA07A'))
    )

    fig.add_trace(
    go.Bar(x=np.array(range(len(pago_iterar))), 
           y=ganancia_iterar, name="Ganancia para ti",
          marker=dict(color='#90EE90'))
    )


    fig.add_shape(type='line',
                  x0 = -1, x1 = len(pago_iterar),
                  y0 = monto_credito_distribuidor, y1 = monto_credito_distribuidor,
                  line=dict(color='red', width=2, dash = 'dot'), 
                  name="Capital solicitado")
    
    
    
    txt_ganancias = f"A partir de {np.argmax(np.array(ganancia_iterar)>0)} créditos colocados, las ganancias que obtienes de tu valera, \nservirían para pagar los intereses de tu crédito."
    if sum(np.array(ganancia_iterar)>0) == 0:
        txt_ganancias = "Incrementa el monto promedio de tus colocaciones ¡y verás como comienzas a ganar!"

    fig.update_layout(title=f'Pago final con base en créditos colocados',
                       xaxis_title='Créditos colocados',
                       xaxis=dict(tickmode='array', tickvals=list(range(len(pago_iterar))), showticklabels=True, showline=True),
                       yaxis_title='Monto a pagar',
                     showlegend=True,
                      barmode='stack',
                     annotations=[dict(x=-0.04, y=1.1, 
                                       text=f"{num2curr(monto_credito_distribuidor)} capital solicitado a una tasa de {tasa_credito_distribuidor}%", 
                                       showarrow=False, xref="paper", yref="paper", font=dict(size=10)),
                                 
                                  dict(x=-0.04, y=-0.3, 
                                       text=txt_ganancias, 
                                       showarrow=False, xref="paper", yref="paper", font=dict(size=13))
                                 ])
    return fig

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
    st.image("./logo_volana.png")
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
    
    tasa_media_a_colocar = 1.41
    
    pago_a_colocar = pagado(monto_medio_a_colocar, (tasa_media_a_colocar/52) * 1.16, duracion_credito_semanas) + costo_seguro(monto_medio_a_colocar, duracion_credito_semanas)
    comision = (pago_a_colocar / duracion_credito_semanas) * porc_comision * cantidad_creditos_colocar * duracion_credito_semanas
    
    nuevo_total_a_pagar_intereses = total_a_pagar - comision - IVA - seguro
    
    nuevo_intereses = intereses - comision
    
    nuevo_IVA = nuevo_intereses * 0.16
    
    nuevo_total_a_pagar = monto_credito_distribuidor + nuevo_intereses + seguro + nuevo_IVA #total_a_pagar - comision
    
    nueva_tasa = find_rate(nuevo_total_a_pagar_intereses, monto_credito_distribuidor, duracion_credito_semanas)
    
    nueva_tasa = nueva_tasa if nuevo_intereses > 0 else 0
    
    nuevo_intereses = nuevo_intereses if nuevo_intereses > 0 else 0
    
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    #col1.metric("Comisión durante el crédito", num2curr(comision))
    col1.metric("Intereses con descuento", num2curr(nuevo_intereses), num2curr(max(-comision, -intereses)))
    col2.metric("Nuevo total a pagar", num2curr(nuevo_total_a_pagar ), num2curr(nuevo_total_a_pagar - total_a_pagar))
    col3.metric("Nueva tasa", f"{nueva_tasa}%",f"{nueva_tasa - tasa_credito_distribuidor}%")
    
    
    st.plotly_chart(getGanancias(monto_credito_distribuidor, tasa_credito_distribuidor, monto_medio_a_colocar))
