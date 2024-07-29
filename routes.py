from flask import Flask, render_template, request
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
    cur.execute('SELECT * WHERE Mediums WHERE id = ?', (id,))
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


# For a working Search Function

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    results = query_database(search_term)
    return render_template('search.html', results=results)


def query_database(search_term):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT 'ArtStyle' AS type, id, name, description
        FROM ArtStyles  WHERE name LIKE ?
        UNION
        SELECT 'Medium' AS type, id, name, description
        FROM Mediums WHERE name LIKE ?
        UNION
        SELECT 'Artist' AS type, id, name, description
        FROM Artists
        WHERE name LIKE ?
        ''', ('%' + search_term + '%',
              '%' + search_term + '%',
              '%' + search_term + '%'))
    results = cursor.fetchall()
    conn.close()
    return results


# Test

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
