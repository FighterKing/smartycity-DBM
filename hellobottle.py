import bottle
from bottle import jinja2_template

app = bottle.Bottle()

@app.route('/hello')
def hello():
    # return jinja2_template('template/login.html')
    return jinja2_template('template/base.html')

app.run(host='localhost', port=81, debug=True)
