import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregar o dataset
df = pd.read_excel("Adidas US Sales Datasets2.xlsx")

st.logo = "logo-adidas.png"

df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])
df = df.sort_values("Invoice Date")

# Criar a coluna 'Month' como datetime
df['Month'] = pd.to_datetime(df['Invoice Date'].dt.to_period('M').astype(str))

# Criar uma lista de meses únicos formatados para exibição
month_options = ["Todos"] + df['Month'].dt.strftime('%Y-%m').unique().tolist()
selected_month = st.sidebar.selectbox("Selecione o mês", month_options)

# Filtrar pelo mês selecionado
if selected_month != "Todos":
    df_filtered = df[df['Month'].dt.strftime('%Y-%m') == selected_month]
else:
    df_filtered = df

# Criar lista de vendedores para seleção
seller_options = ["Todos"] + list(df["Seller"].unique())
vendedores = st.sidebar.selectbox("Vendedores", seller_options)

# Filtrar pelo vendedor selecionado
if vendedores != "Todos":
    df_filtered = df_filtered[df_filtered["Seller"] == vendedores]

# Layout das colunas
col01, col02, col03 = st.columns(3)
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráficos
col01.metric(
    label="Total Faturamento",
    value=f"{df_filtered['Total Sales'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    delta=None,
    delta_color='off',
)

col02.metric(
    label="Total Unidades Vendidas",
    value=f"{df_filtered['Units Sold'].sum():,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    delta=None,
    delta_color="off",
)

# Garantir que o cálculo seja feito com valores agregados (sum)
total_sales = df_filtered['Total Sales'].sum()
operating_profit = df_filtered['Operating Profit'].sum()
# Calcular a margem
if total_sales != 0:  # Prevenir divisão por zero
    margem = ((total_sales - operating_profit) / total_sales) * 100
else:
    margem = 0
# Exibir a métrica
col03.metric(
    label="Margem (%)",
    value=round(margem, 2),  # Arredondar para 2 casas decimais
    delta=None,              # Você pode usar um delta se quiser comparar com outro valor
    delta_color='normal'
)

fat_por_categoria = df_filtered.groupby('Product')['Total Sales'].sum().sort_values(ascending=False).reset_index()
fig_cat = px.bar(fat_por_categoria, 
                 x='Product', 
                 y='Total Sales', 
                 title='Faturamento por Categoria',
                 template='plotly_white')
col1.plotly_chart(fig_cat, use_container_width=True)

fat_por_catregiao = df_filtered.groupby(['Product', 'Region'])['Total Sales'].sum().sort_values(ascending=False).reset_index()
fig_catregiao = px.bar(fat_por_catregiao, x="Product", y="Total Sales", color="Region", title="Faturamento por Categoria e Região")
col2.plotly_chart(fig_catregiao, use_container_width=True)

fat_regiao = df_filtered.groupby("Region")[["Total Sales"]].sum().sort_values(by='Total Sales', ascending=False).reset_index()
fig_regiao = px.bar(fat_regiao, x="Region", y="Total Sales",
                      title="Faturamento por Região")
col3.plotly_chart(fig_regiao, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Total Sales", names="Sales Method",
                  title="Faturamento por tipo de venda")
col4.plotly_chart(fig_kind, use_container_width=True)

mean_price = df_filtered.groupby('Product')['Total Sales'].mean().sort_values(ascending=True).reset_index()
fig_mean = px.bar(mean_price, x="Total Sales", y="Product",
                  title="Preço Médio por Categoria")
col5.plotly_chart(fig_mean, use_container_width=True)