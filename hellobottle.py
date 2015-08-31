import bottle
from bottle import jinja2_template, static_file


app = bottle.Bottle()


from bottle import static_file
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@app.route('/hello')
def hello():
    # return jinja2_template('template/login.html')
    return jinja2_template('template/base.html')


app.run(host='localhost', port=81, debug=True)
