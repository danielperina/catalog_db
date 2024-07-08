import mysql.connector

from secret_vars import USER, PASSWORD, HOST, DATABASE

import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

def conectar_bd():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

def resize_image(image: Image):
    max_size = width = canvas.winfo_width(), canvas.winfo_height()

    width, height = image.size
    
    if width > max_size[0] or height > max_size[1]:
        ratio = min(max_size[0] / width, max_size[1] / height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size)
    return image

def getfilename():
    # im.icursor(0)
    try:
        filename = filedialog.askopenfilename()
        im.delete(first=0, last=len(im.get()))
        im.insert(0, filename)
        original_image = Image.open(filename) #tk.PhotoImage(file=filename)
        # img = resize_image(img, (200, 200))
        # (100/img.width(), 100/img.height())
        # img = img.zoom(1,1)
        # img = img.subsample(img.width()//200, img.height()//200)

        resized_image = resize_image(original_image)
        photo = ImageTk.PhotoImage(resized_image)

        canvas.img = photo
        
        canvas.create_image((canvas.winfo_width() - resized_image.width) // 2, (canvas.winfo_height() - resized_image.height) // 2, anchor=NW, image=photo)
    except Exception as e:
        im.delete(0, len(im.get()))
        messagebox.showwarning("Erro", e)


def insert():
    
    nome_cient = nc.get()
    nome_pop = np.get()
    desc_bot = d_b.get()
    img_path = im.get()

    if not (nome_cient and nome_pop and desc_bot and img_path):
        messagebox.showwarning("Aviso", "Preencha todos os campos")
        return

    try:
        with open(img_path, "rb") as f:
            content = f.read()
        
        id_p.delete(0, len(id_p.get()))
        nc.delete(0, len(nc.get()))
        np.delete(0, len(np.get()))
        d_b.delete(0, len(d_b.get()))
        im.delete(0, len(im.get()))
        canvas.img = ""

        db = conectar_bd()
        cursor = db.cursor()
        sql = 'INSERT INTO planta (nomeCientifico, nomePopular, descricaoBotanica, imagem) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (nome_cient, nome_pop, desc_bot, content))
        db.commit()
        cursor.close()
        db.close()

        messagebox.showinfo("Info", "Planta inserida com sucesso!")
    
    except Exception as e:
        messagebox.showwarning("Erro", e)

def update():

    id_plant = id_p.get()
    nome_cient = nc.get()
    nome_pop = np.get()
    desc_bot = d_b.get()
    img_path = im.get()

    if not (nome_cient and nome_pop and desc_bot and img_path and id_plant):
        messagebox.showwarning("Aviso", "Preencha todos os campos")
        return

    try:
        with open(img_path, "rb") as f:
            content = f.read()
        
        id_p.delete(0, len(id_p.get()))
        nc.delete(0, len(nc.get()))
        np.delete(0, len(np.get()))
        d_b.delete(0, len(d_b.get()))
        im.delete(0, len(im.get()))
        canvas.img = ""

        db = conectar_bd()
        cursor = db.cursor()
        sql = "UPDATE planta SET nomeCientifico = %s, nomePopular = %s, descricaoBotanica=%s, imagem= %s WHERE idPlanta = %s;"
        cursor.execute(sql, (nome_cient, nome_pop, desc_bot, content, id_plant))
        db.commit()
        cursor.close()
        db.close()  

        messagebox.showinfo("Info", "Planta atualizada com sucesso!")
    
    except Exception as e:
        messagebox.showwarning("Erro", e)

win = tk.Tk()
win.title("Cadastrar planta")
win.geometry("520x210")
win.resizable(width=False, height=False)

# Carregando a imagem do ícone
icon_image = Image.open("resources\icon\icon.png")
icon_photo = ImageTk.PhotoImage(icon_image)

# Definindo o ícone da janela
win.iconphoto(False, icon_photo)

# id para atualizar
tk.Label(win, text="id (atualizar):").place(x=5, y=5)
id_p = tk.Entry(win, width=15)
id_p.place(x=115, y=5)

# Nome científico
tk.Label(win, text="Nome científico:").place(x=5, y=30)
nc = tk.Entry(win, width=30)
nc.place(x=115, y=30)

# Nome popular
tk.Label(win, text="Nome popular:").place(x=5, y=55)
np = tk.Entry(win, width=30)
np.place(x=115, y=55)

# Descrição botânica
tk.Label(win, text="Descrição Botânica:").place(x=5, y=80)
d_b = tk.Entry(win, width=30)
d_b.place(x=115, y=80)

# Imagem
tk.Label(win, text="Imagem:").place(x=5, y=105)
im = tk.Entry(win, width=30)
im.place(x=60, y=105)
tk.Button(win, text="Procurar", command=getfilename).place(x=250, y=105)


tk.Button(win, text="Inserir", command=insert).place(x=150, y=130)

tk.Button(win, text="Atualizar", command=update).place(x=145, y=160)

# print([i for i in tk.__dict__.keys() if not i.startswith("_")])

canvas = tk.Canvas(width=200, height=200, background="#bbb")
canvas.place(x=310, y=2)

win.mainloop()