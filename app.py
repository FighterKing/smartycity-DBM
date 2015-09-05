import bottle
from bottle import jinja2_template, static_file


app = bottle.Bottle()


# Description : document template.
#
# Input : None
#
# Output : test page
@app.route('/test')
def hello():
    # return jinja2_template('template/login.html')
    return jinja2_template('template/index.html')


# Description : get static files.
#
# Input : filepath
#
# Output : static file
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


# Description : login page.
#
# Input : None
#
# Output : login page
@app.get('/')
@app.get('/admin/login')
def admin_login():
    return jinja2_template('template/login.html', app_path = '/admin/login')

# Description : login process.
#
# Input : None
#
# Output : login page
@app.post('/admin/login')
def admin_login_process():
    username = request.forms.get('username')
    password = requets.forms.get('password')
    if admin_login_check(username, password):
        return "<p>Login success.</p>"
    else:
        return "<p>Login failed.</p>"

# Description : login check for username and password.
#
# Input : None
#
# Output : boolean
def admin_login_check(username, password):
    return True


# Description : index page.
#
# Input : None
#
# Output : index page
@app.get('/admin/index')
def admin_index():
    return jinja2_template('template/index.html')



app.run(host='localhost', port=1025, debug=True, reloader=True)
