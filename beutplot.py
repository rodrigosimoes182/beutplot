# https://github.com/rodrigosimoes182/beutplot.git
# Codigo Baseado em https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less-affc361b2c6a
# Alterações realizadas para adequação de informaçoes e aprendizado da biblioteca Matplotlib
# Section 1 - Importando bibliotecas  
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

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

# Section 6 - Generando cores e estilos do grafico
colors = {'Brazil':'#045275', 'China':'#089099', 'France':'#7CCBA2', 'Germany':'#FCDE9C', 'US':'#DC3977', 'United Kingdom':'#7C1D6F'}
plt.style.use('fivethirtyeight')

# Section 7 - Criando a visualização
plot = covid.plot(figsize = (9,6), color=list(colors.values()), linewidth=3, legend=True)
plot.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
plot.grid(color='#d4d4d4')
plot.set_xlabel('Data')
plot.set_ylabel('No. de Casos')

# Section 8 - Atribuindo as cores aos paises
for country in list(colors.keys()):
    plot.text(x = covid.index[-1], y = covid[country].max(), color = colors[country],s = country, weight = 'bold')

# Section 9 - Adicionando as legendas
plot.text(x = covid.index[1], y = int(covid.max().max())+95000, s = "COVID-19 Casos por país", fontsize = 14, weight = 'bold', alpha = .75)
plot.text(x = covid.index[1], y = int(covid.max().max())+15000, s = "Para Brasil, USA, China, Alemanha, França e Reino Unido \nInclui Casos Atuais, Recuperados, e Mortes", fontsize = 10, alpha = .75)
plot.text(x = percapita.index[1], y = -1000000,s = 'by Rodsim182                 Source: https://github.com/datasets/covid-19/blob/master/data/countries-aggregated.csv', fontsize = 8)  

# Section 10 - Segundo Grafico  
percapitaplot = percapita.plot(figsize=(9,6), color=list(colors.values()), linewidth=5, legend=True)
percapitaplot.grid(color='#d4d4d4')
percapitaplot.set_xlabel('Date')
percapitaplot.set_ylabel('No. de Casos por 100 mil habitantes')
for country in list(colors.keys()):
    percapitaplot.text(x = percapita.index[-1], y = percapita[country].max(), color = colors[country], s = country, weight = 'bold')
percapitaplot.text(x = percapita.index[1], y = percapita.max().max()+27, s = "Per Capita COVID-19 Casos por país", fontsize = 14, weight = 'bold', alpha = .75)
percapitaplot.text(x = percapita.index[1], y = percapita.max().max()+12, s = "Para Brasil, USA, China, Alemanha, França e Reino Unido \nInclui Casos Atuais, Recuperados, e Mortes", fontsize = 10, alpha = .75)
percapitaplot.text(x = percapita.index[1], y = -55,s = 'Rodsim182                     Source: https://github.com/datasets/covid-19/blob/master/data/countries-aggregated.csv', fontsize = 10)

# Section 11 - "Voit la" o resultado!
plt.show()
#plt.savefig()
