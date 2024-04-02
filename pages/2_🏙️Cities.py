# Importando Bibliotecas
# Libraries
from haversine import haversine

import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static

# Bibliotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster


st.set_page_config (page_title='Countries', page_icon='🏙️', layout = 'wide')


df_raw = pd.read_csv('dataset/zomato.csv')
df = df_raw.copy()

# Funções das respostas


def city_with_the_largest_number_of_different_cuisines(df1):
    # 5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
    df2 = df1.loc[:, ['Cuisines', 'Country Name', 'City']].groupby(['City','Country Name']).nunique().sort_values(['Cuisines'],ascending = False)[0:10].reset_index()
    fig = px.bar(df2, x = 'City', y = 'Cuisines', color='Country Name', title = 'Top 10 Cidades: Restaurantes com Mais Tipos de Culinárias Distintas')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade de Tipos de Culinárias Únicas')
    return fig


def city_more_restaurants_average_rating_below_two_and_a_half(df1):
    df2 = df1.loc[df1['Aggregate rating'] < 2.5, ['Restaurant ID','Country Name', 'City']].groupby(['City','Country Name']).count().sort_values(['Restaurant ID'],ascending = False)[0:7].reset_index()
    fig = px.bar(df2, x = 'City', y = 'Restaurant ID', color='Country Name', title = 'Restaurantes com Média de Avaliação Abaixo de 2.5')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade de Restaurantes')
    return fig


def city_more_restaurants_average_rating_above_four(df1):
    # 2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
    df2 = df1.loc[df1['Aggregate rating'] > 4, ['Country Name', 'Restaurant ID', 'City']].groupby(['City','Country Name']).count().sort_values(['Restaurant ID'],ascending = False)[0:7].reset_index()
    fig = px.bar(df2, x = 'City', y = 'Restaurant ID',color='Country Name', title = 'Restaurantes com Média de Avaliação Acima de 4')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade de Restaurantes')
    return fig




def city_most_registered_restaurants(df1):
    # 1. Qual o nome da cidade que possui mais restaurantes registrados?
    df2 = df1.loc[:, ['Country Name','Restaurant ID', 'City']].groupby(['City', 'Country Name']).count().sort_values(['Restaurant ID'],ascending = False)[0:10].reset_index()
    fig = px.bar(df2, x = 'City', y = 'Restaurant ID',color='Country Name', title = 'Top 10 Cidades com mais Restaurantes na Base de Dados')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade de Restaurantes')
    return fig

# Criando Funções:

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def Country_Name(country_id):
    return COUNTRIES[country_id]


# -----------------------------------------------


def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
    
# -----------------------------------------------

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# -----------------------------------------------

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df


#------------------------LIMPEZA DE DADOS----------------------


def clean_code(df):


    # Removendo linhas 'NaN'

    df = df.dropna(subset=['Restaurant ID'])
    df = df.dropna(subset=['Restaurant Name'])
    df = df.dropna(subset=['Cuisines'])
    df = df.dropna(subset=['Country Code'])
    df = df.dropna(subset=['Address'])
    df = df.dropna(subset=['Locality'])
    df = df.dropna(subset=['Locality Verbose'])
    df = df.dropna(subset=['Longitude'])
    df = df.dropna(subset=['Average Cost for two'])
    df = df.dropna(subset=['Has Table booking'])
    df = df.dropna(subset=['Has Online delivery'])
    df = df.dropna(subset=['Price range'])
    df = df.dropna(subset=['Aggregate rating'])
    df = df.dropna(subset=['Rating color'])
    df = df.dropna(subset=['Votes'])
    df = df.dropna(subset=['City'])
    #df = df.dropna(subset=['City'])

    df = df.dropna( )

    # Removendo linhas duplicadas
    df = df.drop_duplicates()

    df = df.drop(columns = ['Switch to order menu'], axis=1)

    # Define categorias de preço de acordo com o range
    df['Price range'] = df['Price range'].apply(create_price_tye)

    # Define o padrão de cores das avaliações
    df['Rating color'] = df['Rating color'].apply(color_name)

    # --------------------------------------------------------

    df['Country Name'] = df['Country Code'].map(Country_Name)
    # Definisdo os restaurantes po apenas um tipo de culinaria
    df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])


    df = df.copy()
    df = df.dropna(subset=['Country Name'])


    df2 = df['Restaurant ID'].unique()
    df2 = pd.DataFrame(df)
    QtdeRest = df2.count()
    print(QtdeRest)

    return df


# -------------------------------------------------- Inicio da estrutura logica do código ---------------------------------------


df1 = clean_code(df)



# ==================================================
# Barra Lateral
# ==================================================

st.sidebar.markdown ( """___""" )

st.sidebar.markdown( '## Filtros' )
countries_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'] )

st.sidebar.markdown ( """___""" )
st.sidebar.markdown( '### Powered by Uemerson Santana' )


#filtro de país
linhas_selecionadas = df1['Country Name'].isin ( countries_options ) # isin == esta em 
df1 = df1.loc[linhas_selecionadas, :]


# ==================================================
# Layout no Streamlit
# ==================================================


#with tab1:
st.title( '🏙️ Visão Cidades' )
    
with st.container():
    fig = city_most_registered_restaurants(df1)
    st.plotly_chart(fig,use_container_width=True)
    
    
with st.container():
    col1, col2 = st.columns ( 2, gap = "small" )
    with col1:
        fig = city_more_restaurants_average_rating_above_four(df1)
        st.plotly_chart(fig,use_container_width=True)
        
        
with st.container():
     # 3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
    with col2:
        fig = city_more_restaurants_average_rating_below_two_and_a_half(df1)
        st.plotly_chart(fig,use_container_width=True)
        

with st.container():
    fig = city_with_the_largest_number_of_different_cuisines(df1)
    st.plotly_chart(fig,use_container_width=True)
        

