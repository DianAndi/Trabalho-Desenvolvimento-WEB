from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui' 

# upload de imgs
UPLOAD_FOLDER = 'static/imagens_painel'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# bco de dados funcoes
def get_db_connection():
    conn = sqlite3.connect('site_content.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            line TEXT NOT NULL,
            image_filename TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))
    conn.commit()
    conn.close()

# p iniciar o banco de dados aqui
with app.app_context():
    init_db()

# as rotas p o front end

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_partial')
def index_partial():
    return render_template('index.html')

@app.route('/ambientes_partial')
def ambientes_partial():
    return render_template('ambientes.html')

@app.route('/materiais_partial')
def materiais_partial():
    return render_template('materiais.html')

@app.route('/contato_partial')
def contato_partial():
    return render_template('contato.html')


# autenticação

@app.route('/lojista', methods=['GET', 'POST'])
def lojista_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('painel'))
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', 'error')
    return render_template('lojista.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('lojista_page'))

# painel aqui

@app.route('/painel')
def painel():
    if not session.get('logged_in'):
        flash('Você precisa estar logado para acessar esta página.', 'error')
        return redirect(url_for('lojista_page'))

    conn = get_db_connection()
    contents = conn.execute('SELECT * FROM contents ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('painel.html', contents=contents)


# --- API endpoints crud

@app.route('/api/content', methods=['POST'])
def add_content():
    if not session.get('logged_in'):
        return jsonify({'message': 'Não autorizado'}), 401

    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    line = request.form.get('line')
    image_file = request.files.get('imagem')

    if not all([title, description, category, line]):
        return jsonify({'message': 'Todos os campos de texto são obrigatórios!'}), 400

    image_filename = None
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_filename = filename
        try:
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            return jsonify({'message': f'Erro ao salvar a imagem: {e}'}), 500
    else:
        return jsonify({'message': 'Envio de imagem inválido ou nenhum arquivo enviado.'}), 400 # Imagem é obrigatória para POST

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO contents (title, description, category, line, image_filename) VALUES (?, ?, ?, ?, ?)',
                     (title, description, category, line, image_filename))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        # caso tenha erro remove img
        if image_filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        return jsonify({'message': f'Erro ao adicionar conteúdo ao banco de dados: {e}'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Conteúdo adicionado com sucesso!', 'image_filename': image_filename}), 201


@app.route('/api/contents', methods=['GET'])
def get_contents():
    conn = get_db_connection()
    contents = conn.execute('SELECT * FROM contents ORDER BY id DESC').fetchall()
    conn.close()
    contents_list = [dict(row) for row in contents]
    return jsonify(contents_list)

# busca conteúdo por categoria
@app.route('/api/contents/category/<string:category_name>', methods=['GET'])
def get_contents_by_category(category_name):
    conn = get_db_connection()
    # Adc um '%' para buscar categorias
    contents = conn.execute('SELECT * FROM contents WHERE category = ? ORDER BY id DESC', (category_name,)).fetchall()
    conn.close()
    contents_list = [dict(row) for row in contents]
    return jsonify(contents_list)

# busca conteúdo por linha
@app.route('/api/contents/line/<string:line_name>', methods=['GET'])
def get_contents_by_line(line_name):
    conn = get_db_connection()
    contents = conn.execute('SELECT * FROM contents WHERE line = ? ORDER BY id DESC', (line_name,)).fetchall()
    conn.close()
    contents_list = [dict(row) for row in contents]
    return jsonify(contents_list)


@app.route('/api/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    if not session.get('logged_in'):
        return jsonify({'message': 'Não autorizado'}), 401

    conn = get_db_connection()
    content = conn.execute('SELECT * FROM contents WHERE id = ?', (content_id,)).fetchone()
    if not content:
        conn.close()
        return jsonify({'message': 'Conteúdo não encontrado!'}), 404

    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    line = request.form.get('line')
    image_file = request.files.get('imagem')

    if not all([title, description, category, line]):
        conn.close()
        return jsonify({'message': 'Todos os campos de texto são obrigatórios!'}), 400

    image_filename = content['image_filename']
    if image_file and allowed_file(image_file.filename):
       
        if image_filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        filename = secure_filename(image_file.filename)
        image_filename = filename
        try:
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
            return jsonify({'message': f'Erro ao salvar a nova imagem: {e}'}), 500


    try:
        conn.execute('UPDATE contents SET title = ?, description = ?, category = ?, line = ?, image_filename = ? WHERE id = ?',
                     (title, description, category, line, image_filename, content_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'message': f'Erro ao atualizar conteúdo no banco de dados: {e}'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Conteúdo atualizado com sucesso!'}), 200

@app.route('/api/content/<int:content_id>', methods=['DELETE'])
def delete_content(content_id):
    if not session.get('logged_in'):
        return jsonify({'message': 'Não autorizado'}), 401

    conn = get_db_connection()
    content = conn.execute('SELECT image_filename FROM contents WHERE id = ?', (content_id,)).fetchone()
    if not content:
        conn.close()
        return jsonify({'message': 'Conteúdo não encontrado!'}), 404

    image_filename = content['image_filename']

    try:
        conn.execute('DELETE FROM contents WHERE id = ?', (content_id,))
        conn.commit()
        
        if image_filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'message': f'Erro ao deletar conteúdo: {e}'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Conteúdo deletado com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)