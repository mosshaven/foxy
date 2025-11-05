import sqlite3
import os

db_path = "data/fox.db"

if not os.path.exists(db_path):
    print("Database not found! Creating new database...")
    os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    foxy_bucks INTEGER DEFAULT 0,
    pizzas INTEGER DEFAULT 0,
    cubes INTEGER DEFAULT 0,
    angry_kids INTEGER DEFAULT 0,
    is_banned INTEGER DEFAULT 0,
    last_pizza DATETIME,
    last_case DATETIME,
    last_command DATETIME,
    last_pizzeria DATETIME
)
""")
conn.commit()
print("✓ Users table checked/created")

# Get existing columns
cursor.execute("PRAGMA table_info(users)")
existing_columns = {column[1]: column[2] for column in cursor.fetchall()}

# Define all required columns with their types
required_columns = {
    'id': 'INTEGER PRIMARY KEY',
    'username': 'TEXT',
    'first_name': 'TEXT',
    'last_name': 'TEXT',
    'foxy_bucks': 'INTEGER DEFAULT 0',
    'pizzas': 'INTEGER DEFAULT 0',
    'cubes': 'INTEGER DEFAULT 0',
    'angry_kids': 'INTEGER DEFAULT 0',
    'is_banned': 'INTEGER DEFAULT 0',
    'last_pizza': 'DATETIME',
    'last_case': 'DATETIME',
    'last_command': 'DATETIME',
    'last_pizzeria': 'DATETIME'
}

# Add missing columns
migrations_done = 0
for column_name, column_type in required_columns.items():
    if column_name not in existing_columns and column_name != 'id':
        print(f"Adding column: {column_name} ({column_type})")
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
            conn.commit()
            migrations_done += 1
            print(f"✓ Added {column_name}")
        except sqlite3.OperationalError as e:
            print(f"✗ Failed to add {column_name}: {e}")

if migrations_done > 0:
    print(f"\n✓ Migration completed! Added {migrations_done} column(s)")
else:
    print("\n✓ Database is up to date, no migrations needed")

conn.close()
