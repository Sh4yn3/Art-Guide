from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'ARTGUIDE.db'


# DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


def query_database(search_term):
    conn = get_db()
    cursor = conn.cursor()

    # Query for ArtStyles
    cursor.execute("""
        SELECT *
        FROM ArtStyles
        WHERE name LIKE ?
    """, ('%' + search_term + '%',))
    artstyles = cursor.fetchall()

    # Query for Mediums
    cursor.execute("""
        SELECT *
        FROM Mediums
        WHERE name LIKE ?
    """, ('%' + search_term + '%',))
    mediums = cursor.fetchall()

    # Query for Artists
    cursor.execute("""
        SELECT *
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


# WEBPAGES

@app.route('/')
def home():
    latest_mediums = get_latest_mediums(limit=4)
    latest_artstyles = get_latest_artstyles(limit=4)
    latest_artists = get_latest_artists(limit=4)
    return render_template('home.html', latest_mediums=latest_mediums,
                           latest_artstyles=latest_artstyles,
                           latest_artists=latest_artists)


@app.route('/artstyle')
def artstylenav():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ArtStyles")
    artstyles = cur.fetchall()
    conn.close()
    return render_template('artstylenav.html', artstyles=artstyles)


@app.route('/medium')
def mediumsnav():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mediums")
    mediums = cur.fetchall()
    conn.close()
    return render_template('mediumsnav.html', mediums=mediums)


@app.route('/artist')
def artistnav():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Artists")
    artists = cur.fetchall()
    conn.close()
    return render_template('artistnav.html', artists=artists)


@app.route('/artstyle/<int:id>')
def artstyle(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ArtStyles WHERE id = ?", (id,))
    artstyle = cur.fetchone()
    if not artstyle:
        return render_template('error.html', message="ArtStyle not found"), 404
    cur.execute("SELECT * FROM Artworks WHERE artstyle_id = ?", (id,))
    artworks = cur.fetchall()
    conn.close()
    return render_template('artstyle.html', artstyle=artstyle,
                           artworks=artworks)


@app.route('/medium/<int:id>')
def medium(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mediums WHERE id = ?", (id,))
    medium = cur.fetchone()
    if not medium:
        return render_template('error.html', message="Medium not found"), 404
    cur.execute("SELECT * FROM Artworks WHERE medium_id = ?", (id,))
    artworks = cur.fetchall()
    conn.close()
    return render_template('medium.html', medium=medium,
                           artworks=artworks, )


@app.route('/artist/<int:id>')
def artist(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Artists WHERE id = ?", (id,))
    artist = cur.fetchone()
    if not artist:
        return render_template('error.html', message="Artist not found"), 404
    cur.execute("SELECT * FROM Artworks WHERE artist_id = ?", (id,))
    artworks = cur.fetchall()
    conn.close()
    return render_template('artist.html', artist=artist,
                           artworks=artworks)


# FUNCTIONS

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    results = query_database(search_term)
    return render_template('search.html', results=results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


def get_latest_artists(limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM Artists
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    latest_artists = cur.fetchall()
    conn.close()
    return latest_artists


def get_latest_artstyles(limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM ArtStyles
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    latest_artstyles = cur.fetchall()
    conn.close()
    return latest_artstyles


def get_latest_mediums(limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM Mediums
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    latest_mediums = cur.fetchall()
    conn.close()
    return latest_mediums


if __name__ == '__main__':
    app.run(debug=True)
