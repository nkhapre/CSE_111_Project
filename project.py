from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_PATH = "Checkpoint2-database.sqlite3"
PER_PAGE = 10  # Number of records per page

def get_db_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def paginate(query, params, page):
    offset = (page - 1) * PER_PAGE
    query += ' LIMIT ? OFFSET ?'
    params.extend([PER_PAGE, offset])
    return query, params

@app.route('/')
def index():
    """Homepage: Display all players with pagination."""
    page = int(request.args.get('page', 1))
    query, params = paginate('SELECT * FROM player', [], page)

    connection = get_db_connection()
    players = connection.execute(query, params).fetchall()
    total = connection.execute('SELECT COUNT(*) FROM player').fetchone()[0]
    connection.close()

    return render_template('index.html', players=players, page=page, total=total, per_page=PER_PAGE)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search players with filtering, sorting, and pagination."""
    player_name = request.form.get('player_name', '')
    team = request.form.get('team', '')
    position = request.form.get('position', '')
    sort_by = request.form.get('sort_by', 'p_name')
    page = int(request.args.get('page', 1))

    query = 'SELECT * FROM player WHERE 1=1'
    params = []

    if player_name:
        query += ' AND p_name LIKE ?'
        params.append(f"%{player_name}%")
    if team:
        query += ' AND p_team = ?'
        params.append(team)
    if position:
        query += ' AND p_position = ?'
        params.append(position)

    query += f' ORDER BY {sort_by}'
    query, params = paginate(query, params, page)

    connection = get_db_connection()
    players = connection.execute(query, params).fetchall()
    total = connection.execute('SELECT COUNT(*) FROM player WHERE 1=1', params[:-2]).fetchone()[0]
    connection.close()

    return render_template(
        'search.html', players=players, player_name=player_name, team=team, position=position, sort_by=sort_by,
        page=page, total=total, per_page=PER_PAGE
    )

@app.route('/add', methods=['GET', 'POST'])
def add_player():
    """Add a new player."""
    if request.method == 'POST':
        name = request.form['p_name']
        number = request.form['p_number']
        team = request.form['p_team']
        position = request.form['p_position']
        season = request.form['p_season']

        connection = get_db_connection()
        connection.execute(
            'INSERT INTO player (p_name, p_number, p_team, p_position, p_season) VALUES (?, ?, ?, ?, ?)',
            (name, number, team, position, season)
        )
        connection.commit()
        connection.close()

        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    """Edit an existing player's details."""
    connection = get_db_connection()
    player = connection.execute('SELECT * FROM player WHERE id = ?', (player_id,)).fetchone()
    if not player:
        connection.close()
        return redirect('/')

    if request.method == 'POST':
        name = request.form['p_name']
        number = request.form['p_number']
        team = request.form['p_team']
        position = request.form['p_position']
        season = request.form['p_season']

        connection.execute(
            'UPDATE player SET p_name = ?, p_number = ?, p_team = ?, p_position = ?, p_season = ? WHERE id = ?',
            (name, number, team, position, season, player_id)
        )
        connection.commit()
        connection.close()
        return redirect('/')

    connection.close()
    return render_template('edit.html', player=player)

@app.route('/delete/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    """Delete a player."""
    connection = get_db_connection()
    connection.execute('DELETE FROM player WHERE id = ?', (player_id,))
    connection.commit()
    connection.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
