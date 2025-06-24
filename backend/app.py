# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'chave_senha_2025'


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
            flash('Login realizado com sucesso!', 'success')
           
            return redirect(url_for('painel'))
        else:
            flash('Usuário ou senha inválidos.', 'error')

   
    return render_template('lojista.html')

@app.route('/painel')
def painel():
    """A simple placeholder for the lojista's panel page."""
    
    return "<h1>Painel do Lojista</h1><p>Bem-vindo, admin!</p><p><a href='/'>Voltar ao site</a></p>"

if __name__ == '__main__':
    
    app.run(debug=True)
