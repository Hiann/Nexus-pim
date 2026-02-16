from app.database import db
from app.models import ProdutoSchema, ProdutoUpdate
from pymongo import ReturnDocument # Usado para retornar o objeto já atualizado

# Referência à coleção 'produtos' dentro do banco
collection = db.produtos


def criar_produto(produto: ProdutoSchema):
    """Insere um novo produto no banco."""
    # Transforma o objeto Pydantic em um dicionário Python padrão
    produto_dict = produto.dict()
    
    # Insere no MongoDB
    collection.insert_one(produto_dict)
    
    # Retorna o dicionário para confirmar a criação na API
    return produto_dict

def listar_produtos_avancado(
    categoria: str = None, 
    min_preco: float = None, 
    max_preco: float = None, 
    pagina: int = 1, 
    limite: int = 10
):
    """
    Lista produtos com filtros dinâmicos e paginação.
    Isso é essencial para performance em e-commerces reais.
    """
    
    # 1. Construção da Query (Filtro)
    # Começamos com um dicionário vazio (traz tudo)
    query = {}
    
    # Se o usuário passou uma categoria, adicionamos ao filtro
    if categoria:
        # $regex com 'i' faz a busca ser Case Insensitive (ignora maiúscula/minúscula)
        query["categoria"] = {"$regex": categoria, "$options": "i"}
    
    # Filtro de Faixa de Preço (Range)
    if min_preco or max_preco:
        query["preco"] = {} # Cria um sub-objeto para o campo preço
        if min_preco:
            query["preco"]["$gte"] = min_preco # $gte = Greater Than or Equal (Maior ou igual)
        if max_preco:
            query["preco"]["$lte"] = max_preco # $lte = Less Than or Equal (Menor ou igual)

    # 2. Paginação (Pular registros)
    # Ex: Página 2 com limite 10 deve pular (skip) os primeiros 10 registros.
    pular = (pagina - 1) * limite

    # 3. Execução da Busca no Mongo
    # find(query) aplica os filtros
    # skip() pula os registros das páginas anteriores
    # limit() restringe a quantidade de resultados
    cursor = collection.find(query, {"_id": 0}).skip(pular).limit(limite)
    
    # Converte o cursor (iterador do banco) para uma lista em memória
    produtos = list(cursor)
    
    # Conta quantos itens existem no TOTAL para esse filtro (útil para o frontend saber quantas páginas criar)
    total_items = collection.count_documents(query)

    return {
        "produtos": produtos,
        "total": total_items,
        "pagina": pagina,
        "limite": limite
    }

def buscar_por_sku(sku: str):
    """Busca exata pelo código SKU."""
    return collection.find_one({"sku": sku}, {"_id": 0})

def atualizar_produto_logica(sku: str, dados_novos: ProdutoUpdate):
    """
    Atualiza um produto. Usa o operador $set do MongoDB para 
    alterar apenas os campos enviados, mantendo o resto intacto.
    """
    # exclude_unset=True remove campos que vieram como 'None' no JSON,
    # para não apagarmos dados acidentalmente no banco.
    dados_para_atualizar = dados_novos.dict(exclude_unset=True)

    if not dados_para_atualizar:
        return None # Nada para atualizar

    # Se houver especificações, precisamos tratar com cuidado para não apagar as antigas
    # O MongoDB permite "dot notation" para atualizar campos aninhados, mas aqui
    # faremos uma substituição do objeto de especificações ou merge via código se necessário.
    # Neste exemplo simples, substituímos o objeto 'especificacoes' se ele for enviado.
    
    # find_one_and_update é atômico (seguro para concorrência)
    resultado = collection.find_one_and_update(
        {"sku": sku},                 # Filtro: Quem vamos atualizar?
        {"$set": dados_para_atualizar}, # Operação: $set atualiza apenas os campos listados
        projection={"_id": 0},        # Não retornar o _id
        return_document=ReturnDocument.AFTER # Retorna o objeto JÁ alterado
    )
    
    return resultado

def deletar_produto_logica(sku: str):
    """Remove um produto do banco baseado no SKU."""
    resultado = collection.delete_one({"sku": sku})
    # deleted_count retorna 1 se deletou, 0 se não achou nada
    return resultado.deleted_count > 0

def analise_de_catalogo():
    """Aggregation Pipeline para estatísticas."""
    pipeline = [
        # $group: Agrupa documentos baseado no campo 'categoria'
        {
            "$group": {
                "_id": "$categoria",             # A chave do agrupamento
                "qtd_produtos": {"$sum": 1},     # Conta +1 para cada produto
                "media_preco": {"$avg": "$preco"}, # Calcula média aritmética
                "total_estoque": {"$sum": "$estoque"} # Soma o estoque total
            }
        },
        # $project: Formata a saída para ficar mais bonita (renomeia _id para categoria)
        {
            "$project": {
                "categoria": "$_id",
                "_id": 0,
                "qtd_produtos": 1,
                "media_preco": {"$round": ["$media_preco", 2]}, # Arredonda para 2 casas decimais
                "total_estoque": 1
            }
        },
        # $sort: Ordena por quantidade decrescente (-1)
        {"$sort": {"qtd_produtos": -1}}
    ]
    
    return list(collection.aggregate(pipeline))