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
# ou import PIL.Image as imgpil


st.set_page_config (page_title='Countries', page_icon='🌎', layout = 'wide')


df_raw = pd.read_csv('dataset/zomato.csv')
df = df_raw.copy()


# Funções das respostas

def dish_price_for_two_by_country(df1):
    # 11. Qual a média de preço de um prato para dois por país?
    df2 = round(df1.loc[:, ['Average Cost for two', 'Country Name']].groupby('Country Name').mean().sort_values(['Average Cost for two'], ascending = False).reset_index(),2)
    fig = px.bar(df2, x = 'Country Name', y = 'Average Cost for two', title = 'Média de Preço de um Prato para duas Pessoas por País')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title = 'Países', yaxis_title='Preço de Prato para duas Pessoas')
    return fig




def recorded_average_grade(df1):
    # 10. Qual o nome do país que possui, na média, a menor nota média registrada?
    df2 = df1.loc[:, ['Votes', 'Country Name']].groupby('Country Name').mean().sort_values(['Votes'], ascending = False).reset_index()
    fig = px.bar(df2, x = 'Country Name', y = 'Votes', title = 'Média de Avaliações Feitas por País')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title = 'Países', yaxis_title='Quantidade de Avaliações')
    return fig




def registered_city(df1):
    # 1. Qual o nome do país que possui mais cidades registradas?
    df2 = df1.loc[:, ['City', 'Country Name']].groupby('Country Name').nunique().sort_values(['City', 'Country Name'],ascending = False).reset_index()
    fig = px.bar(df2, x = 'Country Name', y = 'City', title = 'Quantidade de Cidades Registradas por País')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title = 'Países', yaxis_title='Quantidade de Cidades')
    return fig




def countries_regis(df1):
    # 2. Qual o nome do país que possui mais restaurantes registrados?
    df3 = df1.loc[:, ['Restaurant ID', 'Country Name']].groupby('Country Name').count().sort_values(['Restaurant ID', 'Country Name'],ascending = False).reset_index()
    fig = px.bar(df3, x = 'Country Name', y = 'Restaurant ID', title = 'Quantidade de Restaurantes Registrados por País')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Países', yaxis_title='Quantidade de Restaurantes')
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

    # df.info() #valores nulos
    #print(df.isnull())
    # print(df.isna())


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

#tab1, tab2, tab3 = st.tabs ( [ 'Visão Gerencial', '_', '_'])

#with tab1:
st.title( '🌎 Visão Países' )
    
    
    
with st.container():
    fig = countries_regis(df1)
    st.plotly_chart(fig,use_container_width=True)


        
        
with st.container():
    fig = registered_city(df1)
    st.plotly_chart(fig,use_container_width=True)
    
    
    
with st.container():
    # 10. Qual o nome do país que possui, na média, a menor nota média registrada?
    col1, col2 = st.columns ( 2 )
    with col1:
        fig = recorded_average_grade(df1)
        st.plotly_chart(fig,use_container_width=True)
        

with st.container():
    with col2:
        fig = dish_price_for_two_by_country(df1)
        st.plotly_chart(fig,use_container_width=True)
        
    
        
        
        
        
        
        
        
    
