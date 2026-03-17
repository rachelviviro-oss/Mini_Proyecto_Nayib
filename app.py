"""
Dashboard SuperTienda CR
========================

Este archivo contiene las funciones de calculo y los 6 pasos
que usted debe completar para construir un dashboard con Streamlit.

Para ejecutar: streamlit run app.py
Dependencias: pip install streamlit pandas

Archivos necesarios:
- app.py (este archivo)
- supertienda_cr.csv (dataset proporcionado, debe estar en la misma carpeta)
"""

import streamlit as st
import pandas as pd


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                                                                         ║
# ║                 SECCION DE CALCULOS — NO MODIFICAR                      ║
# ║                                                                         ║
# ║  Aqui se encuentran las funciones que usted va a utilizar en los        ║
# ║  pasos de mas abajo. Lea los comentarios de cada una para entender      ║
# ║  que retorna y como usarla.                                             ║
# ║                                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝


def calcular_resumen(df: pd.DataFrame) -> dict:
    """
    Calcula un resumen general de los datos.

    Retorna un diccionario con:
        "ventas"   -> float, suma total de ventas
        "ganancia" -> float, suma total de ganancia
        "ordenes"  -> int, cantidad de ordenes unicas
    """
    return {
        "ventas": round(df["Ventas"].sum(), 2),
        "ganancia": round(df["Ganancia"].sum(), 2),
        "ordenes": df["ID_Orden"].nunique(),
    }


def ventas_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por mes.

    Retorna un DataFrame con columnas: Año_Mes, Ventas
    Ordenado de manera cronologica.
    """
    df = df.copy()
    df["Año_Mes"] = pd.to_datetime(df["Fecha_Orden"]).dt.to_period("M").astype(str)
    return (
        df.groupby("Año_Mes")["Ventas"].sum()
        .reset_index().sort_values("Año_Mes")
        .round(2)
    )


def ventas_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por categoria de producto.

    Retorna un DataFrame con columnas: Categoria, Ventas
    """
    return (
        df.groupby("Categoria")["Ventas"].sum()
        .reset_index().sort_values("Ventas", ascending=False)
        .round(2)
    )


def ventas_por_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por region geografica.

    Retorna un DataFrame con columnas: Region, Ventas
    """
    return (
        df.groupby("Region")["Ventas"].sum()
        .reset_index().sort_values("Ventas", ascending=False)
        .round(2)
    )


def filtrar_datos(df, años=None, categorias=None, regiones=None):
    """
    Filtra el DataFrame segun los parametros indicados.
    Si un parametro es None, no aplica ese filtro.

    Parametros:
        df: DataFrame original
        años: lista de enteros, por ejemplo [2023, 2024]
        categorias: lista de strings, por ejemplo ["Tecnologia"]
        regiones: lista de strings, por ejemplo ["Central"]

    Retorna un DataFrame filtrado.
    """
    resultado = df.copy()
    if años:
        resultado = resultado[resultado["Año"].isin(años)]
    if categorias:
        resultado = resultado[resultado["Categoria"].isin(categorias)]
    if regiones:
        resultado = resultado[resultado["Region"].isin(regiones)]
    return resultado


def obtener_opciones(df: pd.DataFrame) -> dict:
    """
    Retorna un diccionario con las opciones unicas para los filtros.

    Llaves: "años", "categorias", "regiones"
    Cada una contiene una lista ordenada.
    """
    return {
        "años": sorted(df["Año"].unique().tolist()),
        "categorias": sorted(df["Categoria"].unique().tolist()),
        "regiones": sorted(df["Region"].unique().tolist()),
    }


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                                                                         ║
# ║                SU TRABAJO EMPIEZA AQUI — 6 PASOS                       ║
# ║                                                                         ║
# ║  Complete cada paso en orden. Se recomienda ejecutar el dashboard       ║
# ║  despues de cada paso para verificar que funcione antes de avanzar.     ║
# ║                                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝


# =============================================================================
# PASO 1: Configurar la pagina y cargar los datos
# =============================================================================
#
# En este paso usted debe hacer tres cosas:
#
# a) Configurar la pagina con st.set_page_config(). Esto define el titulo
#    de la pestaña del navegador y el ancho del dashboard.
#    Ejemplo:
#       st.set_page_config(page_title="Mi Dashboard", layout="wide")
#
# b) Cargar el archivo CSV usando pd.read_csv() y guardarlo en una
#    variable llamada 'df'. El archivo se llama "supertienda_cr.csv".
#    Ejemplo:
#       df = pd.read_csv("supertienda_cr.csv")
#
# c) Agregar una columna de año al DataFrame. Esto es necesario para
#    que los filtros del paso 6 funcionen. Convierta primero la columna
#    Fecha_Orden a tipo fecha y luego extraiga el año:
#       df["Fecha_Orden"] = pd.to_datetime(df["Fecha_Orden"])
#       df["Año"] = df["Fecha_Orden"].dt.year
#
# Documentacion:
#   st.set_page_config: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
#   pd.read_csv: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
#
# ---------------------------------------------------------------------------
# BITACORA — Paso 1
# Antes de escribir codigo, responda: Que entiende usted por "cargar
# un archivo CSV"? Ha trabajado antes con archivos de este tipo?
# Despues de completar el paso, anote: Que sucede cuando ejecuta
# streamlit run app.py? Que ve en el navegador?
# ---------------------------------------------------------------------------


# =============================================================================
# PASO 2: Titulo y resumen general (KPIs)
# =============================================================================
#
# Aqui usted debe mostrar el titulo del dashboard y los numeros principales.
#
# a) Use st.title() para colocar un titulo. El texto queda a su criterio.
#
# b) Llame a calcular_resumen(df) para obtener el diccionario con los totales.
#    Guarde el resultado en una variable, por ejemplo:
#       resumen = calcular_resumen(df)
#
# c) Cree columnas con st.columns(3) y dentro de cada una use st.metric()
#    para mostrar las ventas totales, la ganancia total y el total de ordenes.
#
#    Ejemplo:
#       col1, col2, col3 = st.columns(3)
#       col1.metric("Ventas Totales", f"${resumen['ventas']:,.0f}")
#       col2.metric("Ganancia Total", f"${resumen['ganancia']:,.0f}")
#       col3.metric("Ordenes", resumen['ordenes'])
#
# Documentacion: https://docs.streamlit.io/develop/api-reference/data/st.metric
#
# ---------------------------------------------------------------------------
# BITACORA — Paso 2
# Antes: Que es un KPI? Si no lo sabe, busquelo antes de continuar.
# Despues: Que hace la f antes de las comillas en f"${resumen['ventas']:,.0f}"?
# Que pasa si quita el :,.0f?
# ---------------------------------------------------------------------------


# =============================================================================
# PASO 3: Grafico de ventas por mes
# =============================================================================
#
# En este paso usted va a mostrar como se comportan las ventas a lo largo
# del tiempo mediante un grafico de linea.
#
# a) Llame a ventas_por_mes(df) y guarde el resultado.
#
# b) Use st.subheader() para ponerle un titulo a esta seccion.
#
# c) Use st.line_chart() para crear el grafico.
#    Necesita indicar cual columna va en el eje X y cual en el eje Y:
#       st.line_chart(datos, x="Año_Mes", y="Ventas")
#
# Documentacion: https://docs.streamlit.io/develop/api-reference/charts/st.line_chart
#
# ---------------------------------------------------------------------------
# BITACORA — Paso 3
# Antes: Para que sirve un grafico de linea? En que situaciones lo usaria?
# Despues: Observando el grafico, puede identificar algun patron en las
# ventas? Se venden mas en ciertos meses?
# ---------------------------------------------------------------------------


# =============================================================================
# PASO 4: Graficos de barras por categoria y por region
# =============================================================================
#
# Aqui va a mostrar dos graficos de barras uno al lado del otro.
# Para eso se usan columnas de Streamlit.
#
# a) Cree dos columnas:
#       izq, der = st.columns(2)
#
# b) Dentro de la columna izquierda, llame a ventas_por_categoria(df)
#    y muestre el resultado con st.bar_chart():
#       with izq:
#           st.subheader("Ventas por Categoria")
#           st.bar_chart(datos_cat, x="Categoria", y="Ventas")
#
# c) Repita lo mismo en la columna derecha con ventas_por_region(df).
#
# Documentacion: https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart
#
# ---------------------------------------------------------------------------
# BITACORA — Paso 4
# Antes: Que diferencia hay entre un grafico de barras y uno de linea?
# Cuando conviene usar cada uno?
# Despues: Cual categoria vende mas? Le sorprende el resultado?
# ---------------------------------------------------------------------------


# =============================================================================
# PASO 5: Tabla de datos
# =============================================================================
#
# Muestre una tabla con los datos del DataFrame para que el usuario
# pueda explorarlos directamente.
#
# a) Use st.subheader() para darle un titulo.
#
# b) Use st.dataframe() para mostrar la tabla:
#       st.dataframe(df, use_container_width=True, hide_index=True)
#
# Documentacion: https://docs.streamlit.io/develop/api-reference/data/st.dataframe
#
# ---------------------------------------------------------------------------
# BITACORA — Paso 5
# Antes: Para que podria ser util mostrar los datos crudos en un dashboard?
# Despues: Haga clic en el encabezado de alguna columna en la tabla.
# Que sucede? Que utilidad le ve a esa funcionalidad?
# ---------------------------------------------------------------------------


# =============================================================================
# PASO 6: Filtros en el sidebar
# =============================================================================
#
# Este es el paso mas complejo. Hasta ahora el dashboard muestra todos
# los datos. Aqui usted va a agregar filtros en la barra lateral para
# que el usuario pueda seleccionar que datos quiere ver.
#
# a) Obtenga las opciones disponibles:
#       opciones = obtener_opciones(df)
#
# b) Cree los filtros en el sidebar con st.sidebar.multiselect():
#       años_sel = st.sidebar.multiselect("Año", opciones["años"])
#       cats_sel = st.sidebar.multiselect("Categoria", opciones["categorias"])
#       regs_sel = st.sidebar.multiselect("Region", opciones["regiones"])
#
# c) Aplique los filtros con filtrar_datos():
#       df_filtrado = filtrar_datos(
#           df,
#           años=años_sel or None,
#           categorias=cats_sel or None,
#           regiones=regs_sel or None,
#       )
#    Nota: 'años_sel or None' retorna None cuando la lista esta vacia,
#    lo que le dice a la funcion que no filtre por ese campo.
#
# d) Ahora viene la parte importante: vuelva a los pasos 2, 3, 4 y 5,
#    y cambie 'df' por 'df_filtrado' en cada llamada a las funciones.
#    De esta manera, cuando el usuario seleccione un filtro, todos los
#    numeros y graficos se van a actualizar automaticamente.
#
# IMPORTANTE: Este paso requiere reorganizar el codigo. Los filtros
# deben ir ANTES de los pasos 2-5 para que df_filtrado exista cuando
# se usen las funciones. Piense en el orden de ejecucion.
#
# Documentacion: https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
#
# ---------------------------------------------------------------------------
# BITACORA — Paso 6
# Antes: En sus propias palabras, por que cree que los filtros deben ir
# antes de los graficos en el codigo? Que pasaria si van despues?
# Despues: Seleccione un año en el filtro. Se actualizaron los graficos?
# Si no, que tuvo que cambiar para que funcionara?
# Reflexion final: Que fue lo mas dificil de toda la asignacion? Que
# fue lo que mas le gusto? Como aplicaria un dashboard en otro contexto?
# ---------------------------------------------------------------------------
