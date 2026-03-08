import mysql.connector
from mysql.connector import Error

# Подключение к базе данных
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="vscode",
            password="Alex2014",
            database="shop"
        )
        if connection.is_connected():
            print("✅ Подключение к базе данных успешно!")
            return connection
    except Error as e:
        print(f"❌ Ошибка подключения: {e}")
        return None

# Показать все товары
def show_products(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    
    print("\n📦 Список товаров:")
    print("-" * 50)
    for product in products:
        print(f"ID: {product[0]}, Название: {product[1]}, Цена: {product[2]} руб., Количество: {product[3]}")
    print("-" * 50)
    cursor.close()

# Добавить новый товар
def add_product(connection, name, price, quantity):
    cursor = connection.cursor()
    sql = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
    values = (name, price, quantity)
    cursor.execute(sql, values)
    connection.commit()
    print(f"✅ Товар '{name}' добавлен с ID {cursor.lastrowid}")
    cursor.close()

# Обновить количество товара
def update_quantity(connection, product_id, new_quantity):
    cursor = connection.cursor()
    sql = "UPDATE products SET quantity = %s WHERE id = %s"
    cursor.execute(sql, (new_quantity, product_id))
    connection.commit()
    if cursor.rowcount > 0:
        print(f"✅ Количество товара ID {product_id} обновлено до {new_quantity}")
    else:
        print(f"❌ Товар с ID {product_id} не найден")
    cursor.close()

# Удалить товар
def delete_product(connection, product_id):
    cursor = connection.cursor()
    sql = "DELETE FROM products WHERE id = %s"
    cursor.execute(sql, (product_id,))
    connection.commit()
    if cursor.rowcount > 0:
        print(f"✅ Товар ID {product_id} удалён")
    else:
        print(f"❌ Товар с ID {product_id} не найден")
    cursor.close()

# Главное меню
def main():
    conn = create_connection()
    if not conn:
        return
    
    while True:
        print("\n" + "="*50)
        print("🏪 МАГАЗИН - УПРАВЛЕНИЕ ТОВАРАМИ")
        print("="*50)
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Обновить количество товара")
        print("4. Удалить товар")
        print("5. Выйти")
        print("-"*50)
        
        choice = input("Выберите действие (1-5): ")
        
        if choice == "1":
            show_products(conn)
        elif choice == "2":
            name = input("Название товара: ")
            price = float(input("Цена: "))
            quantity = int(input("Количество: "))
            add_product(conn, name, price, quantity)
        elif choice == "3":
            product_id = int(input("ID товара: "))
            new_quantity = int(input("Новое количество: "))
            update_quantity(conn, product_id, new_quantity)
        elif choice == "4":
            product_id = int(input("ID товара для удаления: "))
            delete_product(conn, product_id)
        elif choice == "5":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный ввод, попробуйте снова.")
    
    conn.close()

if __name__ == "__main__":
    main()