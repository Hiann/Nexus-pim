import requests
import re
import streamlit as st
import pandas as pd
import io 
from datetime import datetime

API_URL = "http://localhost:8000"

# --- VALIDAÇÃO ---
class ProductValidator:
    @staticmethod
    def validate_sku(sku):
        if not sku: return False, "SKU obrigatório"
        if len(sku) < 2: return False, "Mín. 2 chars"
        return True, "Válido"

    @staticmethod
    def validate_price(price_str):
        if not price_str: return 0.0, False, "Obrigatório"
        # Limpa R$ e espaços
        clean = str(price_str).replace("R$", "").replace(" ", "").strip()
        try:
            # Suporta 1.200,50 e 1200.50
            if "," in clean and "." in clean: clean = clean.replace(".", "").replace(",", ".")
            elif "," in clean: clean = clean.replace(",", ".")
            val = float(clean)
            if val < 0: return 0.0, False, "Negativo"
            return val, True, "Válido"
        except: return 0.0, False, "Inválido"

# --- API ---
@st.cache_data(ttl=5, show_spinner=False)
def get_produtos():
    try:
        res = requests.get(f"{API_URL}/produtos/", timeout=2)
        return res.json().get("produtos", []) if res.status_code == 200 else []
    except: return []

def criar_produto(payload):
    try:
        res = requests.post(f"{API_URL}/produtos/", json=payload)
        if res.status_code in [200, 201]: get_produtos.clear()
        return res
    except: return None

def deletar_produto(sku):
    try:
        res = requests.delete(f"{API_URL}/produtos/{sku}")
        if res.status_code == 200: 
            get_produtos.clear()
            return True
        return False
    except: return False

def atualizar_produto(sku, payload):
    try:
        res = requests.put(f"{API_URL}/produtos/{sku}", json=payload)
        if res.status_code in [200, 204]: 
            get_produtos.clear()
            return True
        return False
    except: return False

def formatar_moeda(val):
    if not isinstance(val, (int, float)): return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_sku_sugestao(nome, categoria):
    import random
    if not nome: return ""
    prefix = categoria[:3].upper() if categoria else "GEN"
    part = "".join([w[:3] for w in nome.split()[:2]]).upper()
    return f"{prefix}-{part}-{random.randint(100, 999)}"

# --- EXPORTAÇÃO EXCEL "MASTERPIECE" ---
def converter_para_excel(data):
    output = io.BytesIO()

    # =========================================
    # 1. NORMALIZAÇÃO ABSOLUTA
    # =========================================

    if isinstance(data, pd.DataFrame):
        data = data.to_dict(orient="records")

    registros = []

    for item in data:
        registros.append({
            "SKU": str(item.get("sku", "SEM-SKU")),
            "Produto": str(item.get("nome", "Sem Nome")),
            "Categoria": str(item.get("categoria", "Geral")),
            "Preço Unitário": float(item.get("preco", 0) or 0),
            "Estoque": int(item.get("estoque", 0) or 0)
        })

    df = pd.DataFrame(registros)
    df["Total"] = df["Preço Unitário"] * df["Estoque"]

    patrimonio = df["Total"].sum()
    total_itens = df["Estoque"].sum()
    total_skus = len(df)

    # =========================================
    # 2. EXPORTAÇÃO PROFISSIONAL
    # =========================================

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        wb = writer.book
        ws = wb.add_worksheet("Relatório Executivo")

        # Remove grid
        ws.hide_gridlines(2)

        # =========================
        # DESIGN SYSTEM
        # =========================

        azul_escuro = "#0B1F3A"
        azul = "#1F4E79"
        cinza_bg = "#F4F6F9"
        verde = "#16A34A"

        # FORMATS
        fmt_title = wb.add_format({
            "bold": True,
            "font_size": 22,
            "font_name": "Segoe UI",
            "font_color": "white",
            "bg_color": azul_escuro,
            "align": "left",
            "valign": "vcenter"
        })

        fmt_sub = wb.add_format({
            "font_size": 10,
            "font_color": "#CBD5E1",
            "bg_color": azul_escuro
        })

        fmt_header = wb.add_format({
            "bold": True,
            "bg_color": azul,
            "font_color": "white",
            "align": "center",
            "valign": "vcenter",
            "border": 1
        })

        fmt_money = wb.add_format({
            "num_format": "R$ #,##0.00",
            "align": "right",
            "border": 1
        })

        fmt_center = wb.add_format({
            "align": "center",
            "border": 1
        })

        fmt_text = wb.add_format({
            "align": "left",
            "border": 1
        })

        fmt_kpi_label = wb.add_format({
            "font_size": 9,
            "font_color": "#64748B"
        })

        fmt_kpi_val = wb.add_format({
            "bold": True,
            "font_size": 14
        })

        fmt_kpi_money = wb.add_format({
            "bold": True,
            "font_size": 14,
            "font_color": verde,
            "num_format": "R$ #,##0.00"
        })

        # =========================
        # HEADER
        # =========================

        ws.merge_range("A1:F2", "RELATÓRIO EXECUTIVO DE INVENTÁRIO", fmt_title)
        ws.merge_range(
            "A3:F3",
            f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            fmt_sub
        )

        ws.set_row(0, 35)
        ws.set_row(1, 10)
        ws.set_row(2, 18)

        # =========================
        # KPIs
        # =========================

        #ws.write("A5", "PATRIMÔNIO TOTAL", fmt_kpi_label)
        #ws.write("A6", patrimonio, fmt_kpi_money)

        ws.write("C5", "TOTAL DE ITENS", fmt_kpi_label)
        ws.write("C6", total_itens, fmt_kpi_val)

        ws.write("E5", "SKUs ATIVOS", fmt_kpi_label)
        ws.write("E6", total_skus, fmt_kpi_val)

        # =========================
        # TABELA
        # =========================

        start_row = 8

        headers = list(df.columns)

        # Cabeçalhos
        for col, header in enumerate(headers):
            ws.write(start_row, col, header, fmt_header)

        # Dados
        for row_num, row in enumerate(df.values, start_row + 1):
            for col_num, value in enumerate(row):
                if col_num in [3, 5]:  # Preço e Total
                    ws.write(row_num, col_num, value, fmt_money)
                elif col_num == 4:
                    ws.write(row_num, col_num, value, fmt_center)
                else:
                    ws.write(row_num, col_num, value, fmt_text)

        # Total geral
        total_row = start_row + len(df) + 2
        ws.write(total_row, 4, "TOTAL GERAL:", fmt_header)
        ws.write_formula(
            total_row,
            5,
            f"=SUM(F{start_row+2}:F{start_row+1+len(df)})",
            fmt_money
        )

        # Ajuste de colunas
        ws.set_column("A:A", 18)
        ws.set_column("B:B", 40)
        ws.set_column("C:C", 20)
        ws.set_column("D:D", 18)
        ws.set_column("E:E", 12)
        ws.set_column("F:F", 18)

    return output.getvalue()
