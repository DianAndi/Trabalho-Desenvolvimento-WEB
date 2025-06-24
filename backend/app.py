# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json 
import os   

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_aqui_escolha_uma_boa_chave_real'


UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'imagens')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


produtos_mock_db = []

next_product_id = 1


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index_partial')
def index_partial():
    
    return render_template('index.html') # O JS no navegador irá extrair apenas o <main>


@app.route('/ambientes_partial')
def ambientes_partial():
   
    return render_template('ambientes.html')

# Rota para o conteúdo parcial da página de Materiais
@app.route('/materiais_partial')
def materiais_partial():
    
    return render_template('materiais.html')


@app.route('/contato_partial')
def contato_partial():
    # O contato.html já contém apenas o conteúdo dentro do <main>
    return render_template('contato.html')



@app.route('/lojista', methods=['GET', 'POST'])
def lojista():
    """
    Lida com o login do lojista.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        
        
        if username == 'admin' and password == '1234':
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('painel'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    
   
    return render_template('lojista.html')

@app.route('/painel')
def painel():
    """
    Exibe o painel administrativo com a lista de produtos.
    """
    
    return render_template('painel.html', produtos=produtos_mock_db)

@app.route('/add_produto', methods=['POST'])
def add_produto():
    """
    Adiciona um novo produto ao sistema.
    """
    global next_product_id # Indica que vamos modificar a variável global

    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    categoria = request.form.get('categoria')
    linha = request.form.get('linha')
    imagem_file = request.files.get('imagem')
