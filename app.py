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
    add_user(db)
    return bottle.jinja2_template('template/login.html')


@app.get('/admin/user')
@app.get('/admin/user/list')
def admin_user_list(db):
    sql = 'select image, username, password, user_type_id,name, email, identity_number, card_id from user'
    db.execute(sql)
    it = iter(db)
    users = []
    user_type_map = {1: 'managemment',2:'service', 3:'resident',4:'admin'}
    for i, row in enumerate(it):
        print(i, row)
        users.append(models.User(i, row[1], row[2], user_type_map[row[3]], '/files/' + (row[0] if row[0] else '') , row[4], row[5],
                                row[6], row[7]))
    return bottle.jinja2_template('template/user_list.html', users=users)


@app.get('/admin/user/<userid:int>')
def admin_user_detail(userid):
    return bottle.jinja2_template('template/user_detail.html', user=models.User(1, 'eugene', 'pass', 'admin'))


@app.get('/admin/apartment')
@app.get('/admin/apartment/list')
def admin_apartment_list():
    return bottle.jinja2_template('template/apartment_list.html',
                                  apartments=[models.Apartment(101, '1号', 'Building 101 description', 101, '201', 60, 'Eugene', '310110196004020311'),
                                              models.Apartment(102, '2号', 'Building 102 description', 102, '202', 80, 'Ernest', '310110196004020312'),
                                              models.Apartment(103, '3号', 'Building 103 description', 103, '203', 90, 'Young', '310110196004020313')])


@app.get('/admin/personnel')
@app.get('/admin/personnel/list')
def admin_personnel_list():
    return bottle.jinja2_template('template/personnel_list.html',
                                  personnels=[models.Personnel(1, 'Eugene', '块长', '块长职责', '居委会', '第一块区（1-11、21、22）', '国和路888弄32号101室'),
                                              models.Personnel(2, 'Ernest', '楼组长', '楼组长职责', '居委会', '第二块区（1-11、21、22）', '国和路888弄32号102室'),
                                              models.Personnel(3, 'Young', '党总支书记', '党总支书记职责', '居委会', '第三块区（1-11、21、22）', '国和路888弄32号103室')])


def check():
    s = bottle.request.environ.get('beaker.session')
    return s['username'] if s.get('username') else None


def add_user(db):
    if not check():
        bottle.redirect('/')

    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    email = bottle.request.forms.get('email')
    name =  bottle.request.forms.get('name')
    id = bottle.request.forms.get('identity_number')
    card_id = bottle.request.forms.get('card_number')

    convert = lambda x: "'{}'".format(x) if x else 'NULL'

    username, password, email, name, id, card_id = [convert(x) for x in [username, password, email, name, id, card_id]]
    select_user_type = bottle.request.forms.get('selectUserType')
    upload = bottle.request.files.get('upload')
    upload.save('files')
    filename = convert(upload.filename)
    sql = 'insert into user (username, password, user_type_id, email, identity_number, card_id, image) values(' + username +\
          ', ' + password + ',' + select_user_type + "," + email + "," +  id + ',' + card_id + ',' + filename + ')'
    print(sql)
    status = db.execute(sql)


bottle.run(host='localhost', port=1025, debug=True, reloader=True, app=app_middlware)
