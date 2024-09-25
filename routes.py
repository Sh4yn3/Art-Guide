from flask import Flask, request, render_template
import sqlite3


app = Flask(__name__)
DATABASE = 'ARTGUIDE.db'


# Efficient Database Query Function
def db_query(query, multiple=True):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        if multiple:
            return cursor.fetchall()
        return cursor.fetchone()


# Query Database (search specific)
def query_database(search_term):
    search_term = f"'%{search_term}%'"
    return {
        'artstyles': db_query(f'''
                              SELECT * FROM ArtStyles
                              WHERE name LIKE {search_term}
                              '''),
        'mediums': db_query(f'''
                            SELECT * FROM Mediums
                            WHERE name LIKE {search_term}
                            '''),
        'artists': db_query(f'''
                            SELECT * FROM Artists
                            WHERE name LIKE {search_term}
                            ''')
    }


# ROUTES FOR WEBPAGES
@app.route('/')
def home():
    return render_template(
        'home.html',
        # Query to showcase newly added content
        latest_mediums=db_query('''
                                SELECT * FROM Mediums
                                ORDER BY created_at DESC LIMIT 4
                                '''),
        latest_artstyles=db_query('''
                                  SELECT * FROM ArtStyles
                                  ORDER BY created_at DESC LIMIT 4
                                  '''),
        latest_artists=db_query('''
                                SELECT * FROM Artists
                                ORDER BY created_at DESC LIMIT 4
                                ''')
    )


# Showcases navigation of artstyles
@app.route('/artstyle')
def artstylenav():
    return render_template('artstylenav.html',
                           artstyles=db_query("SELECT * FROM ArtStyles"))


@app.route('/medium')
def mediumsnav():
    return render_template('mediumsnav.html',
                           mediums=db_query("SELECT * FROM Mediums"))


@app.route('/artist')
def artistnav():
    return render_template('artistnav.html',
                           artists=db_query("SELECT * FROM Artists"))


@app.route('/artstyle/<int:id>')
def artstyle(id):
    artstyle = db_query(f"SELECT * FROM ArtStyles WHERE id={id}",
                        multiple=False)
    if not artstyle:
        return render_template('error.html', message="ArtStyle not found"), 404
    artworks = db_query(f'''
                        SELECT * FROM Artworks
                        WHERE artstyle_id={id} ORDER BY year
                        ''')
    return render_template('artstyle.html', artstyle=artstyle,
                           artworks=artworks)


@app.route('/medium/<int:id>')
def medium(id):
    medium = db_query(f"SELECT * FROM Mediums WHERE id={id}", multiple=False)
    if not medium:
        return render_template('error.html', message="Medium not found"), 404
    artworks = db_query(f'''
                        SELECT * FROM Artworks
                        WHERE medium_id={id} ORDER BY year
                        ''')
    return render_template('medium.html', medium=medium, artworks=artworks)


@app.route('/artist/<int:id>')
def artist(id):
    artist = db_query(f"SELECT * FROM Artists WHERE id={id}", multiple=False)
    if not artist:
        return render_template('error.html', message="Artist not found"), 404
    artworks = db_query(f'''
                        SELECT * FROM Artworks
                        WHERE artist_id={id} ORDER BY year
                        ''')
    return render_template('artist.html', artist=artist, artworks=artworks)


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    results = query_database(search_term)
    no_results = all(len(result) == 0 for result in results.values())
    return render_template('search.html', results=results,
                           no_results=no_results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
