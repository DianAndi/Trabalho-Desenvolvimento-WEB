# 🛋️ Projeto - Site para loja de móveis planejados

### 💡 Tema:
Sistema de gerenciamento de produtos para lojistas do ramo de móveis planejados. O sistema permite adicionar, editar e excluir produtos com campos como título, descrição, categoria, linha e imagem.

---

### :computer: Tecnologias Utilizadas:

- HTML5
- CSS3 puro (no futuro migrar para tailwind)
- JavaScript (puro + Fetch API)
- Python
- JSON para comunicação com o backend (Flask)

### 📕 Funcionalidades

- Exibir informações sobre a marca e os produtos
- Formulário de contato com validação HTML5
- Cadastro de produto com 5 campos: título, descrição, categoria, linha e imagem
- Renderização dinâmica e CRUD via backend flask
- Navegação entre páginas sem recarregar o site
- Identidade visual coerente com a proposta do projeto (fundo escuro, fonte clara e legível, layout minimalista)
- Layout responsivo e mobile first

### 📝 Requisitos

- Navegador moderno como Google Chrome, Firefox, etc
- Backend configurado e rodando
   * **Observação:** O código do backend (Python/Flask) deve estar na pasta raiz do projeto (`seu_projeto/app.py`) para que o aplicativo possa encontrar os templates e arquivos estáticos corretamente. Se o backend estiver em um repositório ou pasta separada, ele precisará ser movido ou ter seus caminhos configurados adequadamente.
  1.  (Se aplicável) Instale as dependências Python: `pip install -r requirements.txt`
  2.  Ative o ambiente virtual: `source venv/bin/activate` (Linux/macOS) ou `.\venv\Scripts\activate` (Windows PowerShell)
  3.  Execute o servidor Flask: `python app.py`


### 📃 Páginas

- Index: Página inicial do site, com apresentação da marca e chamada para navegação
- Ambientes: Galeria de ambientes planejados (cozinha, banheiro, etc.), com fotos e títulos
- Materiais: Mostra os materiais utilizados nos móveis, com imagens e descrições
- Contato: Formulário com campos validados via HTML5 para o cliente enviar mensagens
- Lojista: Painel exclusivo para lojistas, com CRUD de produtos integrados ao backend


