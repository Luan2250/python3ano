import pandas as pd
import string
lista_ano = [2014,2012,1980,2019,2025,2024,2017,2025,1981,1976]
lista_filme = pd.Series(lista_ano, index=['Interestellar', 'The perks of being a wallflower', 'The shining',
 'Once upon a time in hollywood', 'Obsession','The life of chuck','Lady bird','Marty supreme','Possession','Carrie'])

serie_ano = pd.Series(lista_ano)
dict_ano = serie_ano.to_dict()

#print(type(lista_ano))
print(lista_ano)

#print(type(lista_filme))
print(lista_filme)

# print(lista_filme.index)
# print(lista_filme.values)
# print(lista_filme.dtype)
# print(lista_filme.info)

indice_alfabetico = list(string.ascii_uppercase[:len(lista_filme)])
lista_filme.index = indice_alfabetico

lista_ano_mais_1 = serie_ano.add(1)
lista_ano_mais_1 = serie_ano.add(1)
print("ano + 1:")
print(lista_ano_mais_1)
#lista_ano.to_dict()
dict_ano = serie_ano.to_dict()
dict_filme = lista_filme.to_dict()
print("Head 6 do filme:")
print(lista_filme.head(6))

print("Tail 7 do filme:")
print(lista_filme.tail(7))

print("Dicionario de lista_ano:")
print(dict_ano)

print("Dicionario de lista_filme:")
print(dict_filme)

