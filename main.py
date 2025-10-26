from keccak import sha3
from fstr import write_file
from sha1 import sha1
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                out_text.config(state="normal")
                entry_path.config(state="normal")
                entry_path.delete(0, tk.END)
                entry_path.insert(tk.END, file_path)
                content = file.read()
                out_text.delete(1.0, tk.END)

                if radio_value.get() == "SHA-1":
                    print("Выбран алгоритм SHA-1")
                    print("Выбран файл ", file_path)

                    out_text.insert(tk.END, 'SHA-1 хеш: \n')
                    start_time = time.time()
                    content = sha1(content.encode()) 
                    end_time = time.time()
                    print("SHA-1 хеш файла: ", content)
                    out_text.insert(tk.END, content + "\n")
                    
                    path = file_path[:-4] + "_sha1.txt"
                    write_file(path, content)
                    out_text.insert(tk.END, "SHA-1 хеш записан в файл: " + path)
                    print("SHA-1 хеш сохранен в ", path)
                    print("Хеш был найден за ", end_time - start_time, " секунд")

                    



                elif radio_value.get() == "SHA-3":
                    print("Выбран алгоритм SHA-3")
                    print("Выбран файл ", file_path)

                    out_text.insert(tk.END, 'SHA-3 хеш: \n')
                    start_time = time.time()
                    content = sha3(content.encode())
                    end_time = time.time()

                    print("SHA-3 хеш файла: ", content)
                    out_text.insert(tk.END, content + "\n")

                    path = file_path[:-4] + "_sha3.txt"
                    write_file(path, content)
                    print("SHA-3 хеш сохранен в ", path)

                    out_text.insert(tk.END, "SHA-3 хеш записан в файл: " + path)
                    print("Хеш был найден за ", end_time - start_time, " секунд")

                out_text.config(state="disabled")
                entry_path.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file:\n{e}")



if __name__ == "__main__":
    # Главное окно
    root = tk.Tk()
    root.title("Хеширование файлов")
    root.geometry("455x200")

    # Поле вывода
    out_text = tk.Text(root, width=45)
    out_text.place(x=10, y=10, height=140)
    out_text.config(state="disabled")

    # Лейбл над полем выбора файла
    label1 = tk.Label(root, text='Выберите файл: ')
    label1.place(x=10, y=150)

    # Поле выбора файла
    entry_path = tk.Entry(root, width=60)
    entry_path.place(x=10, y=170)
    entry_path.config(state="disabled")

    # Кнопка выбора файла
    select_button = tk.Button(root, text="Открыть", command=select_file)
    select_button.place(x=375, y=170, width=70, height=20)

    # Радиокнопки
    radio_value = tk.StringVar()
    radio_value.set("SHA-1")  

    radio_button1 = tk.Radiobutton(root, text="SHA-1", variable=radio_value, value="SHA-1")
    radio_button1.place(x=375, y=10)

    radio_button2 = tk.Radiobutton(root, text="SHA-3", variable=radio_value, value="SHA-3")
    radio_button2.place(x=375, y=30)

    root.mainloop()

    # # Блок криптоанализа
    # alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # max_length = 20 # Максимальная длина проверяемого текста

    # # Брутфорс SHA-1
    # is_found = False
    # for length in range(1, max_length + 1):
    #     is_found = False
    #     for combination in itertools.product(alphabet, repeat=length):  
    #         mes = ''.join(combination)
    #         hash = sha1(mes.encode())
    #         print(mes, ': ', hash)

    #         if hash == res_hex:
    #             is_found = True
    #             break
    #     if is_found:
    #         print('Коллизия найдена при сообщении: ', mes)
    #         break
    # if not is_found:
    #     print('Коллизия не найдена ')
            
        