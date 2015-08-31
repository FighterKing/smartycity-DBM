import bottle
from bottle import jinja2_template, static_file

app = bottle.Bottle()


@app.route('/hello')
def hello():
    # return jinja2_template('template/login.html')
    return jinja2_template('template/base.html')


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/static/' + filepath)


app.run(host='localhost', port=81, debug=True)
