import sys
import os

# Add the project root directory to the Python path
project_root = "/home/maria-laura/Downloads/trabalhofinalOOy/trabalho_final-main"
sys.path.append(project_root)

# Print sys.path to verify
print("Updated sys.path:", sys.path)

from bottle import template, redirect, request
from app.controllers.db.db_stories import DataStory
from models.user_model import init_db, check_credentials, add_user
from models.user_model import authenticate_user

class Application():

    def __init__(self):
        self.pages = {
            'pagina': self.pagina,
            'home': self.home,
            'store': self.store,
            'inicio': self.inicio,
            'cadastrar': self.cadastrar,
            'historias': self.historias,
            'entrar': self.entrar,
            'home2': self.home2
        }
        
        self.story_model = DataStory()  # Instância da classe DataStory para gerenciar as histórias
        init_db()
        
    def __call__(self, environ, start_response):
        # This method makes the class callable and compatible with Bottle's run function
        from bottle import request, response
        request.bind(environ)
        response.bind()

        # Get the path from the request
        path = request.path.lstrip('/')

        if path in self.pages:
            return self.pages[path]()
        else:
            return self.helper()
        
        

    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')

    def helper(self):
        return template('app/views/html/helper')
    def pagina(self, parameter=None):
        if not parameter:
            return template('app/views/html/pagina', transfered=False)
        else:
            # Chama o método get_user_account para buscar o usuário pelo nome
            info = self.user_model.get_user_account(parameter)
            if not info:
                redirect('/pagina')  # Redireciona caso a conta não seja encontrada
            else:
                return template('app/views/html/pagina', transfered=True, data=info)

    def is_authenticated(self, username):
        session_id = self.get_session_id()
        if not session_id:
            return False
        current_username = self.user_model.getUserName(session_id)
        return username == current_username

    def authenticate_user(self, username, password):
        session_id = self.user_model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self._current_username = username  # Define diretamente o nome do usuário
            return session_id, username
        return None

    def logout_user(self):
        session_id = self.get_session_id()
        if session_id:
            self.user_model.logout(session_id)  # Remove o usuário logado
            self._current_username = None  # Limpa o nome de usuário atual

    def home(self):
        return template('app/views/html/home')
    def store(self):
        return template('app/views/html/store')
    def home2(self):
        return template('app/views/html/home2')

    def inicio(self):
        return template('app/views/html/inicio')

    def historias(self):
        return template('app/views/html/historias')

    def entrar(self):
        return template('app/views/html/portal')

    def cadastrar(self):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            if add_user(username, password):
                return redirect('/home')
            else:
                return "Username already exists."
        return template('app/views/html/cadastrar')

    def signin(self):
        from bottle import request, response
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            if check_credentials(username, password):
                session_id, username = self.authenticate_user(username, password)
                response.set_cookie('session_id', session_id)
                return redirect('/home')
            else:
                return "Invalid username or password."
        return template('app/views/html/portal')

from bottle import default_app, run

app = default_app()

if __name__ == "__main__":
    run(app=app, server='wsgiref', host='127.0.0.1', port=8080)