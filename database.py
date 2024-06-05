import sqlite3

def setup_database():
    conn = sqlite3.connect('data/hangman.db')
    c = conn.cursor()

    # Criação das tabelas
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )''')

    # Inserção de categorias
    categories = ['animals', 'objects', 'cities']
    for category in categories:
        c.execute('INSERT INTO categories (name) VALUES (?)', (category,))
    
    conn.commit()

    # Inserção de palavras a partir de arquivos
    for category in categories:
        c.execute('SELECT id FROM categories WHERE name=?', (category,))
        category_id = c.fetchone()[0]
        
        with open(f'data/{category}.txt', 'r') as file:
            words = file.read().splitlines()
            for word in words:
                word = word.lower()  # Garantir que todas as palavras estejam em minúsculas
                c.execute('INSERT INTO words (word, category_id) VALUES (?, ?)', (word, category_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
