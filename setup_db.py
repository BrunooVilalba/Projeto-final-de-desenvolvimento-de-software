import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_database():
    # Conectar ao postgres default
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Criar banco
    try:
        cur.execute('CREATE DATABASE projetodb')
        print("Banco de dados 'projetodb' criado com sucesso!")
    except psycopg2.Error as e:
        print(f"Nota: {e}")
    
    # Criar usuário e dar permissões
    try:
        cur.execute("CREATE USER projuser WITH PASSWORD 'projsenha'")
        print("Usuário 'projuser' criado com sucesso!")
    except psycopg2.Error as e:
        print(f"Nota: {e}")
    
    try:
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE projetodb TO projuser')
        print("Permissões concedidas ao usuário 'projuser'!")
    except psycopg2.Error as e:
        print(f"Nota: {e}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    setup_database()