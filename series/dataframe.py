import pandas as pd
import string

lista_ano = [2014,2012,1980,2019,2025,2024,2017,2025,1981,1976]
lista_filme = ['Interestellar',
             'The perks of being a wallflower',
             'The shining',
             'Once upon a time in hollywood',
             'Obsession',
             'The life of chuck',
             'Lady bird','Marty supreme',
             'Possession',
             'Carrie']

lista_diretor = ['Christopher Nollan',
                 'Stephen chbosky',
                 'Stanley Kubrick',
                 'Quentin Tarantino',
                 'Curry Barker',
                 'Mike Flanagan',
                 'Greta Gerwig',
                 'Josh Safdie',
                 'Andrzej Zulawski',
                 'Brian de Palma']

lista_rating= [4.5, 4.0, 4.2, 3.8, 4.1, 3.7, 3.8, 4.0, 4.0, 3.8]

lista_ator = ['Matthew McConaughey',
               'Emma Watson',
                'Shelley Duval',
                'Brad Pitt',
                'Inde Navarette',
                'Tom Hiddleston',
                'Saoirse Ronan',
                'Timothee Chalamet',
                'Isabelle Adjani',
                'Sissy Spacek']

dados = {
    "Ano": lista_ano,
    "Filme": lista_filme,
    "Diretor": lista_diretor,
    "Rating": lista_rating,
    "Ator": lista_ator
}
df = pd.DataFrame(dados)

df.index= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
print(df)

print("--------------------------------")
print(df.head(2))

print("--------------------------------")
print(df.tail(4))

print("--------------------------------")
df["Ano"] = df["Ano"].add(1)
print(df)

df= df.to_dict()
print(df)
