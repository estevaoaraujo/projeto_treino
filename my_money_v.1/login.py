import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sqlite3

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x600")
        self.root.configure(bg="#d8e9e5")

        caminho_logo = os.path.join("img", "logo.png")

        logo_image = Image.open(caminho_logo)
        logo_image = logo_image.resize((300, 300), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        tk.Label(root, image=self.logo_photo, bg="#d8e9e5").pack(pady=20)

        tk.Label(root, text="Usuário:", bg="#d8e9e5").pack(pady=5)
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack(pady=5)

        tk.Label(root, text="Senha:", bg="#d8e9e5").pack(pady=5)
        self.entry_senha = tk.Entry(root, show="*")
        self.entry_senha.pack(pady=5)

        tk.Button(root, text="Entrar", command=self.fazer_login).pack(pady=10)
        tk.Button(root, text="Registrar", command=self.abrir_registro).pack(pady=5)

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # Conectar ao banco de dados e verificar as credenciais
        conn = sqlite3.connect(os.path.join("service", "finance.db"))
        cursor = conn.cursor()

        cursor.execute("SELECT senha FROM usuarios WHERE usuario=?", (usuario,))
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            senha_registrada = resultado[0]
            if senha == senha_registrada:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.abrir_home()
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    def abrir_home(self):
        from home import HomeApp
        for widget in self.root.winfo_children():
            widget.destroy()
        HomeApp(self.root)

    def abrir_registro(self):
        self.janela_registro = tk.Toplevel(self.root)
        self.janela_registro.title("Registrar")
        self.janela_registro.geometry("300x250")
        self.janela_registro.configure(bg="#d8e9e5")

        tk.Label(self.janela_registro, text="Novo Usuário:", bg="#d8e9e5").pack(pady=5)
        self.entry_novo_usuario = tk.Entry(self.janela_registro)
        self.entry_novo_usuario.pack(pady=5)

        tk.Label(self.janela_registro, text="Nova Senha:", bg="#d8e9e5").pack(pady=5)
        self.entry_nova_senha = tk.Entry(self.janela_registro, show="*")
        self.entry_nova_senha.pack(pady=5)

        tk.Label(self.janela_registro, text="Email:", bg="#d8e9e5").pack(pady=5)
        self.entry_email = tk.Entry(self.janela_registro)
        self.entry_email.pack(pady=5)

        tk.Button(self.janela_registro, text="Registrar", command=self.registrar).pack(pady=10)

    def registrar(self):
        novo_usuario = self.entry_novo_usuario.get()
        nova_senha = self.entry_nova_senha.get()
        email = self.entry_email.get()

        # Conectar ao banco de dados e salvar os dados do novo usuário
        conn = sqlite3.connect(os.path.join("service", "finance.db"))
        cursor = conn.cursor()

        # Criar a tabela 'usuarios' se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha, email) VALUES (?, ?, ?)",
                           (novo_usuario, nova_senha, email))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.janela_registro.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "O usuário já existe.")
        
        conn.close()







