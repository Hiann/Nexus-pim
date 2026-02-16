from fastapi import APIRouter, HTTPException, Query
from app.models import ProdutoSchema, ProdutoUpdate, ListaProdutosResponse
# Importamos as novas funções do service
from app.services import (
    criar_produto, 
    listar_produtos_avancado, 
    buscar_por_sku, 
    analise_de_catalogo,
    atualizar_produto_logica,
    deletar_produto_logica
)

router = APIRouter()

# --- POST: Criar ---
@router.post("/produtos/", response_model=ProdutoSchema, status_code=201)
def adicionar_produto(produto: ProdutoSchema):
    # Verifica se SKU já existe para evitar duplicidade
    if buscar_por_sku(produto.sku):
        raise HTTPException(status_code=400, detail="SKU já cadastrado.")
    return criar_produto(produto)

# --- GET: Listar com Filtros ---
@router.get("/produtos/", response_model=ListaProdutosResponse)
def get_produtos(
    # Query(...) define parâmetros opcionais na URL
    categoria: str = Query(None, description="Filtrar por nome da categoria"),
    min_preco: float = Query(None, description="Preço mínimo"),
    max_preco: float = Query(None, description="Preço máximo"),
    pagina: int = Query(1, ge=1, description="Número da página"),
    limite: int = Query(10, le=100, description="Itens por página (Max 100)")
):
    """
    Retorna lista de produtos com paginação e filtros.
    Exemplo: /produtos/?categoria=Gamer&min_preco=2000&max_preco=5000
    """
    return listar_produtos_avancado(categoria, min_preco, max_preco, pagina, limite)

# --- GET: Buscar UM produto ---
@router.get("/produtos/{sku}", response_model=ProdutoSchema)
def get_produto_unico(sku: str):
    produto = buscar_por_sku(sku)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# --- PUT: Atualizar ---
@router.put("/produtos/{sku}", response_model=ProdutoSchema)
def update_produto(sku: str, dados: ProdutoUpdate):
    """
    Atualiza dados de um produto existente.
    Envie apenas os campos que deseja alterar.
    """
    # Primeiro verifica se existe
    if not buscar_por_sku(sku):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    resultado = atualizar_produto_logica(sku, dados)
    return resultado

# --- DELETE: Remover ---
@router.delete("/produtos/{sku}", status_code=204)
def delete_produto(sku: str):
    """
    Remove um produto. Status 204 significa 'No Content' (sucesso sem corpo de resposta).
    """
    sucesso = deletar_produto_logica(sku)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return # Retorna vazio (204)

# --- GET: Analytics ---
@router.get("/analytics/geral")
def get_analise():
    """Retorna estatísticas de estoque e preços por categoria."""
    return analise_de_catalogo()