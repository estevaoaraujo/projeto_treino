import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import sqlite3
import os

DATABASE_FILE = os.path.join("service", "operacao.db")
CATEGORIAS_DB_FILE = os.path.join("service", "categoria.db")

class ReceitasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lançamentos Receitas")
        self.root.geometry("800x600")
        self.root.configure(bg="#d8e9e5")

        # Verifica se a tabela de categorias existe
        self.verificar_tabela_categorias()

        # Frame do menu
        self.frame_menu = tk.Frame(root, bg="#cfece7", height=100)
        self.frame_menu.pack(side="top", fill="x")

        self.adicionar_botao_menu("Home", "img/Home.png", self.voltar_home)
        self.adicionar_botao_menu("Financeiro", "img/receitas.png", highlight=True)
        self.adicionar_botao_menu("Relatório", "img/relatorio.png", self.abrir_relatorio)
        self.adicionar_botao_menu("Configurações", "img/configuracoes.png", self.abrir_configuracoes)
        self.adicionar_botao_menu("Sair", "img/sair.png", lambda: sair(self.root))

        # Frame do conteúdo
        self.frame_content = tk.Frame(root, bg="#edf6f3")
        self.frame_content.pack(side="top", fill="both", expand=True)

        titulo = tk.Label(self.frame_content, text="Lançamentos Receitas", font=("Arial", 16, "bold"), bg="#edf6f3")
        titulo.pack(pady=10)

        form_frame = tk.Frame(self.frame_content, bg="#edf6f3")
        form_frame.pack(pady=10)

        # Campos do formulário
        self.entries = {}
        labels = ["ID", "Operação", "Data", "Categoria", "Descrição", "R$"]
        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 12), bg="#edf6f3")
            label.grid(row=i, column=0, padx=20, pady=5, sticky="e")

            if label_text == "Data":
                entry = tk.Entry(form_frame)
                calendar_button = tk.Button(form_frame, text="📅", command=lambda e=entry: self.mostrar_calendario(e))
                entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                calendar_button.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            elif label_text == "Operação":
                self.operacao_var = tk.StringVar()
                check_receita = tk.Checkbutton(form_frame, text="Receita", variable=self.operacao_var, onvalue="Receita", offvalue="")
                check_despesa = tk.Checkbutton(form_frame, text="Despesa", variable=self.operacao_var, onvalue="Despesa", offvalue="")
                check_receita.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                check_despesa.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            elif label_text == "Categoria":
                self.categorias_var = tk.StringVar()
                categorias = self.buscar_categorias()
                print(categorias)  # Verifique se as categorias estão sendo carregadas
                entry = ttk.Combobox(form_frame, textvariable=self.categorias_var, values=categorias, state="readonly")
                entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
            else:
                entry = tk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                if label_text == "ID":
                    entry.insert(0, self.obter_proximo_id())  # Insere o próximo ID
                    entry.config(state="readonly")  # Torna o campo de ID somente leitura
            
            self.entries[label_text] = entry

        # Botão de salvar
        salvar_button = tk.Button(self.frame_content, text="SALVAR", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=20, pady=10, command=self.salvar_receita)
        salvar_button.pack(pady=20)

    def verificar_tabela_categorias(self):
        # Verifica se a tabela de categorias existe
        conn = sqlite3.connect(CATEGORIAS_DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def buscar_categorias(self):
        # Conecta ao banco de dados e busca as categorias disponíveis
        conn = sqlite3.connect(CATEGORIAS_DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT nome FROM categorias")
        categorias = [row[0] for row in cursor.fetchall()]
        print("Categorias encontradas:", categorias)  # Debug: verifique o que está sendo retornado

        conn.close()

        if not categorias:
            categorias = ["Nenhuma Categoria Disponível"]  # Adiciona uma opção padrão caso não existam categorias

        return categorias

    def mostrar_calendario(self, entry):
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20)

        def selecionar_data():
            entry.delete(0, tk.END)
            entry.insert(0, cal.get_date())
            top.destroy()

        tk.Button(top, text="Selecionar", command=selecionar_data).pack()

    def salvar_receita(self):
        nova_receita = {
            "id": self.entries["ID"].get(),
            "operacao": self.operacao_var.get(),
            "data": self.entries["Data"].get(),
            "categoria": self.categorias_var.get(),
            "descricao": self.entries["Descrição"].get(),
            "valor": self.entries["R$"].get()
        }

        # Conecta ao banco de dados e insere a nova receita
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO receitas (id, operacao, data, categoria, descricao, valor)
            VALUES (:id, :operacao, :data, :categoria, :descricao, :valor)
        ''', nova_receita)

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Receita salva com sucesso!")

        # Limpa os campos após salvar
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.config(state="normal")  # Habilita o campo para limpeza
                entry.delete(0, tk.END)
                if entry == self.entries["ID"]:
                    entry.insert(0, self.obter_proximo_id())  # Insere o próximo ID
                    entry.config(state="readonly")  # Torna o campo de ID somente leitura novamente
            elif isinstance(entry, ttk.Combobox):
                entry.set("")  # Reseta a seleção de categoria

    def obter_proximo_id(self):
        # Conecta ao banco de dados e busca o próximo ID
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Verifica se a tabela existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operacao TEXT,
                data TEXT,
                categoria TEXT,
                descricao TEXT,
                valor REAL
            )
        ''')

        cursor.execute("SELECT MAX(id) FROM receitas")
        ultimo_id = cursor.fetchone()[0]
        conn.close()

        if ultimo_id is not None:
            return ultimo_id + 1
        else:
            return 1  # Caso não haja registros

    def adicionar_botao_menu(self, texto, imagem_path, comando=None, highlight=False):
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((50, 50), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)
        botao = tk.Button(self.frame_menu, text=texto, image=imagem_tk, compound="top", bg="#cfece7", relief="flat", font=("Arial", 10), command=comando)
        botao.image = imagem_tk
        botao.pack(side="left", padx=10, pady=10)
        if highlight:
            botao.config(bg="#ffffff", font=("Arial", 10, "bold"))

    # Funções para navegação entre seções
    def voltar_home(self):
        from home import HomeApp
        for widget in self.root.winfo_children():
            widget.destroy()
        HomeApp(self.root)

    def abrir_relatorio(self):
        from relatorio import RelatorioApp
        for widget in self.root.winfo_children():
            widget.destroy()
        RelatorioApp(self.root)

    def abrir_configuracoes(self):
        from configurar import ConfiguracoesApp
        for widget in self.root.winfo_children():
            widget.destroy()
        ConfiguracoesApp(self.root)

def sair(root):
    root.quit()




