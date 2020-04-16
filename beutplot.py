# https://github.com/rodrigosimoes182/beutplot.git
# Codigo Baseado em https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less-affc361b2c6a
# Alterações realizadas para adequação de informaçoes e aprendizado da biblioteca Matplotlib
# Section 1 - Importando bibliotecas  
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
#importando Bokeh
from bokeh.plotting import figure, output_file, show

# Section 2 - Carregando os dados CSV e montando um Dataframe
df = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv", parse_dates=['Date'])
countries = ['Brazil','Germany','United Kingdom', 'US', 'France', 'China']
df = df[df['Country'].isin(countries)]

# Section 3 - Criando as colunas
df['Cases'] = df[['Confirmed','Recovered','Deaths']].sum(axis=1)

# Section 4 - Reestruturando os dados
df = df.pivot(index='Date', columns='Country', values='Cases')
countries = list(df.columns)
covid = df.reset_index('Date')
covid.set_index(['Date'], inplace=True)
covid.columns = countries

# Section 5 - Calculando casos por  100,000 habitantes
populations = {'Brazil':216939396, 'Germany': 83721496 , 'United Kingdom': 67802690 , 'US': 330548815, 'France': 65239883, 'China':1438027228}
percapita = covid.copy()
for country in list(percapita.columns):
    percapita[country] = percapita[country]/populations[country]*100000
    #print(percapita['Brazil'])
#Criando a lista de paises e arrumando dados para os graficos
colors = {'Brazil':'#045275', 'China':'#089099', 'France':'#7CCBA2', 'Germany':'#FCDE9C', 'US':'#DC3977', 'United Kingdom':'#7C1D6F'}

dias = covid.index
#Adaptação do código  com Bokeh ----------------------------------------
# output to static HTML file
output_file("/Users/rodsim/Documents/beutplot/log_lines.html")
# create a new plot
p = figure(
   tools="pan,box_zoom,reset,save",y_range=[0, 10**6],x_axis_type="datetime", title="Quantidade de casos",
  x_axis_label='Dias', y_axis_label='Casos'
)

# add some renderers
for pais in countries:
    p.line(x = dias, y = covid[pais], legend_label= pais,line_width=6, line_color=colors[pais])
    p.circle(x = dias, y = covid[pais], legend_label= pais, fill_color="white", size=7, line_color=colors[pais])

show(p)