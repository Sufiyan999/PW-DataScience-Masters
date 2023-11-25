from flask import Flask, render_template
from bokeh.embed import server_document

app = Flask(__name__)

@app.route('/')
def index():
    script = server_document('http://localhost:5006/your_bokeh_app')
    return render_template('index.html', script=script)

if __name__ == '__main__':
    app.run(debug=True)