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
            requisicao TEXT NOT NULL,
            nome_empresa TEXT NOT NULL,
            idade TEXT NOT NULL,
            genero TEXT NOT NULL,
            esporte TEXT NOT NULL,
            usuario_id INTEGER,
            imagem_perfil TEXT,  -- Novo campo para imagem de perfil
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

def adicionar_formulario(requisicao, nome_empresa, idade, genero, esporte, usuario_id, imagem_perfil):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO formularios (requisicao, nome_empresa, idade, genero, esporte, usuario_id, imagem_perfil) 
        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
        (requisicao, nome_empresa, idade, genero, esporte, usuario_id, imagem_perfil))
    conn.commit()
    conn.close()
