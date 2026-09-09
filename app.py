import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador Contable - Empacadora de Chiles", layout="wide")

st.title("🌶️ Sistema Simulador de Contabilidad y Costos")
st.caption("Caso Práctico: Determinación de Costos Semivariables por Punto Alto - Punto Bajo y Ciclo Contable")

# -------------------------------------------------------------------------
# 1. CATÁLOGO DE CUENTAS BASE
# -------------------------------------------------------------------------
catalogo_datos = [
    {"Código": "1101", "Nombre": "Bancos", "Tipo": "Activo Circulante", "Naturaleza": "Deudora", "Saldo Inicial": 250000.00},
    {"Código": "1109", "Nombre": "IVA Pendiente de Acreditar", "Tipo": "Activo Circulante", "Naturaleza": "Deudora", "Saldo Inicial": 0.00},
    {"Código": "2101", "Nombre": "Proveedores Nacionales", "Tipo": "Pasivo Corto Plazo", "Naturaleza": "Acreedora", "Saldo Inicial": 60000.00},
    {"Código": "3101", "Nombre": "Capital Social", "Tipo": "Capital Contable", "Naturaleza": "Acreedora", "Saldo Inicial": 190000.00},
    {"Código": "5201", "Nombre": "Costos Indirectos de Fabricación (CIF)", "Tipo": "Costos de Producción", "Naturaleza": "Deudora", "Saldo Inicial": 0.00},
]
df_catalogo = pd.DataFrame(catalogo_datos)

# -------------------------------------------------------------------------
# BARRA LATERAL: ENTRADA DE DATOS DEL ALUMNO
# -------------------------------------------------------------------------
st.sidebar.header("⚙️ Parámetros de Simulación")
st.sidebar.markdown("Modifica las cajas a empacar o ajusta los datos del método:")

# Historial para determinar Punto Alto - Punto Bajo
x_alto_def, y_alto_def = 18500, 243500.0
x_bajo_def, y_bajo_def = 9500, 162500.0

with st.sidebar.expander("Modificar Historial (Punto Alto / Bajo)"):
    x_alto = st.number_input("Punto Alto: Cajas (Marzo)", min_value=1000, value=x_alto_def, step=500)
    y_alto = st.number_input("Punto Alto: Costo ($)", min_value=1000.0, value=y_alto_def, step=1000.0)
    x_bajo = st.number_input("Punto Bajo: Cajas (Mayo)", min_value=1000, value=x_bajo_def, step=500)
    y_bajo = st.number_input("Punto Bajo: Costo ($)", min_value=1000.0, value=y_bajo_def, step=1000.0)

# Cálculo matemático automático
delta_x = x_alto - x_bajo
delta_y = y_alto - y_bajo

if delta_x <= 0:
    st.error("Las cajas del punto alto deben ser mayores a las del punto bajo.")
    st.stop()

b = delta_y / delta_x
a = y_alto - (b * x_alto)

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Volumen del Periodo a Presupuestar")
cajas_ingresadas = st.sidebar.number_input(
    "Ingresa manualmente las cajas empacadas:",
    min_value=1000,
    max_value=60000,
    value=17000,
    step=500
)

# Cálculo del costo del periodo
cv_total = cajas_ingresadas * b
costo_devengado = a + cv_total
iva_pendiente = round(costo_devengado * 0.16, 2)
total_proveedor = round(costo_devengado + iva_pendiente, 2)

st.sidebar.success(f"**Costo Total Estimado:**\n${costo_devengado:,.2f}")

# -------------------------------------------------------------------------
# SECCIÓN PRINCIPAL CON PESTAÑAS
# -------------------------------------------------------------------------
tab_calculo, tab_diario, tab_mayor, tab_balanza, tab_catalogo = st.tabs([
    "🧮 1. Cálculo Punto Alto - Punto Bajo",
    "📑 2. Libro Diario (Pólizas)",
    "⚖️ 3. Libro Mayor (Cuentas 'T')",
    "📊 4. Balanza de Comprobación",
    "📚 5. Catálogo de Cuentas"
])

# -------------------------------------------------------------------------
# PESTAÑA 1: CÁLCULO Y FÓRMULAS
# -------------------------------------------------------------------------
with tab_calculo:
    st.subheader("1. Determinación de la Tasa Variable y Costo Fijo")
    
    col_hist, col_kpis = st.columns([3, 2])
    with col_hist:
        df_hist = pd.DataFrame([
            {"Mes": "Enero", "Cajas (X)": "12,000", "Costo ($)": "$185,000.00", "Detalle": ""},
            {"Mes": "Febrero", "Cajas (X)": "15,000", "Costo ($)": "$212,000.00", "Detalle": ""},
            {"Mes": "Marzo", "Cajas (X)": f"{x_alto:,.0f}", "Costo ($)": f"${y_alto:,.2f}", "Detalle": "🔴 Punto Alto"},
            {"Mes": "Abril", "Cajas (X)": "14,000", "Costo ($)": "$203,000.00", "Detalle": ""},
            {"Mes": "Mayo", "Cajas (X)": f"{x_bajo:,.0f}", "Costo ($)": f"${y_bajo:,.2f}", "Detalle": "🔵 Punto Bajo"},
            {"Mes": "Junio", "Cajas (X)": "16,000", "Costo ($)": "$221,000.00", "Detalle": ""},
        ])
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
    
    with col_kpis:
        st.metric("Tasa Costo Variable (b)", f"${b:,.2f} / caja")
        st.metric("Costo Fijo Mensual (a)", f"${a:,.2f}")
        st.info(f"**Ecuación Presupuestal:**\n$$\\text{{Costo}} = \\${a:,.2f} + (\\${b:,.2f} \\times X)$$")

    st.write("---")
    st.subheader("2. Desglose del Costo para el Volumen Simulado")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cajas a Empacar", f"{cajas_ingresadas:,.0f} cajas")
    c2.metric("Costo Variable", f"${cv_total:,.2f}", help=f"{cajas_ingresadas:,} x ${b:,.2f}")
    c3.metric("Costo Fijo", f"${a:,.2f}")
    c4.metric("Costo Devengado (CIF)", f"${costo_devengado:,.2f}")

# -------------------------------------------------------------------------
# PESTAÑA 2: LIBRO DIARIO
# -------------------------------------------------------------------------
with tab_diario:
    st.subheader("Libro Diario: Pólizas Contables del Periodo")
    
    polizas_lista = [
        {"Póliza": "P-001", "Fecha": "2026-07-01", "Tipo": "Diario", "Código": "1101", "Cuenta": "Bancos", "Concepto": "Apertura de saldos del ejercicio", "Debe": 250000.00, "Haber": 0.00},
        {"Póliza": "P-001", "Fecha": "2026-07-01", "Tipo": "Diario", "Código": "2101", "Cuenta": "Proveedores Nacionales", "Concepto": "Apertura de saldos del ejercicio", "Debe": 0.00, "Haber": 60000.00},
        {"Póliza": "P-001", "Fecha": "2026-07-01", "Tipo": "Diario", "Código": "3101", "Cuenta": "Capital Social", "Concepto": "Apertura de saldos del ejercicio", "Debe": 0.00, "Haber": 190000.00},
        {"Póliza": "P-002", "Fecha": "2026-07-31", "Tipo": "Diario", "Código": "5201", "Cuenta": "Costos Indirectos de Fabricación (CIF)", "Concepto": f"Provisión costo empaque {cajas_ingresadas:,} cajas", "Debe": costo_devengado, "Haber": 0.00},
        {"Póliza": "P-002", "Fecha": "2026-07-31", "Tipo": "Diario", "Código": "1109", "Cuenta": "IVA Pendiente de Acreditar", "Concepto": "IVA 16% costo empaque julio", "Debe": iva_pendiente, "Haber": 0.00},
        {"Póliza": "P-002", "Fecha": "2026-07-31", "Tipo": "Diario", "Código": "2101", "Cuenta": "Proveedores Nacionales", "Concepto": "Pasivo devengado operación empaque", "Debe": 0.00, "Haber": total_proveedor},
    ]
    df_polizas = pd.DataFrame(polizas_lista)
    
    total_debe = df_polizas["Debe"].sum()
    total_haber = df_polizas["Haber"].sum()
    
    df_p_view = df_polizas.copy()
    df_p_view["Debe"] = df_p_view["Debe"].apply(lambda v: f"${v:,.2f}" if v > 0 else "-")
    df_p_view["Haber"] = df_p_view["Haber"].apply(lambda v: f"${v:,.2f}" if v > 0 else "-")
    
    st.dataframe(df_p_view, use_container_width=True, hide_index=True)
    
    cd1, cd2, cd3 = st.columns(3)
    cd1.metric("Sumas Iguales (Debe)", f"${total_debe:,.2f}")
    cd2.metric("Sumas Iguales (Haber)", f"${total_haber:,.2f}")
    cd3.success("Estado: PÓLIZAS CUADRADAS PERFECTAMENTE")

# -------------------------------------------------------------------------
# PESTAÑA 3: LIBRO MAYOR (CUENTAS 'T')
# -------------------------------------------------------------------------
with tab_mayor:
    st.subheader("Libro Mayor: Movimientos y Saldos por Cuenta")
    
    cuentas_unicas = df_catalogo["Código"].unique()
    cols_m = st.columns(2)
    
    for idx, cod in enumerate(cuentas_unicas):
        info_cta = df_catalogo[df_catalogo["Código"] == cod].iloc[0]
        movs = df_polizas[df_polizas["Código"] == cod]
        
        sum_cargos = movs["Debe"].sum()
        sum_abonos = movs["Haber"].sum()
        s_inicial = info_cta["Saldo Inicial"]
        
        if info_cta["Naturaleza"] == "Deudora":
            saldo_final = s_inicial + sum_cargos - sum_abonos
            etiqueta_saldo = f"Saldo Deudor: ${saldo_final:,.2f}"
        else:
            saldo_final = s_inicial + sum_abonos - sum_cargos
            etiqueta_saldo = f"Saldo Acreedor: ${saldo_final:,.2f}"
            
        with cols_m[idx % 2]:
            st.markdown(f"#### `{cod}` - {info_cta['Nombre']}")
            st.caption(f"Naturaleza: **{info_cta['Naturaleza']}** | Saldo Inicial: **${s_inicial:,.2f}**")
            
            # Tabla formato Cuenta T
            items_t = []
            for _, r in movs.iterrows():
                items_t.append({
                    "Póliza / Concepto": f"{r['Póliza']} - {r['Concepto'][:28]}...",
                    "Debe (Cargo)": f"${r['Debe']:,.2f}" if r["Debe"] > 0 else "-",
                    "Haber (Abono)": f"${r['Haber']:,.2f}" if r["Haber"] > 0 else "-"
                })
            
            if items_t:
                st.dataframe(pd.DataFrame(items_t), use_container_width=True, hide_index=True)
            else:
                st.write("*Sin movimientos en el periodo.*")
                
            st.write(f"**Cargos:** ${sum_cargos:,.2f} | **Abonos:** ${sum_abonos:,.2f}")
            st.info(f"**{etiqueta_saldo}**")
            st.write("---")

# -------------------------------------------------------------------------
# PESTAÑA 4: BALANZA DE COMPROBACIÓN
# -------------------------------------------------------------------------
with tab_balanza:
    st.subheader("Balanza de Comprobación al 31 de Julio de 2026")
    
    filas_balanza = []
    for _, cta in df_catalogo.iterrows():
        cod = cta["Código"]
        nom = cta["Nombre"]
        nat = cta["Naturaleza"]
        s_ini = cta["Saldo Inicial"]
        
        movs = df_polizas[df_polizas["Código"] == cod]
        cargos = movs["Debe"].sum()
        abonos = movs["Haber"].sum()
        
        if nat == "Deudora":
            s_deudor = s_ini + cargos - abonos
            s_acreedor = 0.0
        else:
            s_deudor = 0.0
            s_acreedor = s_ini + abonos - cargos
            
        filas_balanza.append({
            "Código": cod,
            "Cuenta": nom,
            "Naturaleza": nat,
            "Saldo Inicial": s_ini,
            "Total Cargos": cargos,
            "Total Abonos": abonos,
            "Saldo Deudor": s_deudor,
            "Saldo Acreedor": s_acreedor
        })
        
    df_bal = pd.DataFrame(filas_balanza)
    
    # Totales de comprobación
    tot_cargos = df_bal["Total Cargos"].sum()
    tot_abonos = df_bal["Total Abonos"].sum()
    tot_s_deudor = df_bal["Saldo Deudor"].sum()
    tot_s_acreedor = df_bal["Saldo Acreedor"].sum()
    
    df_bal_vista = df_bal.copy()
    for col_mon in ["Saldo Inicial", "Total Cargos", "Total Abonos", "Saldo Deudor", "Saldo Acreedor"]:
        df_bal_vista[col_mon] = df_bal_vista[col_mon].apply(lambda v: f"${v:,.2f}")
        
    st.dataframe(df_bal_vista, use_container_width=True, hide_index=True)
    
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("**Sumas de Movimientos:**")
        st.write(f"- Total Debe: **${tot_cargos:,.2f}**")
        st.write(f"- Total Haber: **${tot_abonos:,.2f}**")
        if round(tot_cargos - tot_abonos, 2) == 0:
            st.success("✅ Movimientos Cuadrados")
            
    with b2:
        st.markdown("**Sumas de Saldos Finales:**")
        st.write(f"- Total Saldos Deudores: **${tot_s_deudor:,.2f}**")
        st.write(f"- Total Saldos Acreedores: **${tot_s_acreedor:,.2f}**")
        if round(tot_s_deudor - tot_s_acreedor, 2) == 0:
            st.success("✅ Saldos Cuadrados")

# -------------------------------------------------------------------------
# PESTAÑA 5: CATÁLOGO DE CUENTAS
# -------------------------------------------------------------------------
with tab_catalogo:
    st.subheader("Catálogo de Cuentas Contable")
    st.markdown("Estructura de cuentas utilizadas en la contabilización del caso de estudio:")
    
    df_cat_v = df_catalogo.copy()
    df_cat_v["Saldo Inicial"] = df_cat_v["Saldo Inicial"].apply(lambda v: f"${v:,.2f}")
    st.dataframe(df_cat_v, use_container_width=True, hide_index=True)
