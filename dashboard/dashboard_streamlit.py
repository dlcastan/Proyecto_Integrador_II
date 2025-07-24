import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os


st.set_page_config(page_title="Dashboard E-commerce", layout="wide")


DB = os.getenv("POSTGRES_DB", "EcommerceDB")
USER = os.getenv("POSTGRES_USER", "admin")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "dept01")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")


engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")


@st.cache_data
def load_data():
    df_compras = pd.read_sql("SELECT * FROM int_detalle_ordenes_enriquecido", engine)
    df_productos = pd.read_sql("SELECT * FROM int_metricas_productos", engine)  # Cambiado aquí
    kpi_ventas = pd.read_sql("SELECT * FROM kpi_valor_total_ventas", engine)
    kpi_ticket = pd.read_sql("SELECT * FROM kpi_ticket_promedio", engine)
    kpi_satisfaccion = pd.read_sql("SELECT * FROM kpi_satisfaccion_productos", engine)
    kpi_recompra = pd.read_sql("SELECT * FROM kpi_recompra_clientes", engine)
    return kpi_ventas, kpi_ticket, kpi_satisfaccion, kpi_recompra, df_compras, df_productos

kpi_ventas, kpi_ticket, kpi_satisfaccion, kpi_recompra, df_compras, df_productos = load_data()

df_compras["fechaorden"] = pd.to_datetime(df_compras["fechaorden"])

tab1, tab2, tab3 = st.tabs(["KPIs", "Compras", "Productos"])

with tab1:
    st.header("Indicadores KPIs principales")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        row = kpi_ventas.iloc[0]
        st.metric(label=row['kpi_nombre'], value=f"${row['valor']:,.2f}", help=row['descripcion'])

    with col2:
        row = kpi_ticket.iloc[0]
        st.metric(label=row['kpi_nombre'], value=f"${row['valor']:,.2f}", help=row['descripcion'])

    with col3:
        row = kpi_satisfaccion.iloc[0]
        st.metric(label=row['kpi_nombre'], value=f"{row['valor']:.2f}", help=row['descripcion'])

    with col4:
        row = kpi_recompra.iloc[0]
        st.metric(label=row['kpi_nombre'], value=f"{row['valor']}%", help=row['descripcion'])

with tab2:
    st.header("Detalle de compras")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventas por categoría")
        fig1, ax1 = plt.subplots()
        df_compras.groupby("categoria_nombre")["subtotal"].sum().sort_values().plot(kind="barh", ax=ax1)
        ax1.set_xlabel("Subtotal acumulado")
        st.pyplot(fig1)

    with col2:
        st.subheader("Cantidad vendida por producto")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        vendidos = df_compras.groupby("producto_nombre")["cantidad"].sum().sort_values(ascending=False).head(15)
        vendidos.plot(kind="bar", ax=ax2)
        ax2.set_ylabel("Cantidad vendida")
        ax2.set_title("Top productos por unidades vendidas")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Cantidad de stock por producto")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        stock = df_productos.set_index("nombre")["stock"].sort_values(ascending=False).head(15)
        stock.plot(kind="bar", ax=ax3)
        ax3.set_ylabel("Stock disponible")
        ax3.set_title("Productos con más stock")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig3)

    with col4:
        st.subheader("Total de órdenes por producto")
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ordenes = df_compras.groupby("producto_nombre")["ordenid"].nunique().sort_values(ascending=False).head(15)
        ordenes.plot(kind="bar", ax=ax4)
        ax4.set_ylabel("Cantidad de órdenes")
        ax4.set_title("Productos con más órdenes únicas")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig4)

    st.subheader("Tabla de compras")
    st.dataframe(df_compras)

with tab3:
    st.header("Análisis de productos")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top productos más vendidos")
        fig6, ax6 = plt.subplots(figsize=(8, 6))

        productos_con_ventas = df_productos[df_productos["total_vendido"] > 0]
        top_productos = productos_con_ventas.nlargest(10, "total_vendido")
        
        sns.barplot(data=top_productos, y="nombre", x="total_vendido", ax=ax6)
        ax6.set_title("Top 10 productos más vendidos")
        ax6.set_xlabel("Total vendido")
        st.pyplot(fig6)

    with col2:
        st.subheader("Distribución de calificaciones")
        fig7, ax7 = plt.subplots(figsize=(8, 6))

        productos_calificados = df_productos[df_productos["calificacion_promedio"] > 0]
        sns.histplot(productos_calificados["calificacion_promedio"], bins=10, kde=True, ax=ax7)
        ax7.set_title("Distribución de calificaciones promedio")
        ax7.set_xlabel("Calificación promedio")
        st.pyplot(fig7)

    st.subheader("Relación entre precio y calificación")
    fig8, ax8 = plt.subplots(figsize=(10, 6))

    productos_scatter = df_productos[df_productos["calificacion_promedio"] > 0]
    sns.scatterplot(data=productos_scatter, x="precio", y="calificacion_promedio", 
                   hue="categoria_nombre", ax=ax8)
    ax8.set_title("Precio vs Calificación Promedio")
    ax8.set_xlabel("Precio")
    ax8.set_ylabel("Calificación Promedio")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig8)

    st.subheader("Métricas de productos por categoría")
    col3, col4 = st.columns(2)
    
    with col3:
        fig9, ax9 = plt.subplots(figsize=(8, 6))
        categoria_ventas = df_productos.groupby("categoria_nombre")["total_vendido"].sum().sort_values(ascending=False)
        categoria_ventas.plot(kind="bar", ax=ax9)
        ax9.set_title("Ventas totales por categoría")
        ax9.set_ylabel("Total vendido")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig9)
    
    with col4:
        fig10, ax10 = plt.subplots(figsize=(8, 6))
        categoria_ingresos = df_productos.groupby("categoria_nombre")["ingresos_totales"].sum().sort_values(ascending=False)
        categoria_ingresos.plot(kind="bar", ax=ax10)
        ax10.set_title("Ingresos totales por categoría")
        ax10.set_ylabel("Ingresos totales")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig10)

    st.subheader("Tabla de productos con métricas")

    columnas_importantes = ['nombre', 'categoria_nombre', 'precio', 'stock', 'total_vendido', 
                          'ingresos_totales', 'calificacion_promedio', 'total_reseñas', 
                          'categoria_ventas', 'categoria_calificacion']
    st.dataframe(df_productos[columnas_importantes])
