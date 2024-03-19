import re

def slice_text(text, length):
    '''Slices text'''
    return text[1:1+length]

def parse_integer(texto, position):
    j = 1
    entero = ''
    while chr(texto[position+j]) in ['0','1','2','3','4','5','6','7','8','9']:
        entero = entero + chr(texto[position+j])
        j=j+1
    data = int(entero)

    if chr(texto[position+j]) != 'e':
        raise ValueError(f"Invalid torrent encoding in byte character {position}")
    
    return (data, j)

def parse_list(texto, position):
    data = []
    j = 1
    while chr(texto[position+j]) != 'e':
        if chr(texto[position+j]) in '0123456789':
            entero = ''
            while chr(texto[position+j]) in '0123456789':
                entero = entero + chr(texto[position+j])
                j = j+1
            length = int(entero)
            nuevo_elemento = slice_text(texto[position+j:], length)
            data.append(nuevo_elemento)
            j = j+1+length
        else:
            res = parsing(texto, position+j)
            j = j+res[1]+1
            data.append(res[0])
    return (data, j)

def parse_dictionary(texto, position):
    (data, j) = parse_list(texto, position)

    data_dict =  dict([])
    for k in range(0, len(data), 2):
        data_dict[data[k]] = data[k+1]
    return (data_dict, j)


def parsing(texto, position = 0):
    '''Returns a dictionary with the metadata of the torrent'''

    if chr(texto[position]) == 'i':         #Parsing of integers
        return parse_integer(texto, position)

    if chr(texto[position]) == 'l':        #Parsing of lists
        return parse_list(texto, position)
                
    if chr(texto[position]) == 'd':       #Parsing of dictionaries
        return parse_dictionary(texto, position)
    
    raise ValueError(f"Invalid torrent encoding in byte character {position}")
    

if __name__ == "__main__":
    data = open("./Torrent_examples/prueba.torrent", "rb").read()
    data = open("./Torrent_examples/ubuntu-21.04-desktop-amd64.iso.torrent", "rb").read()
    torrent = parsing(data, 0)[0]
