from secret_vars import USER, PASSWORD, HOST, DATABASE
import tkinter as tk
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
from io import BytesIO

# Conexão com o banco de dados MySQL
db_connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
db_cursor = db_connection.cursor()

# Função para exibir a imagem da planta selecionada
def exibir_imagem():
    item = tree.focus()  # obtém o item selecionado na TreeView
    if item:
        planta_id = tree.item(item, "text")
        db_cursor.execute("SELECT imagem FROM Planta WHERE idPlanta = %s", (planta_id,))
        imagem_blob = db_cursor.fetchone()[0]
        
        # Converter o blob em imagem
        imagem = Image.open(BytesIO(imagem_blob))
        imagem = imagem.resize((300, 300))  # ajustar tamanho da imagem conforme necessário
        
        # Converter imagem para o formato suportado pelo tkinter
        imagem_tk = ImageTk.PhotoImage(imagem)
        
        # Mostrar imagem no Canvas
        canvas_imagem.create_image(0, 0, anchor=tk.NW, image=imagem_tk)
        
        # Atualizar a referência da imagem para evitar garbage collection
        canvas_imagem.imagem_tk = imagem_tk

# Configuração da janela principal
root = tk.Tk()
root.title("Catálogo de Plantas")

# Frame para conter a TreeView e o Canvas
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Configuração da TreeView
tree = ttk.Treeview(frame, columns=("Nome Científico", "Nome Popular", "Descrição Botânica"))
tree.heading("#0", text="ID")
tree.heading("Nome Científico", text="Nome Científico")
tree.heading("Nome Popular", text="Nome Popular")
tree.heading("Descrição Botânica", text="Descrição Botânica")

# Scrollbar para a TreeView
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.config(yscrollcommand=scrollbar.set)

# Obtém dados do banco e popula a TreeView
db_cursor.execute("SELECT idPlanta, nomeCientifico, nomePopular, descricaoBotanica FROM Planta")
for row in db_cursor.fetchall():
    tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Canvas para mostrar a imagem da planta
canvas_imagem = tk.Canvas(root, width=300, height=300)
canvas_imagem.pack(side=tk.RIGHT, padx=10, pady=10)

# Botão "Visualizar"
btn_visualizar = tk.Button(root, text="Visualizar", command=exibir_imagem)
btn_visualizar.pack(pady=10)

# Loop principal da interface gráfica
root.mainloop()

# Fecha a conexão com o banco de dados
db_cursor.close()
db_connection.close()
