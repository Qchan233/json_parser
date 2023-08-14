current = 0
previous = 0

def json_parser(string:str):
    return parse_element(string)

def parse_element(string:str):
    return parse_value(string)

def parse_value(string:str):
    global current
    global previous
    skip_whitespace(string)
    value = None
    if current == len(string):
        return None
    match(string[current]):
        case '"':
            value = parse_string(string)
        case 't':
            value =  parse_true(string)
        case 'f':
            value =  parse_false(string)
        case '[':
            value =  parse_array(string)
        case '{':
            value =  parse_object(string)
        case 'n':
            value = parse_null(string)
        case _:
            if string[current] in ['\n', '\t', ' ', '\r']:
                skip_whitespace(string)
            if string[current].isdigit() or string[current] == '-':
                value = parse_number(string)
            else:
                raise ValueError("Invalid value")
    skip_whitespace(string)
    return value

def match(string, substring):
    global current
    global previous
    length = len(substring)
    if current >= len(string):
        return False
    if string[current:current+length] == substring:
        current += length
        previous = current
        return True
    else:
        return False 

def peek(string, char):
    global current
    global previous
    if current >= len(string):
        return False
    if string[current] == char:
        return True
    else:
        return False

def skip_whitespace(string:str):
    global current
    global previous
    length = len(string)
    while current < length and string[current] in ['\n', '\t', ' ', '\r']:
        current += 1
    previous = current

def parse_string(string:str):
    global current 
    global previous
    current += 1
    previous = current
    while string[current] != '"':
        current += 1
    
    content = string[previous:current]
    match(string, '"')
    previous = current
    return content

def parse_true(string:str):
    global current
    global previous
    if string[current:current+4] == 'true':
        current += 4
        previous = current
        return True
    else:
        raise ValueError("Invalid value")
    
def parse_false(string:str):
    global current
    global previous
    if string[current:current+5] == 'false':
        current += 5
        previous = current
        return False
    else:
        raise ValueError("Invalid value")

def parse_null(string:str):
    global current
    global previous
    if string[current:current+4] == 'null':
        current += 4
        previous = current
        return None
    else:
        raise ValueError("Invalid value")

def parse_number(string:str):
    global current
    global previous
    length = len(string)
    while current < length and string[current].isdigit():
        current += 1
    
    if(peek(string, '.')):
        current += 1
        while current < length and string[current].isdigit():
            current += 1    

    num = float(string[previous:current])
    previous = current

    if(match(string, 'e') or match(string, 'E')):
        if(peek(string, '+') or peek(string, '-')):
            current += 1
        while current < length and string[current].isdigit():
            current += 1
        exp = int(string[previous:current])
        num = num * (10 ** exp)
        previous = current
    return num


def parse_object(string:str):
    global current
    global previous
    current += 1

    members = parse_members(string)
    skip_whitespace(string)
    if not match(string, '}'):
        raise ValueError("Unpaired braces")
    skip_whitespace(string)
    return members

def parse_array(string:str):
    global current
    global previous
    current += 1
    elements = parse_elements(string)
    skip_whitespace(string)
    if not match(string, ']'):
        raise ValueError("Unpaired brackets")
    skip_whitespace(string)
    return elements

def parse_elements(string:str):
    global current
    global previous
    elements = []
    skip_whitespace(string)
    if peek(string, ']'):
        return elements
    while True:
        elements.append(parse_value(string))
        if not match(string, ','):
            break
        skip_whitespace(string)
    return elements

def parse_members(string: str):
    global current
    global previous
    members = {}
    skip_whitespace(string)
    if peek(string, '}'):
        return members
    while True:
        key = parse_value(string)
        if not match(string, ':'):
            raise ValueError("Missing colon")
        value = parse_value(string)
        members[key] = value
        if not match(string, ','):
            break
        skip_whitespace(string)
    return members

if __name__ == "__main__":
    example = ' '
print(json_parser(example))