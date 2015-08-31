import bottle

app = bottle.Bottle()

@app.route('/hello')
def hello():
  return app.jinja2_template('template/admin/login.html')

app.run(host='localhost', port=8000, debug=True)
