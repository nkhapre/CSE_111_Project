import pandas as pd

# Load data
file_path = 'PLAYER_CAREER_STATS.csv'
data = pd.read_csv(file_path)

# Drop unnecessary columns explicitly
data = data.drop(columns=['PLAYER_AGE', 'SEASON_ID', 'TEAM_ID', 'LEAGUE_ID', 'TEAM_ABBREVIATION', 'Player_STATUS'], errors='ignore')

# Define the columns to exclude from summing (those to be averaged)
exclude_from_sum = ['FG_PCT', 'FG3_PCT', 'FT_PCT']

# Prepare an empty list to collect the results
career_stats_list = []

# Sort the data by PLAYER_ID to process each player consecutively
data = data.sort_values(by='PLAYER_ID')

# Initialize variables to store the sum for each player and the count for averaging
current_player_id = None
player_sum = {col: 0 for col in data.select_dtypes(include='number').columns if col not in exclude_from_sum}
player_avg = {col: 0 for col in exclude_from_sum}
game_count = 0  # To track the number of games per player

# Iterate through the rows of the dataset
i = 0
while i < len(data):
    row = data.iloc[i]
    player_id = row['PLAYER_ID']
    
    if player_id == current_player_id:
        # Add the stats to the current sum for non-excluded columns
        for col in player_sum:
            player_sum[col] += row[col]
        
        # Add the stats to the current avg for excluded columns
        for col in player_avg:
            player_avg[col] += row[col]
        
        game_count += 1
    else:
        # If we encounter a new player, store the previous player's data
        if current_player_id is not None:
            player_sum['PLAYER_ID'] = current_player_id
            player_sum['GP'] = game_count
            # Calculate average for the excluded columns
            for col in player_avg:
                player_avg[col] /= game_count  # Averaging the stats
            # Add the averages to the player stats
            player_sum.update(player_avg)
            career_stats_list.append(player_sum)

        # Reset for the new player
        current_player_id = player_id
        player_sum = {col: 0 for col in data.select_dtypes(include='number').columns if col not in exclude_from_sum}
        player_avg = {col: 0 for col in exclude_from_sum}
        game_count = 0
        
        # Add the current row stats
        for col in player_sum:
            player_sum[col] += row[col]
        
        for col in player_avg:
            player_avg[col] += row[col]
        
        game_count += 1
    
    i += 1

# After the loop, append the last player's data
if current_player_id is not None:
    player_sum['PLAYER_ID'] = current_player_id
    player_sum['GP'] = game_count
    for col in player_avg:
        player_avg[col] /= game_count  # Averaging the stats
    player_sum.update(player_avg)
    career_stats_list.append(player_sum)

# Convert the list of dictionaries to a DataFrame
career_stats = pd.DataFrame(career_stats_list)

# Round all numeric columns to 2 decimal places (including averages)
career_stats = career_stats.round(2)

# Apply integer conversion to all columns except those in exclude_from_sum
for col in career_stats.select_dtypes(include='number').columns:
    if col not in exclude_from_sum:
        career_stats[col] = career_stats[col].astype(int)

# Save the results to a CSV file
career_stats.to_csv('career_stats.csv', index=False)
