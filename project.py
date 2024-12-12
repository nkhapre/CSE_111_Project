from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_PATH = "Checkpoint2-database.sqlite3"

def get_db_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/home')
def home():
    """Home page with a welcome message."""
    return render_template('home.html')

@app.route('/')
def root():
    """Redirect root URL to /home."""
    return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search or sort players based on form input."""
    # Use appropriate method
    method = request.form if request.method == 'POST' else request.args
    player_name = method.get('p_name', '').strip()
    team = method.get('p_team', '').strip()
    position = method.get('p_position', '').strip()
    player_key = method.get('p_key', '').strip()
    sort_by = method.get('sort_by', 'p_name').strip()
    action = method.get('action', 'search')

    query = "SELECT * FROM player WHERE 1=1"
    params = []

    # Add filters
    if player_name:
        query += ' AND p_name LIKE ?'
        params.append(f"%{player_name}%")
    if team:
        query += ' AND p_team LIKE ?'
        params.append(f"%{team}%")
    if position:
        query += ' AND p_position LIKE ?'
        params.append(f"%{position}%")
    if player_key:
        query += ' AND p_key = ?'
        params.append(player_key)

    # Sorting
    query += f' ORDER BY {sort_by}' if action == 'sort' else ' ORDER BY p_name'

    # Execute query
    connection = get_db_connection()
    print("Final Query:", query)  # Debug
    print("Params:", params)      # Debug
    players = connection.execute(query, params).fetchall()

    # Optional: Count total results
    total = len(players)
    connection.close()

    return render_template(
        'search.html', players=players, player_name=player_name, team=team, position=position,
        player_key=player_key, sort_by=sort_by, total=total
    )

@app.route('/searchc', methods=['GET', 'POST'])
def searchc():
    """Search or sort coachs based on form input."""
    coach_name = request.form.get('coach_name', '').strip()
    team = request.form.get('team', '').strip()
    coach_key = request.form.get('coach_key', '').strip()  # New: Get c_key from the form
    sort_by = request.form.get('sort_by', 'c_name').strip()
    action = request.form.get('action', 'search')  # Determine if it's a search or sort action
    page = int(request.args.get('page', 1))

    # Base query
    query = 'SELECT * FROM coach WHERE 1=1'
    params = []

    # Add conditions for search fields
    if coach_name:
        query += ' AND c_name LIKE ?'
        params.append(f"%{coach_name}%")
    if team:
        query += ' AND c_team LIKE ?'
        params.append(f"%{team}%")
    if coach_key:  # New: Add c_key filter
        query += ' AND c_key = ?'
        params.append(coach_key)

    # Add sorting if the action is "sort"
    if action == 'sort':
        query += f' ORDER BY {sort_by}'
    else:
        # Default sorting
        query += ' ORDER BY c_name'

    # Execute query
    connection = get_db_connection()
    coaches = connection.execute(query, params).fetchall()

    # Count total results
    total_query = 'SELECT COUNT(*) FROM coach WHERE 1=1'
    total_params = params[:-2]  # Exclude pagination params
    if coach_name:
        total_query += ' AND c_name LIKE ?'
    if team:
        total_query += ' AND c_team LIKE ?'
    if coach_key:
        total_query += ' AND c_key = ?'

    total = connection.execute(total_query, total_params).fetchone()[0]
    connection.close()

    return render_template(
        'searchc.html', coaches=coaches, coach_name=coach_name, team=team, 
        coach_key=coach_key, sort_by=sort_by, page=page, total=total
    )

@app.route('/searcht', methods=['GET', 'POST'])
def searcht():
    """Search or sort teams based on form input."""
    team_name = request.form.get('team_name', '').strip()
    team_city = request.form.get('team_city', '').strip()  # New: Get c_key from the form
    team_conference = request.form.get('team_conference', '').strip()  # New: Get c_key from the form
    sort_by = request.form.get('sort_by', 't_name').strip()
    action = request.form.get('action', 'search')  # Determine if it's a search or sort action
    page = int(request.args.get('page', 1))

    # Base query
    query = 'SELECT * FROM team WHERE 1=1'
    params = []

    # Add conditions for search fields
    if team_name:
        query += ' AND t_name LIKE ?'
        params.append(f"%{team_name}%")
    if team_city:
        query += ' AND t_city LIKE ?'
        params.append(f"%{team_city}%")
    if team_conference:  # New: Add c_key filter
        query += ' AND t_conference = ?'
        params.append(team_conference)

    # Add sorting if the action is "sort"
    if action == 'sort':
        query += f' ORDER BY {sort_by}'
    else:
        # Default sorting
        query += ' ORDER BY t_name'

    # Execute query
    connection = get_db_connection()
    teams = connection.execute(query, params).fetchall()

    # Count total results
    total_query = 'SELECT COUNT(*) FROM team WHERE 1=1'
    total_params = params[:-2]  # Exclude pagination params
    if team_name:
        total_query += ' AND t_name LIKE ?'
    if team_city:
        total_query += ' AND t_city LIKE ?'
    if team_conference:
        total_query += ' AND t_conference = ?'

    total = connection.execute(total_query, total_params).fetchone()[0]
    connection.close()

    return render_template(
        'searcht.html', teams=teams, team_name=team_name, team_city=team_city, 
        team_conference = team_conference, sort_by=sort_by, page=page, total=total
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
        p_key = request.form['p_key']

        connection = get_db_connection()
        connection.execute(
            """INSERT INTO player (p_name, p_number, p_team, p_position, p_key, p_season) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, number, team, position, season)
        )
        connection.commit()
        connection.close()

        return redirect('/')
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(PLAYER_ID) FROM career_stats")
    max_player_id = cursor.fetchone()[0] 
    connection.close()

    next_player_id = max_player_id + 1 if max_player_id is not None else 1
    return render_template('add.html', next_player_id=next_player_id)



@app.route('/addc', methods=['GET', 'POST'])
def add_coach():
    """Add a new coach."""
    if request.method == 'POST':
        name = request.form['c_name']
        team = request.form['c_team']
        key = request.form['c_key']
        season = request.form['c_season']

        connection = get_db_connection()
        connection.execute(
            'INSERT INTO coach (c_name, c_team, c_key, c_season) VALUES (?, ?, ?, ?)',
            (name, team, key, season)
        )
        connection.commit()
        connection.close()

        return redirect('/')
    return render_template('addc.html')

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

        connection.execute(
            'UPDATE player SET p_name = ?, p_number = ?, p_team = ?, p_position = ?, p_season = ? WHERE p_key = ?',
            (name, number, team, position, p_key)
        )
        connection.commit()
        connection.close()
        return redirect('/')

    connection.close()
    return render_template('edit.html', player=player)



@app.route('/editc/<int:c_key>', methods=['GET', 'POST'])
def edit_coach(c_key):
    """Edit an existing coach's details."""
    connection = get_db_connection()
    coach = connection.execute('SELECT * FROM coach WHERE c_key = ?', (c_key,)).fetchone()
    if not coach:
        connection.close()
        return redirect('/')

    if request.method == 'POST':
        name = request.form['c_name']
        team = request.form['c_team']
        season = request.form['c_season']

        connection.execute(
            'UPDATE coach SET c_name = ?, c_team = ?, c_season = ? WHERE c_key = ?',
            (name, team, season, c_key)
        )
        connection.commit()
        connection.close()
        return redirect('/')

    connection.close()
    return render_template('editc.html', coach=coach)

@app.route('/deletec/<int:c_key>', methods=['POST'])
def delete_coach(c_key):
    """Delete a coach."""
    connection = get_db_connection()
    connection.execute('DELETE FROM coach WHERE c_key = ?', (c_key,))
    connection.commit()
    connection.close()
    return redirect('/home')


@app.route('/delete/<int:p_key>', methods=['POST'])
def delete_player(p_key):
    """Delete a player."""
    connection = get_db_connection()
    connection.execute('DELETE FROM player WHERE p_key = ?', (p_key,))
    connection.commit()
    connection.close()
    return redirect('/home')

        
@app.route('/allplayers', methods=['GET', 'POST'])
def index():
    """Display all players."""
    connection = get_db_connection()
    players = connection.execute("""
        SELECT * FROM player
        JOIN career_stats ON career_stats.p_key = player.p_key
    """).fetchall()
    connection.close()
    return render_template('index.html', players=players)

@app.route('/allcoaches', methods=['GET', 'POST'])
def coaches():
    """Display all coaches."""
    connection = get_db_connection()
    coaches = connection.execute('SELECT * FROM coach').fetchall()
    connection.close()
    return render_template('coaches.html', coaches=coaches)

@app.route('/teams', methods = ['GET', 'POST'])
def teams():
    """Display all teams."""
    connection = get_db_connection()
    teams = connection.execute('SELECT * FROM team').fetchall()
    connection.close()
    return render_template('teams.html', teams=teams)

if __name__ == '__main__':
    app.run(debug=True)
