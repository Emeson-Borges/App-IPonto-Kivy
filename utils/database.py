import sqlite3

DB_PATH = "banco_dados.db"

def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            matricula TEXT NOT NULL UNIQUE
        )
    ''')

    # Tabela de dados faciais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados_faciais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL UNIQUE,
            encoding TEXT NOT NULL
        )
    ''')

    # Tabela de registros de ponto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_ponto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            tipo TEXT NOT NULL,
            sincronizado TEXT NOT NULL
        )
    ''')

    # Tabela de credenciais (CPF e senha)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credenciais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de PINs para login
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL UNIQUE,
            pin TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Chamar esta função no início do programa
inicializar_banco()
