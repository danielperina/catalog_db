import mysql.connector # Para conexão com o mysql server

from secret_vars import USER, PASSWORD, HOST, DATABASE # Dados para acesso ao banco

# Lib tkinter para a interface gráfica
import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
from tkinter import messagebox

# Lib Pillow para manipulação de imagens
from PIL import Image, ImageTk

# Cores e fontes para a interface gráfica
MAINBGCOLOR = "#2B9468"
MAINFGCOLOR = "#ffffff"
MAINFONT = ("Courier New", 20, "bold")

MAINFRAMEBGCOLOR = "#F9F3E5"


# classe para adição de placeholder no componente Entry
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self): # insere o placeholder se a entry estiver vazia
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        #if not self.get():
        self.put_placeholder()

    def get(self): # pega o valor da entry
        if self['fg'] == self.placeholder_color:
            return ''
        else:
            return super().get()

    def reset(self): # deleta os dados escritos na entry
        self.delete(0, tk.END)
        self.focus()

def conectar_bd(): # retorna a conexão com o banco de dados
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

# verifica se o id é válido
def check_planta_id(planta_id: int) -> bool:
    
    db = conectar_bd()
    cursor = db.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM planta WHERE idPlanta = %s)"
    cursor.execute(query, (planta_id,))
    
    # Obter o resultado
    exists = cursor.fetchone()[0]
    
    cursor.close()
    db.close()

    return exists

# manipulação da imagem
def resize_image(image: Image):
    max_size = (img_canvas.winfo_width(), img_canvas.winfo_height())
    width, height = image.size

    # Calcular a proporção para redimensionar a imagem
    ratio = min(max_size[0] / width, max_size[1] / height)
    new_size = (int(width * ratio), int(height * ratio))
    
    resized_image = image.resize(new_size)
    
    # Criar um fundo (background) para a imagem redimensionada se necessário
    final_image = Image.new("RGBA", max_size, (128, 128, 128, 0))  # Fundo cinza (RGBA)
    final_image.paste(resized_image, ((max_size[0] - new_size[0]) // 2, (max_size[1] - new_size[1]) // 2))

    return final_image

# Obtém o diretório da imagem e insere no componente canvas
def getfilename():
    global img_canvas
    global img_dir
    try:
        filename = filedialog.askopenfilename()
        # im.delete(first=0, last=len(im.get()))
        # im.insert(0, filename)
        original_image = Image.open(filename)
        img_dir = filename

        resized_image = resize_image(original_image)
        photo = ImageTk.PhotoImage(resized_image)

        img_canvas.img = photo
        
        img_canvas.create_image((img_canvas.winfo_width() - resized_image.width) // 2, (img_canvas.winfo_height() - resized_image.height) // 2, anchor=NW, image=photo)
    except Exception as e:
        # im.delete(0, len(im.get()))
        messagebox.showwarning("Erro", e)

# Insere os dados na tabela planta
def insert():
    global nomeC, nomeP, desc, img_dir

    nome_cient = nomeC.get()
    nome_pop = nomeP.get()
    desc_bot = desc.get()
    img_path = img_dir

    if not (nome_cient and nome_pop and desc_bot):
        messagebox.showwarning("Aviso", "Preencha todos os campos")
        return

    if not img_path:
        messagebox.showwarning("Aviso", "Insira a imagem")
        return

    try:
        with open(img_path, "rb") as f:
            content = f.read()
        
        nomeP.reset()
        desc.reset()
        nomeC.reset()

        img_dir = ""
        img_canvas.img = ""

        db = conectar_bd()
        cursor = db.cursor()
        sql = "INSERT INTO planta (nomeCientifico, nomePopular, descricaoBotanica, imagem) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome_cient, nome_pop, desc_bot, content))
        db.commit()
        cursor.close()
        db.close()

        print(sql%(nome_cient, nome_pop, desc_bot, f"[MEDIUMBLOB {len(content)/1024:.2f}kB]"))

        messagebox.showinfo("Info", "Planta inserida com sucesso!")
    
    except Exception as e:
        messagebox.showwarning("Erro", e)

# Atualiza os dados da tabela planta
def update():
    global idP, nomeC, nomeP, desc, img_dir

    id_plant = idP.get()
    nome_cient = nomeC.get()
    nome_pop = nomeP.get()
    desc_bot = desc.get()
    img_path = img_dir

    
    if not id_plant:
        messagebox.showwarning("Aviso", "Preencha o campo id")
        return

    if not (nome_cient or nome_pop or desc_bot or img_path):
        messagebox.showwarning("Aviso", "Defina ao menos um atributo a ser atualizado")
        return

    if not check_planta_id(id_plant):
        messagebox.showwarning("Aviso", "O id fornecido é inválido")
        return
    
    try:
        db = conectar_bd()
        cursor = db.cursor()

        if nome_cient:
            sql = "UPDATE planta SET nomeCientifico = %s WHERE idPlanta = %s;"
            cursor.execute(sql, (nome_cient, id_plant))
            print(sql%(nome_cient, id_plant))
        if nome_pop:
            sql = "UPDATE planta SET nomePopular = %s WHERE idPlanta = %s;"
            cursor.execute(sql, (nome_pop, id_plant))
            print(sql%(nome_pop, id_plant))
        if desc_bot:
            sql = "UPDATE planta SET descricaoBotanica=%s WHERE idPlanta = %s;"
            cursor.execute(sql, (desc_bot, id_plant))
            print(sql%(desc_bot, id_plant))
        if img_path:
            with open(img_path, "rb") as f:
                content = f.read()

            sql = "UPDATE planta SET imagem= %s WHERE idPlanta = %s;"
            print(sql%(f"[MEDIUMBLOB {len(content)/1024:.2f}kB]", id_plant))
            cursor.execute(sql, (content, id_plant))
        
        db.commit()
        cursor.close()
        db.close()

        messagebox.showinfo("Info", "Planta atualizada com sucesso!")

        nomeC.reset()
        nomeP.reset()
        desc.reset()
        idP.reset()

        img_dir = ""
        img_canvas.img = ""
    
    except Exception as e:
        messagebox.showwarning("Erro", e)

# Frame de cadastro
def frame_insert():
    global main_frame
    global img_canvas
    global nomeC, nomeP, desc, img_dir

    main_frame.destroy()
    toggle_btn.configure(text="☰", command=toggle_menu)

    title_lb.configure(text="Cadastrar")

    main_frame = tk.Frame(root, bg=MAINFRAMEBGCOLOR)
    main_frame.pack(side=tk.TOP, fill=tk.X)
    main_frame.pack_propagate(False)
    main_frame.configure(height=root.winfo_height()-50)

    nomeC = PlaceholderEntry(main_frame, placeholder="Digite o nome científico")
    nomeC.pack(padx=10, pady=5)
    nomeC.configure(width=150)

    nomeP = PlaceholderEntry(main_frame, placeholder="Digite o nome popular")
    nomeP.pack(padx=10, pady=5)
    nomeP.configure(width=150)

    desc = PlaceholderEntry(main_frame, placeholder="Digite a descrição botânica")
    desc.pack(padx=10, pady=5)
    desc.configure(width=150)

    tk.Button(main_frame, text="Inserir imagem", command=getfilename).pack(padx=10, pady=5)
    tk.Button(main_frame, text="Cadastrar planta", command=insert).pack(padx=10, pady=5)

    img_canvas = tk.Canvas(main_frame, bg="gray", width=250, height=250)
    img_canvas.pack(padx=10, pady=10)

# Frame de Atualização
def frame_update():
    global main_frame
    global img_canvas
    global idP, nomeC, nomeP, desc, img_dir

    main_frame.destroy()
    title_lb.configure(text="Atualizar")
    toggle_btn.configure(text="☰", command=toggle_menu)

    main_frame = tk.Frame(root, bg=MAINFRAMEBGCOLOR)
    main_frame.pack(side=tk.TOP, fill=tk.X)
    main_frame.pack_propagate(False)
    main_frame.configure(height=root.winfo_height()-50)

    idP = PlaceholderEntry(main_frame, placeholder="Digite o id da planta")
    idP.pack(padx=10, pady=5)
    idP.configure(width=150)

    nomeC = PlaceholderEntry(main_frame, placeholder="Digite o nome científico")
    nomeC.pack(padx=10, pady=5)
    nomeC.configure(width=150)

    nomeP = PlaceholderEntry(main_frame, placeholder="Digite o nome popular")
    nomeP.pack(padx=10, pady=5)
    nomeP.configure(width=150)

    desc = PlaceholderEntry(main_frame, placeholder="Digite a descrição botânica")
    desc.pack(padx=10, pady=5)
    desc.configure(width=150)

    tk.Button(main_frame, text="Inserir imagem", command=getfilename).pack(padx=10, pady=5)
    tk.Button(main_frame, text="Atualizar planta", command=update).pack(padx=10, pady=5)

    img_canvas = tk.Canvas(main_frame, bg="gray", width=250, height=250)
    img_canvas.pack(padx=10, pady=10)

# Menu
def toggle_menu():
    
    def collapse_toggle_menu():
        toggle_btn.configure(text="☰", command=toggle_menu)
        toggle_menu_fm.destroy()
    
    toggle_menu_fm = tk.Frame(root, bg=MAINBGCOLOR)

    tk.Button(toggle_menu_fm, 
        text="Cadastrar",
        font=MAINFONT, bd=0, bg=MAINBGCOLOR, fg=MAINFGCOLOR, 
        activebackground=MAINBGCOLOR,
        activeforeground=MAINFGCOLOR,
        command=frame_insert
    ).place(x=20, y=20)

    tk.Button(toggle_menu_fm, 
        text="Atualizar",
        font=MAINFONT, bd=0, bg=MAINBGCOLOR, fg=MAINFGCOLOR, 
        activebackground=MAINBGCOLOR,
        activeforeground=MAINFGCOLOR,
        command=frame_update
    ).place(x=20, y=80)

    window_height = root.winfo_height()
    toggle_menu_fm.place(x=0, y=50, height=window_height, width=200)
    toggle_btn.configure(text="X", command=collapse_toggle_menu)

# Configurações da Janela
root = tk.Tk() # Janela
root.geometry("300x500") # Tamanho da janela
root.title("Plantas") # Título da janela
root.resizable(width=False, height=False) # Torna o tamanho fixo
icon = tk.PhotoImage(file='resources\\icon\\icon.png') # Obtém o ícone
root.iconphoto(True, icon) # Insere o ícone

# Layout da Janela

head_frame = tk.Frame(root, bg=MAINBGCOLOR, 
    highlightbackground=MAINFGCOLOR,
    highlightthickness=1)

toggle_btn = tk.Button(head_frame, text='☰', bg=MAINBGCOLOR, fg=MAINFGCOLOR,
    font=MAINFONT, bd=0, 
    activebackground=MAINBGCOLOR,
    activeforeground=MAINFGCOLOR,
    command=toggle_menu)

toggle_btn.pack(side=tk.LEFT)

title_lb = tk.Label(head_frame, text="Cadastrar", bg=MAINBGCOLOR, fg=MAINFGCOLOR,
    font=MAINFONT, bd=0)

title_lb.pack(side=tk.LEFT)

head_frame.pack(side=tk.TOP, fill=tk.X)
head_frame.pack_propagate(False)
head_frame.configure(height=50)

root.update_idletasks()

main_frame = tk.Frame(root, bg=MAINFRAMEBGCOLOR)
main_frame.pack(side=tk.TOP, fill=tk.X)
main_frame.pack_propagate(False)
main_frame.configure(height=root.winfo_height()-50)

idP = PlaceholderEntry(main_frame, placeholder="Digite o id da planta")

nomeC = PlaceholderEntry(main_frame, placeholder="Digite o nome científico")
nomeC.pack(padx=10, pady=5)
nomeC.configure(width=150)

nomeP = PlaceholderEntry(main_frame, placeholder="Digite o nome popular")
nomeP.pack(padx=10, pady=5)
nomeP.configure(width=150)

desc = PlaceholderEntry(main_frame, placeholder="Digite a descrição botânica")
desc.pack(padx=10, pady=5)
desc.configure(width=150)

tk.Button(main_frame, text="Inserir imagem", command=getfilename).pack(padx=10, pady=5)
tk.Button(main_frame, text="Cadastrar planta", command=insert).pack(padx=10, pady=5)

img_dir = ""

img_canvas = tk.Canvas(main_frame, bg="gray", width=250, height=250)
img_canvas.pack(padx=10, pady=10)


# Roda a janela
root.mainloop()
