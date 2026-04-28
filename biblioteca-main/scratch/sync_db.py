import sqlite3
import os

db_path = 'instance/flaskdb.sqlite'

def sync():
    if not os.path.exists(db_path):
        print(f"Error: {db_path} no encontrado.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    commands = [
        # Auditoría
        """
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            usuario_nombre VARCHAR(100),
            accion VARCHAR(50) NOT NULL,
            tabla VARCHAR(100) NOT NULL,
            registro_id INTEGER,
            valores_anteriores TEXT,
            valores_nuevos TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(idUser)
        )
        """,
        # Usuarios
        "ALTER TABLE users ADD COLUMN fecha_registro DATETIME",
        
        # Autores
        "ALTER TABLE authors ADD COLUMN fecha_creacion DATETIME",
        
        # Publicaciones (Posts)
        "ALTER TABLE publicaciones ADD COLUMN fecha_creacion DATETIME",
        "ALTER TABLE publicaciones ADD COLUMN idAuthor INTEGER REFERENCES authors(idAuthor)",
        
        # Salas (Rooms)
        "ALTER TABLE rooms ADD COLUMN fecha_creacion DATETIME",
        "ALTER TABLE rooms ADD COLUMN status VARCHAR(50) DEFAULT 'Disponible'",
        
        # Etiquetas (Tags)
        "ALTER TABLE etiquetas ADD COLUMN fecha_creacion DATETIME"
    ]

    for cmd in commands:
        try:
            print(f"Ejecutando: {cmd[:50]}...")
            cursor.execute(cmd)
            conn.commit()
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print(f"  Info: La columna/tabla ya existe. Saltando...")
            else:
                print(f"  Error: {e}")
    
    conn.close()
    print("Sincronización finalizada.")

if __name__ == "__main__":
    sync()
