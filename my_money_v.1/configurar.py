import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import os

class ConfiguracoesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurações")
        self.root.geometry("800x600")
        self.root.configure(bg="#d8e9e5")

        self.frame_menu = tk.Frame(root, bg="#cfece7", height=100)
        self.frame_menu.pack(side="top", fill="x")

        self.adicionar_botao_menu("Home", "img/Home.png", self.voltar_home)
        self.adicionar_botao_menu("Financeiro", "img/receitas.png", self.abrir_receitas)
        self.adicionar_botao_menu("Relatório", "img/relatorio.png", self.abrir_relatorio)
        self.adicionar_botao_menu("Configurações", "img/configuracoes.png", highlight=True)
        self.adicionar_botao_menu("Sair", "img/sair.png", self.sair)

        self.frame_content = tk.Frame(root, bg="#edf6f3")
        self.frame_content.pack(side="top", fill="both", expand=True)

        titulo = tk.Label(self.frame_content, text="Configurações", font=("Arial", 16, "bold"), bg="#edf6f3")
        titulo.pack(pady=10)

        # Chama a função nome_usuario para exibir as informações do usuário
        self.nome_usuario()

        # Botões para cadastrar e alterar contas e categorias
        action_frame = tk.Frame(self.frame_content, bg="#edf6f3")
        action_frame.pack(pady=20)

        cadastrar_frame = tk.Frame(action_frame, bg="#edf6f3")
        cadastrar_frame.grid(row=0, column=0, padx=40)

        tk.Label(cadastrar_frame, text="Cadastrar", font=("Arial", 14), bg="#edf6f3").pack(anchor="w")

        tk.Button(cadastrar_frame, text="Categoria", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", padx=20, command=self.abrir_cadastro_categoria).pack(pady=10)

        alterar_frame = tk.Frame(action_frame, bg="#edf6f3")
        alterar_frame.grid(row=0, column=1, padx=40)

        # Cria a tabela se ela não existir
        self.criar_tabela_categorias()

    def nome_usuario(self):
        # Conectar ao banco de dados finance.db para buscar as informações do usuário
        conn = sqlite3.connect(os.path.join("service", "finance.db"))
        cursor = conn.cursor()

        # Supondo que o usuário esteja logado e você tenha o username para buscar
        username = "estevaoaraujo"  # Exemplo de username, pode ser ajustado para o contexto do seu app

        cursor.execute("SELECT usuario, senha, email FROM usuarios WHERE usuario=?", (username,))
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            usuario, senha, email = resultado
        else:
            usuario, senha, email = "Usuário não encontrado", "*******", "Email não encontrado"

        # Exibir as informações na interface
        user_frame = tk.Frame(self.frame_content, bg="#edf6f3")
        user_frame.pack(pady=10, padx=10, anchor="w")

        tk.Label(user_frame, text="Usuário:", font=("Arial", 12), bg="#edf6f3").grid(row=0, column=0, sticky="w")
        tk.Label(user_frame, text=usuario, font=("Arial", 12), bg="#edf6f3").grid(row=0, column=1, sticky="w")

        tk.Label(user_frame, text="Senha:", font=("Arial", 12), bg="#edf6f3").grid(row=1, column=0, sticky="w")
        tk.Label(user_frame, text="*******", font=("Arial", 12), bg="#edf6f3").grid(row=1, column=1, sticky="w")

        tk.Label(user_frame, text="Email:", font=("Arial", 12), bg="#edf6f3").grid(row=2, column=0, sticky="w")
        tk.Label(user_frame, text=email, font=("Arial", 12), bg="#edf6f3").grid(row=2, column=1, sticky="w")

        tk.Button(user_frame, text="Alterar", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", command=self.alterar_usuario).grid(row=3, column=0, columnspan=2, pady=10)

    def criar_tabela_categorias(self):
        # Criação da tabela 'categorias' caso ela não exista
        conn = sqlite3.connect(os.path.join("service", "categoria.db"))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def adicionar_botao_menu(self, texto, imagem_path, comando=None, highlight=False):
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((50, 50), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)
        botao = tk.Button(self.frame_menu, text=texto, image=imagem_tk, compound="top", bg="#cfece7", relief="flat", font=("Arial", 10), command=comando)
        botao.image = imagem_tk
        botao.pack(side="left", padx=10, pady=10)
        if highlight:
            botao.config(bg="#ffffff", font=("Arial", 10, "bold"))

    def alterar_usuario(self):
        # Função para alterar informações do usuário
        pass

    def cadastrar_conta(self):
        # Função para cadastrar conta
        pass

    def obter_proximo_id(self):
        # Função para buscar o último ID e calcular o próximo
        conn = sqlite3.connect(os.path.join("service", "categoria.db"))
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) FROM categorias")
        ultimo_id = cursor.fetchone()[0]

        conn.close()

        if ultimo_id is not None:
            return ultimo_id + 1
        else:
            return 1  # Caso não haja nenhum registro ainda

    def abrir_cadastro_categoria(self):
        # Criação de uma nova janela para cadastro de categorias
        self.cadastro_categoria_window = tk.Toplevel(self.root)
        self.cadastro_categoria_window.title("Cadastrar Categoria")
        self.cadastro_categoria_window.geometry("400x300")
        self.cadastro_categoria_window.configure(bg="#d8e9e5")

        proximo_id = self.obter_proximo_id()  # Obter o próximo ID

        tk.Label(self.cadastro_categoria_window, text="ID", font=("Arial", 12), bg="#d8e9e5").place(x=50, y=50)
        self.id_entry = tk.Entry(self.cadastro_categoria_window, font=("Arial", 12))
        self.id_entry.place(x=200, y=50, width=150)
        self.id_entry.insert(0, str(proximo_id))  # Inserir o próximo ID automaticamente

        tk.Label(self.cadastro_categoria_window, text="Categoria Nova", font=("Arial", 12), bg="#d8e9e5").place(x=50, y=100)
        self.categoria_entry = tk.Entry(self.cadastro_categoria_window, font=("Arial", 12))
        self.categoria_entry.place(x=200, y=100, width=150)

        tk.Button(self.cadastro_categoria_window, text="Efetivar", font=("Arial", 12, "bold"), bg="#6c757d", fg="white", command=self.salvar_categoria).place(x=150, y=200, width=100)

    def salvar_categoria(self):
        # Conexão com o banco de dados e salvamento da nova categoria
        id_categoria = self.id_entry.get()
        nome_categoria = self.categoria_entry.get()

        # Conectar ao banco de dados
        conn = sqlite3.connect(os.path.join("service", "categoria.db"))
        cursor = conn.cursor()

        # Inserir os valores na tabela 'categorias'
        cursor.execute("INSERT INTO categorias (id, nome) VALUES (?, ?)", (id_categoria, nome_categoria))

        conn.commit()
        conn.close()

        # Fecha a janela após salvar e retorna para configurações
        self.cadastro_categoria_window.destroy()
        self.root.deiconify()  # Garante que a tela principal retome o foco

    def voltar_home(self):
        from home import HomeApp
        for widget in self.root.winfo_children():
            widget.destroy()
        HomeApp(self.root)

    def abrir_receitas(self):
        from receita import ReceitasApp
        for widget in self.root.winfo_children():
            widget.destroy()
        ReceitasApp(self.root)

    def abrir_relatorio(self):
        from relatorio import RelatorioApp
        for widget in self.root.winfo_children():
            widget.destroy()
        RelatorioApp(self.root)

    def sair(self):
        self.root.quit()





