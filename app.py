from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import sqlite3
from database import criar_tabela, adicionar_usuario, verificar_usuario, adicionar_formulario

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para flash messages

# Inicializando banco de dados
criar_tabela()

# Função para verificar o CNPJ usando a ReceitaWS
def verificar_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        if dados.get('status') == 'OK':
            return True  # CNPJ válido
    return False  # CNPJ inválido ou não encontrado

@app.route('/')
def home():
    return render_template('login.htm')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        cnpj = request.form['cnpj']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar-senha']
        
        # Verificação de CNPJ
        if not verificar_cnpj(cnpj):
            flash('CNPJ inválido ou não encontrado!', 'error')
            return redirect(url_for('registrar'))

        # Verificação de senha
        if len(senha) < 6:
            flash('A senha deve ter no mínimo 6 caracteres.', 'error')
            return redirect(url_for('registrar'))

        if senha != confirmar_senha:
            flash('As senhas não conferem!', 'error')
            return redirect(url_for('registrar'))

        # Adicionar ao banco de dados
        try:
            adicionar_usuario(cnpj, senha)
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('dashboard'))  # Redireciona para a tela inicial
        except sqlite3.IntegrityError:
            flash('Esse CNPJ já está registrado.', 'error')
            return redirect(url_for('registrar'))

    return render_template('registro.htm')

@app.route('/login', methods=['POST'])
def login():
    cnpj = request.form['cnpj']
    senha = request.form['senha']

    # Verificação de login no banco de dados
    usuario = verificar_usuario(cnpj, senha)
    if usuario:
        session['user_id'] = usuario[0]  # Armazena o ID do usuário na sessão
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))  # Redireciona para a tela inicial
    else:
        flash('CNPJ ou senha incorretos.', 'error')
        return redirect(url_for('home'))

# Nova rota para a tela inicial/dashboard
@app.route('/dashboard')
def dashboard():
    # Consulta ao banco de dados para trazer os dados dos formulários preenchidos
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM formularios')
    formularios = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.htm', formularios=formularios)

# Nova rota para o formulário
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nome_empresa = request.form['nome_empresa']
        idade = request.form['idade']
        genero = request.form['genero']
        esporte = request.form['esporte']
        usuario_id = request.form['usuario_id']  # ID do usuário logado

        # Adicionar os dados do formulário ao banco de dados
        adicionar_formulario(nome_empresa, idade, genero, esporte, usuario_id)
        flash('Formulário enviado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('formulario.htm')

@app.route('/perfil')
def perfil():
    return render_template('perfil.htm')

if __name__ == '__main__':
    app.run(debug=True)
