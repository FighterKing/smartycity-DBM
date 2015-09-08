import uuid
import bottle
import bottle_mysql

app = bottle.Bottle()
app.config.load_config('app.conf')
# dbhost: optional, default is localhost
# keyword: The keyword argument name that triggers the plugin (default: ‘db’).
plugin = bottle_mysql.Plugin(dbuser=app.config['mysql.user'], dbpass=app.config['mysql.pwd'], dbname=
         app.config['mysql.dbname'], dbhost=app.config['mysql.host'], dictrows=['mysql.dictrows'] == 'True')
app.install(plugin)


# Description : document template.
#
# Input : None
#
# Output : test page
@app.route('/test')
def hello():
    # return bottle.jinja2_template('template/login.html')
    return bottle.jinja2_template('template/index.html')


# Description : get static files.
#
# Input : filepath
#
# Output : static file
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')


# Description : login page.
#
# Input : None
#
# Output : login page
@app.get('/')
@app.get('/admin/login')
def admin_login():
    s_id = uuid.uuid1()
    return bottle.jinja2_template('template/login.html', app_path='/admin/login', session_id=s_id)


# Description : login process.
#
# Input : None
#
# Output : login result page
@app.post('/admin/login', mysql={'dbname': 'community_dbm'})
def admin_login_process(db):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
	s_id = bottle.request.forms.get('s_id')
    db.execute('select password, user_type_id from user where username = "' + username + '"')
    row = db.fetchone()
    if row:
        if str(row[0]) == password and str(row[1]) == '4':
            return admin_index(is_authenticated=True, request_session_original_user=True, current_username=username,
                               user_has_usable_password=True, site_url='www.baidu.com')
        else:
            return "<p>Your username or password is wrong, or you are not an administrator.</p>"
    else:
        return "<p>Login failed.</p>"


# Description : index page.
#
# Input : None
#
# Output : index page
@app.get('/admin/index')
def admin_index(**dict):
    return bottle.jinja2_template('template/index.html', dict)

@app.get('/admin/register')
def admin_register():
    return bottle.jinja2_template('template/register.html')

@app.post('/admin/register')
def admin_register_process(db):
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    status = db.execute('insert into user (username, password, user_type_id) values("'+ username + '","' + password + '", 4)')
    return bottle.jinja2_template('template/login.html', app_path='/admin/login')

app.run(host='localhost', port=1025, debug=True, reloader=True)
>>>>>>> 68338a0deb5fdf8c208f449a8a56e29ddd76baa5
