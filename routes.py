from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'ARTGUIDE.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/artstyle')
def artstylenav():
    return render_template('artstylenav.html')


@app.route('/medium')
def mediumsnav():
    return render_template('mediumsnav.html')


@app.route('/artstyle/<int:id>')
def artstyle(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ArtStyles WHERE id = ?", (id,))
    artstyle = cur.fetchone()
    conn.close()
    return render_template('artstyle.html', artstyle=artstyle)


@app.route('/medium/<int:id>')
def medium(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * WHERE id = ?', (id,))
    medium = cur.fetchone()
    conn.close()
    return render_template('medium.html', medium=medium)


if __name__ == '__main__':
    app.run(debug=True)

# For Searching


if __name__ == '__main__':
    app.run(debug=True)
