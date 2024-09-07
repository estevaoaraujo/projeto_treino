import tkinter as tk
from PIL import Image, ImageTk
from utils.utils import sair  # Importe a função sair de utils.py
from relatorio import RelatorioApp
from receita import ReceitasApp
from configurar import ConfiguracoesApp  # Importe a classe ConfiguracoesApp

def sair(root):
    root.quit()

class HomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Controle Financeiro")
        self.root.geometry("800x600")
        self.root.configure(bg="#cfece7")

        self.criar_interface()

    def criar_interface(self):
        self.frame_menu = tk.Frame(self.root, bg="#cfece7", height=100)
        self.frame_menu.pack(side="top", fill="x")

        self.frame_content = tk.Frame(self.root, bg="#d8e9e5")
        self.frame_content.pack(side="top", fill="both", expand=True)

        self.adicionar_botao_menu("Home", "img/Home.png", self.voltar_home)
        self.adicionar_botao_menu("Financeiro", "img/receitas.png", self.abrir_receitas)
        self.adicionar_botao_menu("Relatório", "img/relatorio.png", self.abrir_relatorio)
        self.adicionar_botao_menu("Configurações", "img/configuracoes.png", self.abrir_configuracoes)
        self.adicionar_botao_menu("Sair", "img/sair.png", lambda: sair(self.root))

        self.criar_conteudo_principal()

    def adicionar_botao_menu(self, texto, imagem_path, comando=None):
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((50, 50), Image.Resampling.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)
        botao = tk.Button(self.frame_menu, text=texto, image=imagem_tk, compound="top", bg="#cfece7", relief="flat", font=("Arial", 10), command=comando)
        botao.image = imagem_tk
        botao.pack(side="left", padx=10, pady=10)

    def criar_conteudo_principal(self):
        saldo_label = tk.Label(self.frame_content, text="Saldo Atual R$ 1.000,00", font=("Arial", 16, "bold"), bg="#d8e9e5")
        saldo_label.pack(pady=10)
        
        visao_geral_frame = tk.Frame(self.frame_content, bg="#edf6f3", relief="solid", borderwidth=1)
        visao_geral_frame.pack(pady=10, padx=20, fill="both", expand=True)

        visao_geral_label = tk.Label(visao_geral_frame, text="Visão Geral", font=("Arial", 14, "bold"), bg="#edf6f3")
        visao_geral_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        receitas_label = tk.Label(visao_geral_frame, text="Receitas", font=("Arial", 12), bg="#edf6f3")
        receitas_label.grid(row=1, column=0, sticky="w", padx=10)

        receitas_valor_label = tk.Label(visao_geral_frame, text="R$ 2.000,00", font=("Arial", 12), bg="#edf6f3")
        receitas_valor_label.grid(row=1, column=1, sticky="e", padx=10)

        despesas_label = tk.Label(visao_geral_frame, text="Despesas", font=("Arial", 12), bg="#edf6f3")
        despesas_label.grid(row=2, column=0, sticky="w", padx=10)

        despesas_valor_label = tk.Label(visao_geral_frame, text="R$ 1.000,00", font=("Arial", 12), bg="#edf6f3")
        despesas_valor_label.grid(row=2, column=1, sticky="e", padx=10)

        # Exemplo de tabela de dados
        tabela_frame = tk.Frame(visao_geral_frame, bg="#edf6f3")
        tabela_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tabela_texto = tk.Text(tabela_frame, height=10, width=60, bg="#edf6f3")
        tabela_texto.pack()

        # Adicionando conteúdo fictício na tabela
        tabela_texto.insert(tk.END, "DATA       OPERAÇÃO            CATEGORIA         DEBITO      CREDITO     SALDO\n")
        tabela_texto.insert(tk.END, "01/08/2024 Merceria Feliz      Supermercados     R$ 550,00   R$ 0,00    R$ 120,00\n")
        tabela_texto.insert(tk.END, "02/08/2024 Empresa Matrix      Salário           R$ 0,00     R$ 2.000,00R$ 1.670,00\n")
        tabela_texto.insert(tk.END, "03/08/2024 Shopping            Diversão          R$ 670,00   R$ 0,00    R$ 1.000,00\n")    

    def abrir_receitas(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ReceitasApp(self.root)


    def abrir_relatorio(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        RelatorioApp(self.root)

    def abrir_configuracoes(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ConfiguracoesApp(self.root)

    def voltar_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.criar_interface()












