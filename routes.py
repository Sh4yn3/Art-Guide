from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'ARTGUIDE.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


def query_database(search_term):
    conn = get_db()
    cursor = conn.cursor()

    # Query for ArtStyles

    cursor.execute("""
        SELECT id, name, description, photo
        FROM ArtStyles
        WHERE name LIKE ?
    """, ('%' + search_term + '%',))
    artstyles = cursor.fetchall()

    # Query for Mediums
    cursor.execute("""
        SELECT id, name, description, photo
        FROM Mediums
        WHERE name LIKE ?
    """, ('%' + search_term + '%',))
    mediums = cursor.fetchall()

    # Query for Artists
    cursor.execute("""
        SELECT id, name, description, photo
        FROM Artists
        WHERE name LIKE ?
    """, ('%' + search_term + '%',))
    artists = cursor.fetchall()

    conn.close()
    return {
        'artstyles': artstyles,
        'mediums': mediums,
        'artists': artists
    }


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/artstyle')
def artstylenav():
    return render_template('artstylenav.html')


@app.route('/medium')
def mediumsnav():
    return render_template('mediumsnav.html')


@app.route('/artist')
def artistnav():
    return render_template('artistnav.html')


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
    cur.execute("SELECT * FROM Mediums WHERE id = ?", (id,))
    medium = cur.fetchone()
    conn.close()
    return render_template('medium.html', medium=medium)


@app.route('/artist/<int:id>')
def artist(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Artists WHERE id = ?", (id,))
    artist = cur.fetchone()
    conn.close()
    return render_template('artist.html', artist=artist)


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    results = query_database(search_term)
    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
