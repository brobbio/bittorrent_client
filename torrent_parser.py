import re

def parsing_elemento_dicOLista(texto, longitud):
    '''Returns the elements corresponding to a dictionary or list. PRE: text begins with : '''
    j = 0
    entero = ''
    res = texto[1+j:1+j+longitud]
    return res

def parsing(texto, posicion = 0):
    '''Returns a dictionary with the metadata of the torrent'''
    i = posicion

    if chr(texto[i]) == 'i':         #Parseo si hay un entero
        j = 1
        entero = ''
        while chr(texto[i+j]) in ['0','1','2','3','4','5','6','7','8','9']:
            entero = entero + chr(texto[i+j])
            j=j+1
        data = int(entero)
        if chr(texto[i+j]) != 'e':
            raise ValueError

    elif chr(texto[i]) == 'd' or chr(texto[i]) == 'l':        #Parseo si es diccionario o lista
        data = []
        j = 1
        while chr(texto[i+j]) != 'e':
            if chr(texto[i+j]) in ['0','1','2','3','4','5','6','7','8','9']:
                entero = ''
                while chr(texto[i+j]) in ['0','1','2','3','4','5','6','7','8','9']:
                    entero = entero + chr(texto[i+j])
                    j = j+1
                longitud = int(entero)
                nuevo_elemento = parsing_elemento_dicOLista(texto[i+j:], longitud)
                data.append(nuevo_elemento)
                j = j+1+longitud
            else:
                res = parsing(texto, i+j)
                j = j+res[1]+1
                data.append(res[0])
        if chr(texto[i]) == 'd':
            datos = 0
            data_dict =  dict([])
            while datos < len(data):
                data_dict[data[datos]] = data[datos+1]
                datos = datos+2
            return (data_dict, j)
    else:
        raise ValueError
    return (data, j)

if __name__ == "__main__":
    data = open("./Torrent_examples/ubuntu-21.04-desktop-amd64.iso.torrent", "rb").read()
    torrent = parsing(data, 0)[0]
