import tkinter as tk
from tkinter import filedialog, messagebox
import os

def hide_text_gui():
    def hide():
        carrier_path = carrier_entry.get()
        secret_path = secret_entry.get()
        output_path = output_entry.get()

        if not carrier_path or not secret_path or not output_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите все необходимые файлы и укажите путь для сохранения.")
            return

        try:
            with open(carrier_path, 'r') as cf, open(secret_path, 'r', encoding='utf-8') as sf, open(output_path, 'w', encoding='utf-8') as of:
                secret_data = ''.join(format(ord(c), '08b') for c in sf.read())
                secret_index = 0

                for line in cf:
                    modified_line = line.rstrip()

                    if secret_index < len(secret_data):
                        bit = secret_data[secret_index]
                        if bit == '1':
                            modified_line += ' '
                        secret_index += 1

                    of.write(modified_line + '\n')

                if secret_index < len(secret_data):
                    messagebox.showwarning("Внимание", "Не удалось полностью скрыть сообщение. Длина сообщения превышает вместимость файла-контейнера.")
                else:
                    messagebox.showinfo("Успех", f"Сообщение успешно скрыто в файле:\n{output_path}")

        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Один из файлов не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def browse_carrier():
        filepath = filedialog.askopenfilename()
        carrier_entry.delete(0, tk.END)
        carrier_entry.insert(0, filepath)

    def browse_secret():
        filepath = filedialog.askopenfilename()
        secret_entry.delete(0, tk.END)
        secret_entry.insert(0, filepath)

    def browse_output():
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        output_entry.delete(0, tk.END)
        output_entry.insert(0, filepath)

    window = tk.Tk()
    window.title("Стеганография в тексте (скрытие)")

    carrier_label = tk.Label(window, text="Файл-контейнер:")
    carrier_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    carrier_entry = tk.Entry(window, width=50)
    carrier_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    carrier_button = tk.Button(window, text="Обзор", command=browse_carrier)
    carrier_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    secret_label = tk.Label(window, text="Файл с секретным сообщением:")
    secret_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    secret_entry = tk.Entry(window, width=50)
    secret_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    secret_button = tk.Button(window, text="Обзор", command=browse_secret)
    secret_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")

    output_label = tk.Label(window, text="Сохранить как (стегофайл):")
    output_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    output_entry = tk.Entry(window, width=50)
    output_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    output_button = tk.Button(window, text="Обзор", command=browse_output)
    output_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")

    hide_button = tk.Button(window, text="Скрыть текст", command=hide)
    hide_button.grid(row=3, column=0, columnspan=3, pady=10)

    window.grid_columnconfigure(1, weight=1)
    window.mainloop()

def extract_text_gui():
    def extract():
        stego_path = stego_entry.get()
        output_path = output_entry.get()

        if not stego_path or not output_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите стегофайл и укажите путь для сохранения извлеченного сообщения.")
            return

        try:
            with open(stego_path, 'r', encoding='utf-8') as sf, open(output_path, 'w', encoding='utf-8') as of:
                binary_message = ''
                for line in sf:
                    if line.endswith(' \n') or line.endswith(' \r\n'):
                        binary_message += '1'
                    else:
                        binary_message += '0'

                extracted_message = ''
                for i in range(0, len(binary_message), 8):
                    byte = binary_message[i:i + 8]
                    if len(byte) == 8:
                        try:
                            extracted_message += chr(int(byte, 2))
                        except ValueError:
                            messagebox.showwarning("Предупреждение", f"Некорректный байт: {byte}")
                            continue
                    else:
                        break

                of.write(extracted_message)
                messagebox.showinfo("Успех", f"Сообщение успешно извлечено и сохранено в файле:\n{output_path}")

        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Стегофайл не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def browse_stego():
        filepath = filedialog.askopenfilename()
        stego_entry.delete(0, tk.END)
        stego_entry.insert(0, filepath)

    def browse_output():
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        output_entry.delete(0, tk.END)
        output_entry.insert(0, filepath)

    window = tk.Tk()
    window.title("Стеганография в тексте (извлечение)")

    stego_label = tk.Label(window, text="Стегофайл:")
    stego_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    stego_entry = tk.Entry(window, width=50)
    stego_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    stego_button = tk.Button(window, text="Обзор", command=browse_stego)
    stego_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    output_label = tk.Label(window, text="Сохранить извлеченное сообщение как:")
    output_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    output_entry = tk.Entry(window, width=50)
    output_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    output_button = tk.Button(window, text="Обзор", command=browse_output)
    output_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")

    extract_button = tk.Button(window, text="Извлечь текст", command=extract)
    extract_button.grid(row=2, column=0, columnspan=3, pady=10)

    window.grid_columnconfigure(1, weight=1)
    window.mainloop()

if __name__ == "__main__":
    mode = input("Выберите режим (hide/extract): ").lower()
    if mode == "hide":
        hide_text_gui()
    elif mode == "extract":
        extract_text_gui()
    else:
        print("Неверный режим. Используйте 'hide' или 'extract'.")