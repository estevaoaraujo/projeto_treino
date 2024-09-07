import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import os
from utils.utils import sair

DATABASE_FILE = os.path.join("service", "operacao.db")

class RelatorioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Relatório")
        self.root.geometry("800x600")
        self.root.configure(bg="#d8e9e5")

        self.frame_menu = tk.Frame(root, bg="#cfece7", height=100)
        self.frame_menu.pack(side="top", fill="x")

        self.adicionar_botao_menu("Home", "img/Home.png", self.voltar_home)
        self.adicionar_botao_menu("Financeiro", "img/receitas.png", self.abrir_receitas)
        self.adicionar_botao_menu("Relatório", "img/relatorio.png", highlight=True)
        self.adicionar_botao_menu("Configurações", "img/configuracoes.png", self.abrir_configuracoes)
        self.adicionar_botao_menu("Sair", "img/sair.png", lambda: sair(self.root))

        self.frame_content = tk.Frame(root, bg="#edf6f3")
        self.frame_content.pack(side="top", fill="both", expand=True)

        titulo = tk.Label(self.frame_content, text="Emissão Relatórios", font=("Arial", 16, "bold"), bg="#edf6f3")
        titulo.pack(pady=10)

        form_frame = tk.Frame(self.frame_content, bg="#edf6f3")
        form_frame.pack(pady=10)

        self.entries = {}
        labels = ["Data inicial", "Data final", "Categoria"]
        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 12), bg="#edf6f3")
            entry = tk.Entry(form_frame)
            if label_text in ["Data inicial", "Data final"]:
                calendar_button = tk.Button(form_frame, text="📅", command=lambda e=entry: self.mostrar_calendario(e))
                entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
                calendar_button.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            else:
                entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
            label.grid(row=i, column=0, padx=20, pady=5, sticky="e")
            self.entries[label_text] = entry

        emitir_button = tk.Button(self.frame_content, text="Emitir PDF", font=("Arial", 12, "bold"), bg="#4e3e8a", fg="white", padx=20, pady=10, command=self.emitir_pdf)
        emitir_button.pack(pady=20)

    def adicionar_botao_menu(self, texto, imagem_path, comando=None, highlight=False):
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((50, 50), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)
        botao = tk.Button(self.frame_menu, text=texto, image=imagem_tk, compound="top", bg="#cfece7", relief="flat", font=("Arial", 10), command=comando)
        botao.image = imagem_tk
        botao.pack(side="left", padx=10, pady=10)
        if highlight:
            botao.config(bg="#ffffff", font=("Arial", 10, "bold"))

    def mostrar_calendario(self, entry):
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20)

        def selecionar_data():
            entry.delete(0, tk.END)
            entry.insert(0, cal.get_date())
            top.destroy()

        tk.Button(top, text="Selecionar", command=selecionar_data).pack()

    def emitir_pdf(self):
        # Pedir o local de download do PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        # Obter dados do formulário
        data_inicial = self.entries["Data inicial"].get()
        data_final = self.entries["Data final"].get()
        categoria = self.entries["Categoria"].get()

        # Conectar ao banco de dados e buscar os registros
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT data, categoria, operacao, descricao, valor
            FROM receitas
            WHERE data BETWEEN ? AND ? AND categoria LIKE ?
            ORDER BY data
        ''', (data_inicial, data_final, f"%{categoria}%"))
        registros = cursor.fetchall()
        conn.close()

        # Calcular o saldo
        saldo = 0
        for registro in registros:
            operacao = registro[2]
            valor = registro[4]
            if operacao == "Receita":
                saldo += valor
            elif operacao == "Despesa":
                saldo -= valor

        # Gerar o PDF
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elementos = []

        # Adicionar título
        elementos.append(Paragraph("Relatório Financeiro", styles['Title']))

        # Adicionar tabela de registros
        tabela_dados = [["Data", "Categoria", "Operação", "Descrição", "Valor", "Saldo"]]
        saldo_acumulado = 0
        for registro in registros:
            data, categoria, operacao, descricao, valor = registro
            if operacao == "Receita":
                saldo_acumulado += valor
            elif operacao == "Despesa":
                saldo_acumulado -= valor
            tabela_dados.append([data, categoria, operacao, descricao, f"R${valor:.2f}", f"R${saldo_acumulado:.2f}"])

        tabela = Table(tabela_dados)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabela)

        # Adicionar saldo final
        elementos.append(Paragraph(f"Saldo Final: R${saldo_acumulado:.2f}", styles['Normal']))

        # Construir o PDF
        doc.build(elementos)

        messagebox.showinfo("Sucesso", f"PDF salvo em {file_path}!")

    def abrir_receitas(self):
        from receita import ReceitasApp
        for widget in self.root.winfo_children():
            widget.destroy()
        ReceitasApp(self.root)

    def abrir_configuracoes(self):
        from configurar import ConfiguracoesApp
        for widget in self.root.winfo_children():
            widget.destroy()
        ConfiguracoesApp(self.root)

    def voltar_home(self):
        from home import HomeApp
        for widget in self.root.winfo_children():
            widget.destroy()
        HomeApp(self.root)

