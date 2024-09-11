import json
import os
from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
import pyperclip

history_file="upload_history.json"


def save_history(filepath, download_link):
   history=[]
   if os.path.exists(history_file):
       with open(history_file,"r") as file:
           history =json.load(file)
   history.append({"filepath": os.path.basename(filepath), "download_link": download_link})
   with open(history_file, "w") as file:
       json.dump(history,file, indent=4)


def upload():
  try:
       filepath=fd.askopenfilename()
       if filepath:
           with open(filepath,'rb') as f:
               files={'file': f}
               response=requests.post("https://file.io", files=files)
               response.raise_for_status()
               download_link=response.json().get("link")
               if download_link:
                   entry.delete(0,END)
                   entry.insert(0,download_link)
                   pyperclip.copy(download_link)
                   save_history(filepath, download_link)
                   mb.showinfo("Ссылка скопирована","Ссылка успешно скопирована в буфер обмена")
               else:
                   raise ValueError("Не удалось получить ссылку для скачивания")
  except Exception as e2:
       mb.showerror("Ошибка", f"Произошла ошибка: {e2}")
def show_history():
   if not os.path.exists(history_file):
       mb.showinfo("История", "История загрузок пуста")
       return
   history_window=Toplevel(window)
   history_window.title('История загрузок')
   files_listbox=Listbox(history_window,width=50,height=20)
   files_listbox.grid(row=0,column=0,padx=(10,0),pady=10)
   links_listbox = Listbox(history_window, width=50, height=20)
   links_listbox.grid(row=0, column=1, padx=(0, 10), pady=10)
   with open(history_file,'r') as f:
       history=json.load(f)
       for item in history:
           files_listbox.insert(END,item['filepath'])
           links_listbox.insert(END,item['download_link'])
window=Tk()
window.title("Сохранение файлов в облаке")
window.geometry("200x150")

upload_button=ttk.Button(text="Загрузить файл", command=upload)
upload_button.pack()

entry=ttk.Entry()
entry.pack()
history_button=ttk.Button(text='Показать историю',command=show_history)
history_button.pack()
window.mainloop()


