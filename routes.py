from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


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
def artstyles(id):
    conn = sqlite3.connect('ARTGUIDE.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ArtStyles WHERE id=?;", (id,))
    artstyles = cur.fetchone()
    conn.close()
    return render_template("artstyle.html", artstyles=artstyles)


@app.route('/medium/<int:id>')
def medium(id):
    conn = sqlite3.connect('ARTGUIDE.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mediums WHERE id=?", (id,))
    medium = cur.fetchone()
    conn.close()
    return render_template("medium.html", medium=medium)


def generate_triangle(size):
    triangle = []
    for i in range(1, size + 1):
        line = '*' * i
        triangle.append(line)
    return '\n'.join(triangle)


@app.route('/triangles/<int:size>')
def triangles(size):
    if size < 1:
        return "Size must be a positive integer.", 400
    triangle = generate_triangle(size)
    return f"<pre>{triangle}</pre>"


# For the search function

@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form.get('searchterm')
        return f'You asked to search for \"{search}\"'
    else:
        return "poop"


if __name__ == '__main__':
    app.run(debug=True)
