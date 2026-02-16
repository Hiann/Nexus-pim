from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('nexus.db')
    cursor = conn.cursor()
    # Cria a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            sku TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL,
            url_imagem TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco ao ligar
init_db()

# --- MODELOS (Pydantic) ---
class Produto(BaseModel):
    sku: str
    nome: str
    categoria: str
    preco: float
    estoque: int
    url_imagem: Optional[str] = None

# --- ROTAS DA API ---

@app.get("/produtos/", response_model=dict)
def listar_produtos():
    conn = sqlite3.connect('nexus.db')
    conn.row_factory = sqlite3.Row # Para acessar colunas pelo nome
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conn.close()
    
    # Converte os dados do banco para o formato JSON
    produtos = [dict(row) for row in dados]
    return {"produtos": produtos}

@app.get("/produtos/{sku}", response_model=Produto)
def obter_produto(sku: str):
    conn = sqlite3.connect('nexus.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE sku = ?", (sku,))
    dado = cursor.fetchone()
    conn.close()
    
    if dado:
        return dict(dado)
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.post("/produtos/", status_code=201)
def criar_produto(produto: Produto):
    try:
        conn = sqlite3.connect('nexus.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (sku, nome, categoria, preco, estoque, url_imagem)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (produto.sku, produto.nome, produto.categoria, produto.preco, produto.estoque, produto.url_imagem))
        conn.commit()
        conn.close()
        return produto
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="SKU já existe.")

@app.delete("/produtos/{sku}")
def deletar_produto(sku: str):
    conn = sqlite3.connect('nexus.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE sku = ?", (sku,))
    # Verifica se deletou algo
    linhas_afetadas = cursor.rowcount
    conn.commit()
    conn.close()
    
    if linhas_afetadas == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto removido com sucesso"}

@app.put("/produtos/{sku}")
def atualizar_produto(sku: str, produto: Produto):
    conn = sqlite3.connect('nexus.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos 
        SET nome = ?, categoria = ?, preco = ?, estoque = ?, url_imagem = ?
        WHERE sku = ?
    """, (produto.nome, produto.categoria, produto.preco, produto.estoque, produto.url_imagem, sku))
    
    linhas_afetadas = cursor.rowcount
    conn.commit()
    conn.close()
    
    if linhas_afetadas == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto