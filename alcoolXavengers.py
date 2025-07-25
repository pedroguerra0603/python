import pandas as pd
import numpy as np
import plotly.express as px
import dash 
from dash import dcc, html
from dash.dependencies import Input, Output

# Etapa 1: Carregar
# Função para carregar dados com o tratamento de exceção

def load_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding = 'ISO-8859-1')
        print (f'Dados carregados com sucesso de {file_path}')
        return data
    except:
        print(f'Erro ao carregar os dados de {file_path}')
        return None
    
# Carregar os CSVs
avengers_df = load_data(r'C:\Users\integral\Desktop\Python 2 - Pedro Guerra\Sistema\avengers.csv') 
drinks_df = load_data(r'C:\Users\integral\Desktop\Python 2 - Pedro Guerra\Sistema\drinks.csv')

# Etapa 2: Limpeza dos dados
# Função para limpar os dados
def clean_data (df, numeric_columns):
    try:
        # Remover linhas nulas
        df = df.dropna()
        #Garante que as colunas numéricas sejam convertidas corretamente
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors = 'coerce')
        print ('Dados limpos com Sucesso')
        return df
    except Exception as e:
        print (f'Erro ao limpar os dados: {e}')
        return None
    
#Limpar Avengers
avengers_df = clean_data(avengers_df, ['Appearances'])

# Limpar a tabela Drinks
drinks_df = clean_data(drinks_df, ['beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol'])

print ('\n Avengers Dataframe após a limpeza')
print(avengers_df.head())
print ('\n Drinks Dataframe após a limpeza')
print(drinks_df.head())

# Etapa 3: Vamos analisar os dados
def show_statistics(df, title):
    print(f'\nEstatísticas descritivas de {title}')
    print(df.describe())
    
show_statistics(avengers_df, 'Vingadores')
show_statistics(drinks_df, 'Consumo de Alcool')

# Etapa 4: criação da visualização com o plotly
def create_avengers_chart():
    return px.bar(
        avengers_df,
        x = 'Name/Alias',
        y = 'Appearances',
        title = 'Número de Aparições dos Vingadores',
        labels = {'Name/Alias':'Personagem', 'Appearances':'Numero de aparições'},
        color = 'Gender'
    )
    
# Função para criar o gráfico de consumo de alcool
def create_drinks_chart():
    return px.bar(
        drinks_df,
        x = "country",
        y = "total_litres_of_pure_alcohol",
        title = "Consumo de Alcool por País",
        labels = {'country':'Pais', 'total_litres_of_pure_alcohol':'Litros de Alcool'},
        color = 'total_litres_of_pure_alcohol'
    )
    
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Análise de Dados - Vingadores e Consumo de Alcool', style={'text-align':'center'}),
    # Dropdown para escolher a visualização
    dcc.Dropdown(
        id = 'dropdown-chart',
        options = [
            {'label':'Numero de Aparições dos Vingadores', 'value':'avengers'},
            {'label':'Consumo de Alcool por País', 'value':'drinks'}
        ],
        placeholder = 'Escolha um Gráfico',
        style = {'width':'50%', 'margin':'auto'}
    ),
    dcc.Graph(id='graph-output')
])

# Função de Callback para atualizar o gráfico baseado na escolha do dropdown
@app.callback(
    Output('graph-output', 'figure'),
    [Input('dropdown-chart', 'value')]
)

def update_graph(chart_type):
    try:
        if chart_type == 'avengers':
            return create_avengers_chart()
        elif chart_type == 'drinks':
            return create_drinks_chart()
    except Exception as e:
        print(f'Erro ao gerar o gráfico: {e}')
        

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print (f'Erro ao rodar o servidor Dash: {e}')
