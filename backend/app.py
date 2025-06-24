import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'chavesecretaAqui'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_filename = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Content('{self.title}', '{self.image_filename}')"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_filename': self.image_filename
        }


with app.app_context():
    db.create_all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/api/content', methods=['GET'])
def get_all_content():
    all_content = Content.query.all()
    return jsonify([item.to_dict() for item in all_content])

@app.route('/api/content', methods=['POST'])
def create_content():
    title = request.form.get('title')
    description = request.form.get('description')
    image_file = request.files.get('image')
    image_filename = None

    if not title:
        return jsonify({'message': 'Título é obrigatório'}), 400

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_filename = filename
    elif image_file:
        return jsonify({'message': 'Tipo de arquivo de imagem não permitido'}), 400

    new_content = Content(
        title=title,
        description=description,
        image_filename=image_filename
    )
    db.session.add(new_content)
    db.session.commit()
    return jsonify(new_content.to_dict()), 201

@app.route('/api/content/<int:content_id>', methods=['GET'])
def get_content(content_id):
    """Recupera um único item de conteúdo por ID."""
    content_item = Content.query.get_or_404(content_id)
    return jsonify(content_item.to_dict())

@app.route('/api/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    """Atualiza um item de conteúdo existente."""
    content_item = Content.query.get_or_404(content_id)

    title = request.form.get('title')
    description = request.form.get('description')
    image_file = request.files.get('image')
    
    if title:
        content_item.title = title
    if description is not None:
        content_item.description = description

    if image_file and allowed_file(image_file.filename):
        if content_item.image_filename:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], content_item.image_filename)
            if os.path.exists(old_path):
                os.remove(old_path)
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        content_item.image_filename = filename
    elif image_file and not allowed_file(image_file.filename):
        return jsonify({'message': 'Tipo de arquivo de imagem não permitido'}), 400
    elif request.form.get('remove_image') == 'true':
        if content_item.image_filename:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], content_item.image_filename)
            if os.path.exists(old_path):
                os.remove(old_path)
        content_item.image_filename = None

    db.session.commit()
    return jsonify(content_item.to_dict())

@app.route('/api/content/<int:content_id>', methods=['DELETE'])
def delete_content(content_id):
    """Deleta um item de conteúdo."""
    content_item = Content.query.get_or_404(content_id)
    if content_item.image_filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], content_item.image_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(content_item)
    db.session.commit()
    return jsonify({'message': 'Conteúdo deletado com sucesso'}), 204



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

@app.route('/lojista', methods=['GET', 'POST'])
def lojista():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('painel'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    return render_template('lojista.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('lojista'))

@app.route('/painel')
def painel():
    
    if not session.get('logged_in'):
        flash('Por favor, faça login para acessar esta página.', 'warning')
        return redirect(url_for('lojista'))
    return render_template('painel.html')


if __name__ == '__main__':
    app.run(debug=True)
