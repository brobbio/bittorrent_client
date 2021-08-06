import re

####COMENTAR VARIAS LÍNEAS: CTRL+ALT+/####

def tokenize(text, patron=re.compile(rb'([idel])|(\d+):|(-?\d+)')):
    '''([idel])|(\d+): tiene  partes. 1 es {i,d,e,l}. 2 es por lo menos un número
                    3. 0 o 1 veces un número'''
    i = 0
    while i < len(text):
        s = patron.finditer(text)
        iterador = next(s)
        elemento = iterador.group()
        grupos = s.group(s.lastindex)
        if iterador.start() < i:
            iterador = next(s)
        i = s.end()
        if s.lastindex == 2:
            yield "s"
            yield text[i:i+s.end()]
            i = i + s.end()
        else:
            yield s


def decode_item(next, token):
    if token == "i":
        # integer: "i" value "e"
        data = int(next())
        if next() != "e":
            raise ValueError
#    elif token == "s":
        # string: "s" value (virtual tokens)
#        data = next()
    elif token == "l" or token == "d":
        # container: "l" (or "d") values "e"
        data = []
        tok = next()
        while tok != "e":
            data.append(decode_item(next, tok))
            tok = next()
        if token == "d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        raise ValueError
    return data

def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(next(src), next(src).group())
        for token in src: # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data

def parsing_elemento_dicOLista(texto, longitud):
    '''Devuelve los elementos correspondientes a un diccionario o lista. PRE: texto empieza en : '''
    j = 0
    entero = ''
    res = texto[1+j:1+j+longitud]
    return res

def parsing(texto, posicion):
    '''Devuelve en variable data el tipo de objeto correspondiente al token en texto[posicion]'''
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
    data = open("big-buck-bunny.torrent", "rb").read()
    torrent = parsing(data, 0)[0]
