<div align="center">

# 💠 Nexus PIM
### Gestão de Produtos Enterprise com UX High-End e Inteligência de Dados

![Python Version](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Database](https://img.shields.io/badge/sqlite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-layout-e-ui">Layout</a> •
  <a href="#-como-executar">Instalação</a> •
  <a href="#-autor">Autor</a>
</p>

</div>

---

## 💡 Sobre o Projeto

O **Nexus PIM** (Product Information Management) é uma plataforma de gestão de catálogo de nível corporativo (*Enterprise*), desenvolvida para transcender os dashboards comuns. O projeto une a agilidade do **Python** com o poder de visualização do **Streamlit**, elevando a interface a um patamar "Sênior" através de injeção avançada de CSS e JavaScript.

O foco central foi criar uma experiência de **"Dark Glassmorphism"**, onde a gestão de inventário deixa de ser burocrática e se torna visual, fluida e acionável. O sistema gerencia todo o ciclo de vida do produto, desde a precificação automática até o monitoramento crítico de estoque.

---

## 🌟 Funcionalidades Principais

### 🖥️ Dashboard Executivo
- **KPIs Glass:** Cartões de indicadores (Total de Produtos, Patrimônio, Ticket Médio) com design translúcido.
- **Analytics Visual:** Gráficos interativos (Plotly) de Receita Estimada e Mix de Categorias com tooltips customizados (Dark Theme).
- **Monitoramento de Risco:** Tabela de "Alertas de Estoque" com barras de progresso visuais para identificar rupturas iminentes.

### 🛍️ Vitrine Premium (Catálogo)
- **Cards High-End:** Visualização de produtos inspirada em e-commerces de luxo, com efeitos de hover 3D, badges de status e barras de estoque integradas.
- **Filtros Dinâmicos:** O sistema lê os dados reais para ajustar automaticamente as faixas de preço (Min/Max) e categorias disponíveis.
- **Gestão Rápida:** Edição via Modal (Pop-up) e exclusão direta na vitrine, sem recarregar a página.

### ✨ Gestão de Produtos
- **Cadastro Inteligente:** Geração automática de SKUs baseada no nome e categoria do produto.
- **Precificação:** Cálculo automático de margem e validação de dados em tempo real.
- **Persistência Robusta:** Banco de dados SQLite local (`nexus.db`) garantindo que os dados sobrevivam a reinicializações.

### 🚀 UX/UI Avançada
- **Sidebar Retrátil:** Menu lateral inteligente com animação fluida e fechamento automático (JavaScript Injected).
- **Glassmorphism:** Uso intensivo de `backdrop-filter`, transparências e sombras suaves para um visual moderno e industrial.

---

## 🎨 Layout e UI (Design System)

O Nexus PIM utiliza um **Design System proprietário** injetado via CSS, focado na estética "Dark Enterprise".

| **Componente** | **Detalhes Técnicos** |
|:---:|:---|
| **Sidebar** | Efeito de vidro fosco (`blur 20px`), scrollbar invisível e comportamento responsivo via JS. |
| **Gráficos** | Configuração manual do **Plotly** para remover grids padrão e aplicar tooltips escuros com bordas arredondadas. |
| **Cards** | Design assimétrico com gradiente radial no fundo da imagem e tipografia hierárquica (Inter & JetBrains Mono). |

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído sobre uma pilha tecnológica moderna e eficiente para dados:

* **Core:** Python 3.10+
* **Framework Web:** Streamlit (com hacks de CSS/JS).
* **Visualização de Dados:** Plotly Express & Graph Objects.
* **Manipulação de Dados:** Pandas.
* **Banco de Dados:** SQLite3 (Nativo do Python).
* **Interface:** HTML5 & CSS3 (Injeção via `st.markdown`).
* **Exportação:** XlsxWriter (Relatórios Excel).

---

## 🚀 Como Executar

### Pré-requisitos
* Python 3.8 ou superior instalado.
* Git instalado.

### Passo a Passo

1.  **Clone o repositório**
    ```bash
    git clone [https://github.com/Hiann/nexus-pim.git](https://github.com/Hiann/nexus-pim.git)
    cd nexus-pim
    ```

2.  **Instale as dependências**
    ```bash
    pip install streamlit pandas plotly xlsxwriter streamlit-option-menu fastapi uvicorn pydantic
    ```

3.  **Execução (Atenção: Requer 2 Terminais)**
    Para o funcionamento completo (Backend + Frontend), você deve abrir dois terminais separados na pasta do projeto:

    * **Terminal 1 (Backend API):**
        ```bash
        uvicorn main:app --reload
        ```
        *Aguarde a mensagem "Application startup complete".*

    * **Terminal 2 (Frontend Streamlit):**
        ```bash
        streamlit run frontend.py
        ```

4.  **Acesse**
    * O sistema abrirá automaticamente em seu navegador padrão (geralmente `http://localhost:8501`).

---

## 📂 Estrutura de Pastas

```text
PIM_LITE/
├── app/                # Arquivos de cache e configuração interna
├── components.py       # 🧩 Componentes Visuais (Cards, KPIs, Gráficos)
├── frontend.py         # 🚀 Ponto de entrada do Frontend (Streamlit)
├── main.py             # ⚙️ Backend API (FastAPI)
├── nexus.db            # 🗄️ Banco de Dados SQLite (Gerado automaticamente)
├── requirements.txt    # Dependências do projeto
├── styles.py           # 🎨 Motor de CSS e Injeção de JavaScript
└── utils.py            # 🛠️ Funções utilitárias e conexão com API
```

📫 Autor
<div align="center">

**Hiann Alexander Mendes de Oliveira** *Desenvolvedor Backend & Entusiasta de IA*

<a href="https://www.linkedin.com/in/hiann-alexander" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-Conectar-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge">
</a>

</div>
