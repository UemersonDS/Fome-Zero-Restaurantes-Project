# Importando Bibliotecas
# LibrariesS
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


st.set_page_config (page_title='Main Page', page_icon='📈')



df_raw = pd.read_csv('dataset/zomato.csv')

df = df_raw.copy()


#Funções das respostas

def registered_cuisines(df1):    
        cols = ['Average Cost for two', 'Cuisines', 'Aggregate rating', 'City', 'Latitude', 'Longitude']
        map = folium.Map()
        marker_cluster = MarkerCluster().add_to(map)
        
        # desenhando mapa
        for index, location_info in df1.iterrows():
                  folium.Marker([location_info['Latitude'],
                         location_info['Longitude']], icon=folium.Icon(color='green')).add_to(marker_cluster)
        folium_static ( map, width = 1024, height = 600 )


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
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

# ---------------LIMPEZA DE DADOS--------------------------------

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
df.dropna( )

# Removendo linhas duplicadas
df = df.drop_duplicates().reset_index()

df = df.drop(columns = ['Switch to order menu'], axis=1)

# Define categorias de preço de acordo com o range
df['Price range'] = df['Price range'].apply(create_price_tye)

# Define o padrão de cores das avaliações
df['Rating color'] = df['Rating color'].apply(color_name)

# --------------------------------------------------------

df['Country Name'] = df['Country Code'].map(Country_Name)
# Definisdo os restaurantes po apenas um tipo de culinaria
df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])




# -------------------------------------------------- Inicio da estrutura logica do código ---------------------------------------


df1 = df.copy()


# ==================================================
# Barra Lateral
# ==================================================


st.header( '📈 Marketplace - Fome Zero!' )
st.markdown( '### O Melhor lugar para encontrar seu mais novo restaurante favorito!' )

image_path = 'logo.webp'
image = Image.open ( image_path )
st.sidebar.image ( image, width=120 )

st.sidebar.markdown ( '# Fome Zero' )
st.sidebar.markdown ( "## Zomato's Geographic Analysis" )
st.sidebar.markdown ( """___""" )

st.sidebar.markdown( '## Filtros' )
countries_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'])


                   
st.sidebar.markdown ( """___""" )
st.sidebar.markdown( '### Powered by Uemerson Santana' )



#filtro de país
linhas_selecionadas = df1['Country Name'].isin ( countries_options ) # isin == esta em 
df1 = df1.loc[linhas_selecionadas, :]



# ==================================================
# Layout no Streamlit
# ==================================================


with st.container():
    st.markdown( '#### Temos as seguintes marcas dentro da nossa plataforma:' )
            
    col1, col2, col3, col4, col5 = st.columns ( 5, gap = "small" )
            
    with col1:
        # 1. Quantos restaurantes únicos estão registrados?
        rest_unique = df.loc[:, 'Restaurant ID'].nunique()
        col1.metric( 'Total de Restaurantes', rest_unique  )

    with col2:
        # 2. Quantos países únicos estão registrados?
        paises = df1.loc[:, 'Country Name'].nunique()
        col2.metric( 'Países Cadastrados', paises )
                
    with col3:
        # 3. Quantas cidades únicas estão registradas?
        city_unique = df1.loc[:,'City'].nunique()
        col3.metric( 'Cidades Cadastradas', city_unique )
                    
    with col4:
        # 4. Qual o total de avaliações feitas?
        avl_total = df1.loc[:, 'Votes'].sum()
        col4.metric( 'Avaliações Feitas', avl_total )
            
    with col5:
        # 5. Qual o total de tipos de culinária registrados?
        culi_registradas = len(df1.loc[:, 'Cuisines'].unique())
        col5.metric( 'Tipos de Culinárias', culi_registradas )
                
                
                
                
                
with st.container():
    registered_cuisines(df1)
        
         

    
    
    
    
    
    
    
    
    
    
