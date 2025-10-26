from keccak import shake128_hex
from fstr import string_to_num, read_file
import itertools

if __name__ == "__main__":
    bytes_num = 32
    inp = read_file('message.txt')
    msg = string_to_num(inp)
    res_hex = shake128_hex(msg, bytes_num)
    print(res_hex)


    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # Максимальная длина комбинации
    max_length = 11  # например, 3 для демонстрации, можно увеличить по желанию

    # Перебор всех комбинаций от длины 1 до max_length
    for length in range(7, max_length + 1):
        is_found = False
        for combination in itertools.product(alphabet, repeat=length):  
            mes = ''.join(combination)
            print(mes)
            mes_dec = string_to_num(mes)
            if shake128_hex(mes_dec, bytes_num) == res_hex:
                is_found = True
        if is_found:
            print('Коллизия найдена при сообщении: ', mes)
            break
        else: 
            print('Коллизия не найдена')
        