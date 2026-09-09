import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador de Costos - Empacadora", layout="wide")

st.title("🌽 Empacadora de Chiles")
st.subheader("Determinación de Costos Semivariables: Método Punto Alto - Punto Bajo")

st.markdown("""
Esta herramienta analiza los costos mixtos de operación (refrigeración y líneas de empaque), 
desglosa las fórmulas de estimación paso a paso y genera automáticamente la póliza de diario correspondiente.
""")

# -------------------------------------------------------------------------
# 1. DATOS HISTÓRICOS DEL EJERCICIO
# -------------------------------------------------------------------------
st.markdown("### 1. Historial de Operación (Primer Semestre)")

datos_hist = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
    "Cajas Empacadas (X)": [12000, 15000, 18500, 14000, 9500, 16000],
    "Costo de Operación (Y)": [185000.0, 212000.0, 243500.0, 203000.0, 162500.0, 221000.0]
}
df_hist = pd.DataFrame(datos_hist)

# Identificación automática de puntos
idx_alto = df_hist["Cajas Empacadas (X)"].idxmax()
idx_bajo = df_hist["Cajas Empacadas (X)"].idxmin()

x_alto = df_hist.loc[idx_alto, "Cajas Empacadas (X)"]
y_alto = df_hist.loc[idx_alto, "Costo de Operación (Y)"]
mes_alto = df_hist.loc[idx_alto, "Mes"]

x_bajo = df_hist.loc[idx_bajo, "Cajas Empacadas (X)"]
y_bajo = df_hist.loc[idx_bajo, "Costo de Operación (Y)"]
mes_bajo = df_hist.loc[idx_bajo, "Mes"]

# Formato visual de la tabla
df_mostrar = df_hist.copy()
df_mostrar["Cajas Empacadas (X)"] = df_mostrar["Cajas Empacadas (X)"].apply(lambda v: f"{v:,.0f} cajas")
df_mostrar["Costo de Operación (Y)"] = df_mostrar["Costo de Operación (Y)"].apply(lambda v: f"${v:,.2f}")
df_mostrar["Observación"] = ""
df_mostrar.loc[idx_alto, "Observación"] = "🔴 Punto Alto (Mayor Actividad)"
df_mostrar.loc[idx_bajo, "Observación"] = "🔵 Punto Bajo (Menor Actividad)"

col_tbl, col_kpi = st.columns([3, 2])
with col_tbl:
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

with col_kpi:
    st.info(f"**Punto Alto ({mes_alto}):** {x_alto:,.0f} cajas | ${y_alto:,.2f}")
    st.warning(f"**Punto Bajo ({mes_bajo}):** {x_bajo:,.0f} cajas | ${y_bajo:,.2f}")

st.write("---")

# -------------------------------------------------------------------------
# 2. FÓRMULAS Y CÁLCULO PASO A PASO
# -------------------------------------------------------------------------
st.markdown("### 2. Memoria de Cálculo y Fórmulas")

delta_x = x_alto - x_bajo
delta_y = y_alto - y_bajo
b = delta_y / delta_x
a = y_alto - (b * x_alto)

c_paso1, c_paso2 = st.columns(2)

with c_paso1:
    st.markdown("#### Paso 1: Tasa de Costo Variable Unitario ($b$)")
    st.latex(r"b = \frac{\Delta Y}{\Delta X} = \frac{\text{Costo Alto} - \text{Costo Bajo}}{\text{Actividad Alta} - \text{Actividad Baja}}")
    st.latex(rf"b = \frac{{{y_alto:,.2f} - {y_bajo:,.2f}}}{{{x_alto:,.0f} - {x_bajo:,.0f}}} = \frac{{{delta_y:,.2f}}}{{{delta_x:,.0f}}} = \mathbf{{\${b:,.2f}\text{{ por caja}}}}")

with c_paso2:
    st.markdown("#### Paso 2: Determinación del Costo Fijo Mensual ($a$)")
    st.latex(r"a = Y - b(X)")
    st.latex(rf"a = {y_alto:,.2f} - ({b:,.2f} \times {x_alto:,.0f})")
    st.latex(rf"a = {y_alto:,.2f} - {b * x_alto:,.2f} = \mathbf{{\${a:,.2f}\text{{ mensuales}}}}")

st.success(f"**Ecuación Presupuestal Obtenida:** $\\text{{Costo Total}} = \\${a:,.2f} + \\${b:,.2f}(X)$")

st.write("---")

# -------------------------------------------------------------------------
# 3. SIMULADOR INTERACTIVO PARA EL PERIODO
# -------------------------------------------------------------------------
st.markdown("### 3. Simulación de Producción del Periodo")

cajas = st.slider("Selecciona las cajas a empacar en el mes presupuestado:", 
                  min_value=5000, max_value=30000, value=17000, step=500)

cv_total = cajas * b
costo_total = a + cv_total
iva = costo_total * 0.16
total_pasivo = costo_total + iva

m1, m2, m3 = st.columns(3)
m1.metric("Costo Variable Estimado", f"${cv_total:,.2f}", help=f"{cajas:,} cajas x ${b:,.2f}")
m2.metric("Costo Fijo Mensual", f"${a:,.2f}", help="Componente fijo de refrigeración y planta")
m3.metric("Costo Total Devengado (Sin IVA)", f"${costo_total:,.2f}")

st.write("---")

# -------------------------------------------------------------------------
# 4. PÓLIZA CONTABLE GENERADA
# -------------------------------------------------------------------------
st.markdown("### 4. Asiento Contable en Libro Diario")

linea_separador = "=" * 88
linea_sub = "-" * 88

poliza_lineas = [
    linea_separador,
    "PÓLIZA DE DIARIO | Ref: PROV-EMP-SIM | Aplicación: Costos Indirectos de Fabricación",
    linea_sub,
    f"{'Código':<8} {'Nombre de la Cuenta':<45} {'Debe (Cargo)':>16} {'Haber (Abono)':>16}",
    linea_sub,
    f"5201     Costos Indirectos de Fabricación (CIF)       ${costo_total:>14,.2f}",
    f"         * Porción Variable ({cajas:,} cajas @ ${b:,.2f}): ${cv_total:>12,.2f}",
    f"         * Porción Fija de conservación:             ${a:>12,.2f}",
    f"1109     IVA Pendiente de Acreditar                   ${iva:>14,.2f}",
    f"2101     Proveedores Nacionales                                        ${total_pasivo:>14,.2f}",
    linea_sub,
    f"{'SUMAS IGUALES:':<54} ${total_pasivo:>14,.2f}  ${total_pasivo:>14,.2f}",
    linea_separador
]

st.code("\n".join(poliza_lineas), language="text")
