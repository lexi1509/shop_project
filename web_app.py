from flask import Flask, render_template_string, request, redirect
import mysql.connector

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="vscode",
        password="Alex2014",
        database="shop"
    )

# Главная страница — список товаров
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Мой магазин</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .button { background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
            .button:hover { background: #45a049; }
            .delete { color: red; text-decoration: none; margin-left: 10px; }
        </style>
    </head>
    <body>
        <h1>🛍️ Товары в магазине</h1>
        <a href="/add" class="button">➕ Добавить товар</a>
        <table>
            <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Цена</th>
                <th>Количество</th>
                <th>Действия</th>
            </tr>
            {% for product in products %}
            <tr>
                <td>{{ product.id }}</td>
                <td>{{ product.name }}</td>
                <td>{{ product.price }} руб.</td>
                <td>{{ product.quantity }}</td>
                <td>
                    <a href="/delete/{{ product.id }}" class="delete" onclick="return confirm('Удалить товар?')">🗑️ Удалить</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, products=products)

# Страница добавления товара
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
            (name, price, quantity)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Добавить товар</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            form { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 400px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            button { background: #4CAF50; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
            button:hover { background: #45a049; }
            .back { display: block; margin-top: 20px; color: #666; }
        </style>
    </head>
    <body>
        <h1>➕ Добавить товар</h1>
        <form method="post">
            <label>Название товара:</label>
            <input type="text" name="name" required>
            <label>Цена:</label>
            <input type="number" step="0.01" name="price" required>
            <label>Количество:</label>
            <input type="number" name="quantity" required>
            <button type="submit">Сохранить</button>
        </form>
        <a href="/" class="back">← Вернуться к списку</a>
    </body>
    </html>
    '''
    return render_template_string(html)

# Удаление товара
@app.route('/delete/<int:product_id>')
def delete(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)