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

poliza_texto = f"""
