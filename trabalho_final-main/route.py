from app.controllers.application import Application
from bottle import Bottle, run, request, static_file
from bottle import redirect, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

#copiando o que foi passado
@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<username>', methods=['GET'])
def action_pagina(username=None):
    if not username:
        return ctl.render('pagina')
    else:
        return ctl.render('pagina',username=username)
    
@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username= ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, \
        secure=True, max_age=3600)
        redirect(f'/pagina/{username}')
    else:
        return redirect('/portal')


#-----------------------------------------------------------------------------
#criando o projeto
#ROTAS PARA AUTENTICAÇÃO 
@app.route('/portal', method=['GET'])
def login_page():
    return ctl.render('portal')

@app.route('/portal', method=['POST'])
def action_entrar():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username=ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True) 
        return redirect(f'/pagina/{username}')
    else:
        return redirect('/home')
    
@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/home')

@app.route('/cadastrar', method=['GET'])
def action_home():
    return ctl.render('cadastrar')

#-----------------------------------------------------------------------------
#ROTAS PRINCIPAIS
@app.route('/home', method=['GET'])
def action_home():
    return ctl.render('home')

@app.route('/inicio', method=['GET'])
def action_inicio():
    return ctl.render('inicio')

@app.route('/historias', method=['GET'])
def action_historias():
    return ctl.render('historias')

#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
