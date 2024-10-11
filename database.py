import sqlite3

def criar_tabela():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS formularios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_empresa TEXT NOT NULL,
            idade INTEGER NOT NULL,
            genero TEXT NOT NULL,
            esporte TEXT NOT NULL,
            usuario_id INTEGER,
            imagem TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    


def adicionar_usuario(cnpj, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (cnpj, senha) VALUES (?, ?)', (cnpj, senha))
    conn.commit()
    conn.close()

def verificar_usuario(cnpj, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE cnpj = ? AND senha = ?', (cnpj, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def adicionar_formulario(nome_empresa, idade, genero, esporte, usuario_id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO formularios (nome_empresa, idade, genero, esporte, usuario_id) VALUES (?, ?, ?, ?, ?)', 
                   (nome_empresa, idade, genero, esporte, usuario_id))
    conn.commit()
    conn.close()
