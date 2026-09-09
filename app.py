Python
import streamlit as st

st.set_page_config(page_title="Simulador de Costos", layout="centered")

st.title("🌽 Empacadora de Chiles")
st.subheader("Método de Costos: Punto Alto y Punto Bajo")

st.markdown("""
Esta herramienta interactiva te permite simular el costo de operación de los cuartos fríos y líneas de empaque, 
separando la porción fija y variable para generar la póliza contable de diario.
""")

# Parámetros fijos obtenidos del método
cf = 77000.0   # Costo fijo mensual
cv_unit = 9.0  # Costo variable por caja

col_a, col_b = st.columns(2)
col_a.metric("Costo Fijo Mensual", f"${cf:,.2f} MXN")
col_b.metric("Costo Variable Unitario", f"${cv_unit:,.2f} / caja")

st.write("---")
st.subheader("Simulación del Periodo")

# Deslizador interactivo para los alumnos
cajas = st.slider("Selecciona las cajas empacadas en el mes:", min_value=5000, max_value=25000, value=17000, step=500)

cv_total = cajas * cv_unit
costo_total = cf + cv_total
iva = costo_total * 0.16
total_pasivo = costo_total + iva

st.write(f"Para un volumen de **{cajas:,} cajas**, los costos resultantes son:")

c1, c2, c3 = st.columns(3)
c1.metric("Costo Variable Total", f"${cv_total:,.2f}")
c2.metric("Costo Total Devengado", f"${costo_total:,.2f}")
c3.metric("Total Pasivo (+16% IVA)", f"${total_pasivo:,.2f}")

st.write("---")
st.subheader("Póliza de Diario Generada")

linea_separador = "=" * 85
linea_sub = "-" * 85

poliza_lineas = [
    linea_separador,
    "PÓLIZA DE DIARIO | Tipo: Diario | Ref: PROV-EMP-SIM",
    linea_sub,
    f"{'Código':<8} {'Nombre de la Cuenta':<45} {'Debe (Cargo)':>15} {'Haber (Abono)':>15}",
    linea_sub,
    f"5201     Costos Indirectos de Fabricación (CIF)       ${costo_total:>13,.2f}",
    f"         * Variable ({cajas:,} cajas @ ${cv_unit:,.2f}): ${cv_total:>11,.2f}",
    f"         * Fijo mensual:                            ${cf:>11,.2f}",
    f"1109     IVA Pendiente de Acreditar                   ${iva:>13,.2f}",
    f"2101     Proveedores Nacionales                                       ${total_pasivo:>13,.2f}",
    linea_sub,
    f"{'SUMAS IGUALES:':<54} ${total_pasivo:>13,.2f} ${total_pasivo:>13,.2f}",
    linea_separador
]

st.code("\n".join(poliza_lineas), language="text")
