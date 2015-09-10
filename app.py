import bottle
import bottle_mysql
import models
from beaker.middleware import SessionMiddleware

app = bottle.Bottle()
app.config.load_config('app.conf')
# dbhost: optional, default is localhost
# keyword: The keyword argument name that triggers the plugin (default: ‘db’).
plugin = bottle_mysql.Plugin(dbuser=app.config['mysql.user'], dbpass=app.config['mysql.pwd'],
                             dbname=app.config['mysql.dbname'], dbhost=app.config['mysql.host'],
                             dictrows=['mysql.dictrows'] == 'True')
app.install(plugin)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,  # 300s
    'session.data_dir': './data',
    'session.auto': True
}
app_middlware = SessionMiddleware(app, session_opts)

# Description : document template.
#
# Input : None
#
# Output : test page
@app.route('/test')
def test():
    return bottle.jinja2_template('template/base.html')


# Description : get static files.
#
# Input : filepath
#
# Output : static file
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')


@app.route('/file/<filepath:path>')
def server_file(filepath):
    return bottle.static_file(filepath, root='file')


# Description : login page.
#
# Input : None
#
# Output : login page
@app.get('/')
@app.get('/admin/login')
def admin_login():
    return bottle.jinja2_template('template/login.html')


# Description : login process.
#
# Input : None
#
# Output : login result page
@app.post('/admin/login', mysql={'dbname': 'community_dbm'})
def admin_login_process(db):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    db.execute('select password, user_type_id from user where username = "' + username + '"')
    row = db.fetchone()
    if row:
        if str(row[0]) == password and str(row[1]) == '4':
            s = bottle.request.environ.get('beaker.session')
            s['username'] = username
            return admin_index()
        else:
            return "<p>Your username or password is wrong, or you are not an administrator.</p>"
    else:
        return "<p>Login failed.</p>"


# Description : index page.
#
# Input : None
#
# Output : index page
@app.get('/admin')
@app.get('/admin/index')
def admin_index(**dict):
    return bottle.jinja2_template('template/index.html', dict)


@app.get('/admin/signup')
def admin_signup():
    if check():
        return bottle.jinja2_template('template/signup.html')
    else:
        bottle.redirect('/')


@app.post('/admin/signup')
def admin_signup_process(db):
    if not check():
        bottle.redirect('/')

    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    email = bottle.request.forms.get('email')
    name = bottle.request.forms.get('name')
    identity_number = bottle.request.forms.get('identity_number')
    card_id = bottle.request.forms.get('card_id')

    convert = lambda x: "'{}'".format(x) if x else 'NULL'
    username, password, email, name, identity_number, card_id = [convert(x) for x in [username, password, email, name, identity_number, card_id]]

    upload = bottle.request.files.get('upload')
    upload.save('files')
    filename = convert(upload.filename)

    sql = 'insert into user (username, password, user_type_id, email, identity_number, card_id, image) values(' + username + \
          ', ' + password + ', 4,' + email + "," + identity_number + ',' + card_id + ',' + filename + ')'
    print(sql)
    status = db.execute(sql)
    return bottle.jinja2_template('template/login.html')


@app.get('/admin/user/add')
def admin_user_add():
    return bottle.jinja2_template('template/user_add.html')


@app.post('/admin/user/add')
def admin_user_add_process(db):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    # status = db.execute('insert into user (username, password, user_type_id) values("' + username + '", "' + password +
    # '", 4)')
    # return bottle.jinja2_template('template/login.html', app_path='/admin/login')


@app.get('/admin/user')
@app.get('/admin/user/list')
def admin_user_list():
    return bottle.jinja2_template('template/user_list.html', users=[models.User(1, 'eugene', 'pass', 'admin'),
                                                                    models.User(2, 'ernest', 'pass', 'management'),
                                                                    models.User(3, 'kaiyang', 'pass', 'service')])


def check():
    s = bottle.request.environ.get('beaker.session')
    return s['username'] if s.get('username') else None


bottle.run(host='localhost', port=1025, debug=True, reloader=True, app=app_middlware)
