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


# I struggle so I have test html ; will be removed in the final product

@app.route('/test')
def test():
    return render_template('test.html')


# Teacher's search function that I have no clue how to do

# @app.route('/')
# def index():
    return render_template('search.html')


# @app.route('/search', methods=['GET', 'POST'])
# def search():
    if request.method == 'POST':
        search = request.form.get('searchterm')
        return f'You asked to search for \"{search}\"'
    else:
        return "poop"

# Search Function


@app.route('/search')
def search():
    query = request.args.get('query')
    artstyles = []
    mediums = []
    if query:
        conn = sqlite3.connect('ARTGUIDE.db')
        c = conn.cursor()
        # Perform search queries for both tables with multiline SQL
        c.execute(
            '''
            SELECT id, name
            FROM ArtStyles
            WHERE name LIKE ?
            ''',
            ('%' + query + '%',)
        )
        artstyles = c.fetchall()  # Fetch all rows
        c.execute(
            '''
            SELECT id, name
            FROM Mediums
            WHERE name LIKE ?
            ''',
            ('%' + query + '%',)
        )
        mediums = c.fetchall()  # Fetch all rows
        conn.close()
    return render_template(
        'search.html',
        artstyles=artstyles,
        mediums=mediums,
        query=query
    )


if __name__ == '__main__':
    app.run(debug=True)
