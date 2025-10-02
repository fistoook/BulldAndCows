import os
import csv

CSV_FILE = "players.csv"
CSV_HEADERS = ["Name", "Type", "Wins", "Losses"]

def register_players(players):
    """
    Ensure all players have correct wins/losses from CSV or are added as new.
    Machine players are skipped.
    """
    ensure_csv_exists()
    existing_players = load_players_from_csv()

    for player in players:
        if player.type == "machine":
            continue  # skip machine players

        # Look for player in existing CSV
        found = False
        for row in existing_players:
            if player.name == row["Name"]:
                player.wins = int(row["Wins"])
                player.losses = int(row["Losses"])
                found = True
                break

        # Add new player if not found
        if not found:
            register_new_player(player)
            player.wins = 0
            player.losses = 0

def register_new_player(player):
    """Append a new human player to the CSV."""
    with open("players.csv", mode = "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([player.name, 'human', 0,0])

def ensure_csv_exists():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)

def load_players_from_csv():
    """Return a list of dictionaries representing existing human players."""
    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)  # convert iterator to list

def update_player_log(player, filename="players.csv"):
    rows = []

    # Read all rows
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Name"] == player.name:
                # Update the player's record
                row["Wins"] = str(player.wins)
                row["Losses"] = str(player.losses)
            rows.append(row)

    # Write everything back
    with open(filename, mode="w", newline="") as file:
        fieldnames = ["Name", "Type", "Wins", "Losses"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)