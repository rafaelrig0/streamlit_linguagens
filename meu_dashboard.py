import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title('Dashboard de Vendas')


@st.cache_data
def carregar_dados():
    df = pd.read_csv('vendas.csv', parse_dates=['data_pedido'])
    return df
df = carregar_dados()

st.sidebar.title('Filtros')

lista_de_categorias = sorted(df['categoria'].unique())

categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=lista_de_categorias,
    default=lista_de_categorias
)

if categorias_selecionadas:
    df_filtrado = df[df['categoria'].isin(categorias_selecionadas)]
else:
    df_filtrado = df.copy()

col1, col2 = st.columns([1, 1])

receita_calculada = df_filtrado['receita'].sum()
total_pedidos = df_filtrado['pedido_id'].nunique()

with col1:
    st.metric(label='Receita Total', value=f"R$ {receita_calculada:,.2f}")
with col2:
    st.metric(label='Total de Pedidos', value=f"{total_pedidos:,}")

st.divider()

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])
with aba1:
    receita_mensal = (
        df_filtrado
        .assign(mes=df_filtrado['data_pedido'].dt.to_period('M').astype(str))
        .groupby('mes')['receita']
        .sum()
        .sort_index()
    )
    st.area_chart(receita_mensal)
with aba2:
    st.dataframe(df_filtrado, use_container_width=True)

    csv_para_download = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados filtrados (CSV)",
        data=csv_para_download,
        file_name='vendas_filtradas.csv',
        mime='text/csv'
    )
