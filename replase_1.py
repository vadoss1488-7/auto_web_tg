def replace_characters():

    input_file = 'com.txt'
    output_file = 'coms.txt'

    replacements = {
        'А': 'A',
        'В': 'B',
        'Е': 'E',
        'К': 'K',
        'М': 'M',
        'Н': 'H',
        'О': 'O',
        'Р': 'P',
        'С': 'C',
        'Т': 'T',
        'У': 'Y',
        'Х': 'X'
    }

    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    for old, new in (replacements).items():
        text = text.replace(old, new)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

    print('заменено')
