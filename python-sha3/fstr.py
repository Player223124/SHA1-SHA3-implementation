# Считывание содержимого файла
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"
    
def string_to_num(string):
    decimal_string = ''.join(str(ord(char)) for char in string)
    return decimal_string

if __name__ == "__main__":
    path = 'message.txt'
    msg = read_file(path)
    print("Содержимое файла: ", msg)
    msg = string_to_num(msg)
    print ("Десятичный вид: ", msg)
