from bottle import route, run, static_file, template, TEMPLATE_PATH, redirect
from bottle import request, response
import os
import sys
import bottle
import sqlite3

# Add project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)

# Import the UserModel class from user_model.py
from app.models.user_model import UserModel

# Instantiate the UserModel
user_model = UserModel()

# Set the correct template path relative to your project directory
bottle.TEMPLATE_PATH = [
    os.path.join(os.path.dirname(__file__), '../views/html'),
    './',
    './views/'
]

# Database connection
def get_db():
    return sqlite3.connect('your_database.db')

# Serve static files (like images, CSS, JS)
@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(os.path.dirname(__file__), '../static'))

# Route for the root URL
@route('/')
def root():
    redirect('/home2.html')

# Route for home
@route('/home2.html')
def dashboard():
    return template('home2.html')

@route('/home')
def home():
    return template('home')

@route('/store.html')
def store():
    return template('store.html')

# Route for user registration
@route('/cadastrar.html', method=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        if user_model.add_user(username, password):  # Use user_model.add_user
            return redirect('/home')
        else:
            return "Username already exists."
    return template('cadastrar.html')

@route('/portal.html', method=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        if user_model.check_credentials(username, password):
            # Retrieve the user_id from the database
            user_id = user_model.get_user_id(username)
            if user_id:
                response.set_cookie('session_id', 'some_session_id')  # Set session cookie
                response.set_cookie('username', username)  # Set username cookie
                response.set_cookie('user_id', str(user_id))  # Set user_id cookie
                # Set user_id in localStorage via JavaScript
                return f'''
                    <script>
                        localStorage.setItem('user_id', '{user_id}');
                        localStorage.setItem('username', '{username}');
                        window.location.href = '/home';
                    </script>
                '''
            else:
                return "User not found."
        else:
            return "Invalid username or password."
    return template('portal.html')
@route('/inicio')
def inicio():
    return template('inicio')

@route('/portal')
def portal():
    return template('portal')

# Route to save cart items
@route('/save_cart', method='POST')
def save_cart():
    user_id = request.json.get('user_id')
    cart = request.json.get('cart')
    
    if not user_id or not cart:
        return {'status': 'error', 'message': 'Invalid request data'}

    db = get_db()
    cursor = db.cursor()
    
    try:
        # Clear existing cart items for the user
        cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
        
        # Insert new cart items
        for item in cart:
            cursor.execute("""
                INSERT INTO cart_items (user_id, title, price, image_src, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, item['title'], item['price'], item['imageSrc'], item['quantity']))
        
        db.commit()
        return {'status': 'success'}
    except Exception as e:
        print("Error saving cart:", e)  # Debugging
        return {'status': 'error', 'message': str(e)}
    finally:
        db.close()
# Route to load cart items
@route('/load_cart', method='GET')
def load_cart():
    user_id = request.query.get('user_id')  # Get user_id from the query parameters
    
    db = get_db()
    cursor = db.cursor()
    
    # Fetch cart items for the user
    cursor.execute("""
        SELECT title, price, image_src, quantity
        FROM cart_items
        WHERE user_id = ?
    """, (user_id,))
    
    cart_items = cursor.fetchall()
    db.close()
    
    # Format the cart items for the response
    cart = [{
        'title': item[0],
        'price': item[1],
        'imageSrc': item[2],
        'quantity': item[3]
    } for item in cart_items]
    
    return {'cart': cart}

# Run the application
run(host='127.0.0.1', port=8080, debug=True, reloader=True)