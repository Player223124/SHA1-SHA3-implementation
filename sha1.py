def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def sha1(message):
    # Инициализация переменных
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # Дополнение сообщения
    original_message_bit_length = len(message) * 8
    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += original_message_bit_length.to_bytes(8, 'big')

    # Обработка блоков сообщения
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        words = [0]*80
        for j in range(16):
            words[j] = int.from_bytes(block[j*4:j*4+4], 'big')
        for j in range(16, 80):
            words[j] = left_rotate((words[j-3] ^ words[j-8] ^ words[j-14] ^ words[j-16]), 1)
        
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = left_rotate(a, 5) + f + e + k + words[j] & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
        
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    
    # Возвращение хеша
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

if __name__ == "__main__":
    input_string = input("Введите строку для вычисления SHA-1 хеша: ")
    sha1_hash = sha1(input_string.encode())
    print("SHA-1 хеш для введенной строки:", sha1_hash)