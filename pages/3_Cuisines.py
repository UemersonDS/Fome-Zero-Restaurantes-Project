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


st.set_page_config (page_title='Cuisines', page_icon='🍽️', layout = 'wide')


df_raw = pd.read_csv('dataset/zomato.csv')
df = df_raw.copy()


# Funções das respostas


def worst_types_of_cuisine(df1): 
    # 13. Qual o tipo de culinária que possui a menor nota média?
    df2 = df1.loc[:, ['Aggregate rating', 'Cuisines']].groupby('Cuisines').mean().sort_values(['Aggregate rating'],ascending = True).reset_index()[2:12]
    # 13. Qual o tipo de culinária que possui a menor nota média?
    fig = px.bar(df2, x = 'Cuisines', y = 'Aggregate rating', title = 'Piores Tipos de Culinárias')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Tipo de Culinária', yaxis_title='Média de Avaliações Médias')
    return fig
        
        


def best_types_of_cuisine(df1):
    #12. Qual o tipo de culinária que possui a maior nota média?
    df2 = df1.loc[:, ['Aggregate rating', 'Cuisines']].groupby('Cuisines').mean().sort_values(['Aggregate rating'],ascending = False).reset_index()[0:10]
    fig = px.bar(df2, x = 'Cuisines', y = 'Aggregate rating', title = 'Melhores Tipos de Culinárias')
    fig.update_traces(texttemplate = '%{y}', textposition = 'outside')
    fig.update_layout(xaxis_title='Tipo de Culinária', yaxis_title='Média de Avaliações Médias')
    return fig




def top_ten_restaurants(df1):
    # Top 10 Restaurantes
    st.markdown('#### Top 10 Restaurantes')
    cols = ['Restaurant ID', 'Restaurant Name', 'Country Name', 'City', 'Cuisines', 'Average Cost for two', 'Aggregate rating', 'Votes']
    valor = df1.loc[:, cols].groupby('Restaurant ID').max().sort_values(['Aggregate rating'],ascending = False).reset_index().head(10)
    return valor




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

# ---------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------

cuisines_options = st.sidebar.multiselect(
    'Escolha os Tipos de Culinária',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],
    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'Italian'] )




st.sidebar.markdown ( """___""" )
st.sidebar.markdown( '### Powered by Uemerson Santana' )


#filtro de país
linhas_selecionadas = df1['Country Name'].isin ( countries_options ) # isin == esta em 
df1 = df1.loc[linhas_selecionadas, :]


# filtro de cozinhas
linhas_selecionadas = df1['Cuisines'].isin ( cuisines_options )
df1 = df1.loc[linhas_selecionadas, :]




# ==================================================
# Layout no Streamlit
# ==================================================

#tab1, tab2, tab3 = st.tabs ( [ 'Visão Gerencial', '_', '_'])

#with tab1:
st.title( '🍽️ Visão Tipos de Cozinhas' )
    
    
    
with st.container():
    st.markdown('#### Melhores Restaurantes dos Principais tipos Culinários')
        
    col1, col2, col3, col4, col5 = st.columns ( 5, gap = "small" )
    
    with col1:
        #Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
        df1.loc[df1['Cuisines'] == 'Italian', ['Aggregate rating', 'Restaurant Name']].groupby('Restaurant Name').mean().sort_values(['Aggregate rating'],ascending = False).reset_index()
        col1.metric( 'Italiana: Central Grocery', '4.9/5.0'  )
     
    
    
    
    with col2:
        # 3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
          valor = (df1.loc[df1['Cuisines'] == 'American', ['Aggregate rating', 'Restaurant Name']]
                      .groupby('Restaurant Name')
                      .mean().sort_values(['Aggregate rating'],ascending = False)
                      .reset_index())
          col2.metric( "Americana: Hodad's ", '4.9/5.0' )
        
        
        
    with col3:
        # 3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
        valor = (df1.loc[df1['Cuisines'] == 'American', ['Aggregate rating', 'Restaurant Name']]
                    .groupby('Restaurant Name')
                    .mean()
                    .sort_values(['Aggregate rating'],ascending = False)
                    .reset_index())
        col3.metric( 'Árabe: Mandi@36', '4.7/5.0' )
       
    
    
    
    with col4:   
        # 7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
        valor = (df1.loc[df1['Cuisines'] == 'Japanese', ['Aggregate rating', 'Restaurant Name']]
                    .groupby('Restaurant Name')
                    .mean()
                    .sort_values(['Aggregate rating'],ascending = False)
                    .reset_index())
        col4.metric( 'Japonesa: Samurai', '4.9/5.0' )
        
        
        
        
    with col5:
        # 9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
        valor = (df1.loc[df1['Cuisines'] == 'Home-made', ['Aggregate rating', 'Restaurant Name']]
                   .groupby('Restaurant Name')
                   .mean()
                   .sort_values(['Aggregate rating'],ascending = False)
                   .reset_index())
        col5.metric( 'Caseira: Kanaat Lokantası', '4.0/5.0' )
        
    
    
    
with st.container():
    valor = top_ten_restaurants(df1)
    st.dataframe( valor, use_container_width = True )
    
    
    
with st.container():
    st.markdown('#### Melhores e Piores Tipos de Culinárias')
    col1, col2 = st.columns ( 2, gap = 'small')
    with col1:
        fig = best_types_of_cuisine(df1)
        st.plotly_chart(fig,use_container_width=True)
        
        
   
    with col2:    
        fig = worst_types_of_cuisine(df1)
        st.plotly_chart(fig,use_container_width=True)



        
   
           
        
        
    
    
    


