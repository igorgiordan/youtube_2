import psycopg2
import psycopg2.extras

from flask import g, session, request, redirect, url_for, render_template

from youtube import app

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Connect database
# g = http://flask.pocoo.org/docs/1.0/api/#flask.g
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.before_request
def before_request():
   g.db = psycopg2.connect(host='localhost', database='youtube', user='postgres', password='igor')

# Disconnect database
@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM genero;")
    data = cur.fetchall()
    cur.close()
    '''
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if(request.method == 'GET'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM video")
        videos = cur.fetchall()
        cur.execute("SELECT * FROM curtir")
        curtidas = cur.fetchall()
        cur.execute("SELECT * FROM comentar")
        comentarios = cur.fetchall()
        status = 0
        cur.close()
        for x in videos:
            a = x[2].split('=')
            videos[status][2] = a[1]
            status += 1
        return render_template('index.html', curtidas=curtidas, comentarios=comentarios, videos=videos)
    else:
        print(request.form["login"])
        return render_template('index.html')

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if(request.method == 'GET'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM video WHERE username != '{0}'".format(session['name']))
        videos = cur.fetchall()
        cur.execute("SELECT * FROM curtir")
        curtidas = cur.fetchall()
        cur.execute("SELECT * FROM comentar")
        comentarios = cur.fetchall()
        cur.close()
        status = 0
        for x in videos:
            a = x[2].split('=')
            videos[status][2] = a[1]
            status += 1
        return render_template('todos.html', videos=videos, user = session['name'], curtidas = curtidas, comentarios = comentarios)
    else:
        return render_template('usuario.html')

@app.route('/excluir', methods=['GET', 'POST'])       
def excluir():
    if(request.method == 'POST'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username = session['name']
        nome = request.form['nome']
        cur.execute("SELECT * FROM video WHERE username = '{}'".format(username))
        a = cur.fetchall()
        status = None
        for i in a:
            if i[0] == nome:
                status = True
                break
        print(status)
        if (status == True):
            cur.execute("DELETE FROM video WHERE nome = '{}'".format(nome))
            g.db.commit()
            cur.close()
            return redirect(url_for("usuario"))
    return render_template('excluir_video.html')

@app.route('/comentar/<int:id_video>', methods=['GET', 'POST'])       
def comentar(id_video):
    if (request.method == 'POST'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username = session['name']
        id_video = id_video
        texto = request.form['coment']
        cur.execute("INSERT INTO comentar(username, id_video, texto) VALUES ('{}', {}, '{}')".format(username, id_video, texto))
        g.db.commit()
        cur.close()
        return redirect(url_for("todos"))
    return redirect(url_for("todos"))
@app.route('/curtir/<int:id_video>', methods=['GET', 'POST'])       
def curtir(id_video):
    if (request.method == 'POST'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username = session['name']
        id_video = id_video
        cur.execute("SELECT * FROM curtir WHERE username = '{}'".format(username))
        curtidas = cur.fetchall()
        print(curtidas)
        for i in curtidas:
            if i[0] == id_video:
                return redirect(url_for("todos"))
        cur.execute("INSERT INTO curtir(id_video, username) VALUES ({}, '{}')".format(id_video, username))
        g.db.commit()
        cur.close()
        return redirect(url_for("todos"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username = request.form['username']
        senha = request.form['senha']
        print("SELECT * FROM usuario WHERE username = '{0}' AND senha = '{1}'".format(username, senha))
        cur.execute("SELECT * FROM usuario WHERE username = '{0}' AND senha = '{1}'".format(username, senha))
        usuario = cur.fetchall()
        cur.close()
        if len(usuario) > 0:
            session['name'] = request.form['username']
            return redirect(url_for("usuario"))
        return render_template("login.html", erro="Usuário não cadastrado!")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM genero;")
    data = cur.fetchall()
    cur.close()
    '''
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    return render_template("login.html")

@app.route('/cadastro_video', methods=['GET', 'POST'])
def cadastro_video():
    if (request.method == 'POST'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        nome = request.form['nome']
        link = request.form['link']
        cur.execute('INSERT INTO video(nome, link, username) VALUES (%s, %s, %s)', (nome, link, session['name']))
        g.db.commit()
        cur.close()
        return redirect(url_for("usuario"))
    return render_template('cadastro_video.html')

@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM video WHERE username = '{0}'".format(session['name']))
    videos = cur.fetchall()
    status = 0
    for x in videos:
        a = x[2].split('=')
        videos[status][2] = a[1]
        status += 1
    return render_template("usuario.html", user = session['name'], videos=videos)

@app.route('/sair', methods=['GET', 'POST'])
def sair():
    if (request.method == 'POST'):
        session.pop('name')
        return redirect(url_for("index"))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if (request.method == 'POST'):
        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('cadastro')
        username = request.form['username']
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']
        cur.execute("SELECT * FROM usuario WHERE username = '{0}'".format(username))
        usuario = cur.fetchall()
        if len(usuario) > 0:
            return redirect(url_for("cadastro"))
        cur.execute('INSERT INTO usuario(username, nome, senha, email) VALUES (%s, %s, %s, %s)', (username, nome, senha, email))
        g.db.commit()
        cur.close()
        return redirect(url_for("login"))
    return render_template("cadastro.html")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM genero;")
    data = cur.fetchall()
    cur.close()
    '''
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~