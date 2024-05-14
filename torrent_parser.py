from hashlib import sha1

def slice_text(text, length):
    '''Slices text'''
    return text[1:1+length]

def parse_integer(texto, position):
    '''Parses bencoded integer'''
    advance_step = 0
    entero = ''
    while chr(texto[position+advance_step]) in '0123456789':
        entero = entero + chr(texto[position + advance_step])
        advance_step += 1
    data = int(entero)

    return data, advance_step + 1

def parse_key(texto, position):
    '''Parses key of a bencoded dictionary/element of bencoded list'''
    length, new_advance_step = parse_integer(texto, position)
    new_element = slice_text(texto[position + new_advance_step - 1:], length)

    return new_element, length + new_advance_step - 1


def parse_list(texto, position):
    '''Parses bencoded list'''
    data = []
    advance_step = 0
    while chr(texto[position + advance_step]) != 'e':
        if chr(texto[position + advance_step]) in '0123456789':
            new_element , new_advance_step = parse_key(texto, position + advance_step)
        else:
            new_element, new_advance_step = decode_bencoding(texto, position + advance_step)

        advance_step += new_advance_step + 1
        data.append(new_element)

    return data, advance_step + 1

def parse_dictionary(texto, position):
    '''Parses bencoded dictionary'''
    data, position = parse_list(texto, position)

    data_dict =  dict([])
    for k in range(0, len(data), 2):
        data_dict[data[k]] = data[k+1]

    return data_dict, position

def create_info_hash(bencoded_dict):
    to_encode = bencoded_dict[b'info']
    byte_string = encode_bencoding(to_encode)
    bencoded_dict[b'info_hash'] = sha1(byte_string).digest()

def encode_int(decoded_elm):
    
    entero = str(decoded_elm)
    return b'i' + entero.encode('utf-8') + b'e'

def encode_byte(decoded_elm):

    length = str(len(decoded_elm))
    return length.encode('utf-8') + b':' + decoded_elm


def encode_list(decoded_elm):
    
    byte_string_output = b'l'

    for elm in decoded_elm:
        encoded = encode_bencoding(elm)
        byte_string_output += encoded 

    byte_string_output += b'e'

    return byte_string_output

def encode_dict(decoded_elm):
    key_list = decoded_elm.keys()
    values_list = decoded_elm.values()

    byte_string_output = b'd'

    for key, value in zip(key_list, values_list):
        byte_key = encode_bencoding(key)
        byte_value = encode_bencoding(value)
        byte_string_output += byte_key 
        byte_string_output += byte_value 

    byte_string_output += b'e'
    return byte_string_output

def encode_bencoding(decoded_elm):
    if isinstance(decoded_elm, dict):
        return encode_dict(decoded_elm)
    
    if isinstance(decoded_elm, list):
        return encode_list(decoded_elm)
    
    if isinstance(decoded_elm, int):
        return encode_int(decoded_elm)
    
    if isinstance(decoded_elm, bytes):
        return encode_byte(decoded_elm)
    
    raise ValueError(f"Cannot encode element.")

def decode_bencoding(texto, position = 0):
    '''Returns a dictionary with the metadata of the torrent'''

    if chr(texto[position]) == 'i':         #Parsing of integers
        return parse_integer(texto, position + 1)

    if chr(texto[position]) == 'l':        #Parsing of lists
        return parse_list(texto, position + 1)
                
    if chr(texto[position]) == 'd':       #Parsing of dictionaries
        return parse_dictionary(texto, position + 1)
    
    raise ValueError(f"Invalid torrent encoding in byte character {position}.")
    

if __name__ == "__main__":
    data = open("./Torrent_examples/prueba.torrent", "rb").read()
    data = open("./Torrent_examples/Okupas [Remasterizado HD 2021] (con música original).torrent", "rb").read()
    data = open("./Torrent_examples/big-buck-bunny.torrent", "rb").read()
    torrent = decode_bencoding(data, 0)[0]
    
