from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/artstyle')
def artstylenav():
    return render_template('artstylenav.html')


@app.route('/mediums')
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


@app.route('/triangles/<int:size>')
def triangles(size):
    return render_template("triangles.py")


if __name__ == '__main__':
    app.run(debug=True)
