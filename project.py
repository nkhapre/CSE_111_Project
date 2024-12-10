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

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search or sort players based on form input."""
    player_name = request.form.get('player_name', '').strip()
    team = request.form.get('team', '').strip()
    position = request.form.get('position', '').strip()
    sort_by = request.form.get('sort_by', 'p_name').strip()
    action = request.form.get('action', 'search')  # Determine if it's a search or sort action
    page = int(request.args.get('page', 1))

    # Base query
    query = 'SELECT * FROM player WHERE 1=1'
    params = []

    # Add conditions for search fields
    if player_name:
        query += ' AND p_name LIKE ?'
        params.append(f"%{player_name}%")
    if team:
        query += ' AND p_team LIKE ?'
        params.append(f"%{team}%")
    if position:
        query += ' AND p_position LIKE ?'
        params.append(f"%{position}%")

    # Add sorting if the action is "sort"
    if action == 'sort':
        query += f' ORDER BY {sort_by}'
    else:
        # Default sorting
        query += ' ORDER BY p_name'

    # Add pagination
    offset = (page - 1) * PER_PAGE
    query += ' LIMIT ? OFFSET ?'
    params.extend([PER_PAGE, offset])

    # Execute query
    connection = get_db_connection()
    players = connection.execute(query, params).fetchall()

    # Count total results
    total_query = 'SELECT COUNT(*) FROM player WHERE 1=1'
    total_params = params[:-2]  # Exclude pagination params
    if player_name:
        total_query += ' AND p_name LIKE ?'
    if team:
        total_query += ' AND p_team LIKE ?'
    if position:
        total_query += ' AND p_position LIKE ?'

    total = connection.execute(total_query, total_params).fetchone()[0]
    connection.close()

    return render_template(
        'search.html', players=players, player_name=player_name, team=team, position=position,
        sort_by=sort_by, page=page, total=total, per_page=PER_PAGE
    )



@app.route('/add', methods=['GET', 'POST'])
def add_player():
    """Add a new player."""
    if request.method == 'POST':
        name = request.form['p_name']
        number = request.form['p_number']
        team = request.form['p_team']
        position = request.form['p_position']
        key = request.form['p_key']
        season = request.form['p_season']

        connection = get_db_connection()
        connection.execute(
            'INSERT INTO player (p_name, p_number, p_team, p_position, p_key, p_season) VALUES (?, ?, ?, ?, ?, ?)',
            (name, number, team, position, key, season)
        )
        connection.commit()
        connection.close()

        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:p_key>', methods=['GET', 'POST'])
def edit_player(p_key):
    """Edit an existing player's details."""
    connection = get_db_connection()
    player = connection.execute('SELECT * FROM player WHERE p_key = ?', (p_key,)).fetchone()
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
            'UPDATE player SET p_name = ?, p_number = ?, p_team = ?, p_position = ?, p_season = ? WHERE p_key = ?',
            (name, number, team, position, season, p_key)
        )
        connection.commit()
        connection.close()
        return redirect('/')

    connection.close()
    return render_template('edit.html', player=player)

@app.route('/delete/<int:p_key>', methods=['POST'])
def delete_player(p_key):
    """Delete a player."""
    connection = get_db_connection()
    connection.execute('DELETE FROM player WHERE p_key = ?', (p_key,))
    connection.commit()
    connection.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
