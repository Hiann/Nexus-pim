from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Dict, Any, Optional, List

# URL de uma imagem "padrão" bonita caso o usuário não envie foto
IMAGEM_PADRAO = "https://placehold.co/600x400/1e1e1e/FFF?text=Produto+sem+Foto"

class ProdutoSchema(BaseModel):
    # O SKU identifica o produto. Min_length evita códigos vazios.
    sku: str = Field(..., min_length=3, example="NB-DELL-G15", description="Código único do produto")
    
    nome: str = Field(..., min_length=2, example="Notebook Dell G15")
    
    categoria: str = Field(..., example="Eletronicos")
    
    # Preço deve ser maior que zero (gt = Greater Than)
    preco: float = Field(..., gt=0, example=5200.00)
    
    # Estoque não pode ser negativo (ge = Greater or Equal)
    estoque: int = Field(default=0, ge=0)
    
    # Campo de Imagem Opcional. Se não vier, usamos o validador abaixo para preencher.
    url_imagem: Optional[str] = Field(default=IMAGEM_PADRAO)
    
    # Dicionário para guardar as especificações extras (Cor, Voltagem, Tamanho...)
    especificacoes: Dict[str, Any] = Field(default_factory=dict)

    # --- VALIDAÇÃO AUTOMÁTICA ---
    @validator('url_imagem', pre=True, always=True)
    def set_imagem_padrao(cls, v):
        # Se o valor for vazio, nulo ou string vazia, retorna a imagem padrão
        if not v or v == "string" or len(v) < 5:
            return IMAGEM_PADRAO
        return v
        
# Modelo para atualização (quando editamos um produto)
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None
    url_imagem: Optional[str] = None
    especificacoes: Optional[Dict[str, Any]] = None

class ListaProdutosResponse(BaseModel):
    produtos: List[ProdutoSchema]