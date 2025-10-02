import tkinter as tk
from tkinter import ttk
from dataManager import register_players
import csv

######################################## main ########################################
def main():
    from game import Tournament
    # create the screen and styles
    root = tk.Tk()
    root.title("Bulls and Cows")
    style = ttk.Style(root)

    # center the screen, style widgets
    center_window(root)
    applyStyles(style)

    # select mode
    number_of_players = pick_game_mode(root)

    # nickname entry
    player1, player2 = nickname_entry(root, number_of_players)

    # secret number length
    encoding_length = ask_encoding_length(root)

    tournament = Tournament(player1, player2, encoding_length, root)
    tournament.startGame()

    # player register
    register_players([player1, player2])

    root.mainloop()
    return



######################################## center window ########################################
def center_window(root, width = 1200, height = 800):
    """ center the tkinter window """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position x, y to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")



######################################## apply styles ########################################
def applyStyles(style):
    """ styles the buttons """
    style.theme_use("clam")
    style.configure(
        "Mode.TButton",
        font=("Segoe UI", 12, "bold"),
        padding=10,
        foreground="#333333",
        background="#f0f0f0"
    )

    # Add hover effect
    style.map(
        "Mode.TButton",
        background=[("active", "#4CAF50")],
        foreground=[("active", "white")]
    )


######################################## pick game mode ########################################
def pick_game_mode(root):
    """ asks user to pick one of two game mods by clicking on graphical buttons.
        returns a mark for the picked game mode.
    """
    game_mode_var = tk.IntVar(value=0)
    destroy_var = tk.IntVar(value=0)

    # UI setup
    frame = tk.Frame(root)
    frame.pack()

    label = tk.Label(frame, text="Select Playing Mode", font=("Segoe UI", 20), background="#ffffff",
                     foreground="#333333")
    label.pack(pady=10)

    # on-click functions
    def Two_player_mode_on_click():
        Two_player_mode.pack_forget()
        Single_player_mode.pack_forget()
        label.config(text="Two Player Mode Selected!", foreground='green')
        game_mode_var.set(2)  # 2 = two players
        root.after(2000, lambda: destroy_var.set(1))  # schedule frame removal after 2s

    def Single_player_mode_on_click():
        Two_player_mode.pack_forget()
        Single_player_mode.pack_forget()
        label.config(text="Single Player Mode Selected!", foreground='green')
        game_mode_var.set(1)  # 1 = single player
        root.after(1000, lambda: destroy_var.set(1))  # schedule frame removal after 2s

    Two_player_mode = ttk.Button(frame, text="Two Player", command=Two_player_mode_on_click)
    Two_player_mode.pack(pady=10, fill="x", padx=20)

    Single_player_mode = ttk.Button(frame, text="Single Player", command=Single_player_mode_on_click)
    Single_player_mode.pack(pady=10, fill="x", padx=20)

    # BLOCK until a value is set
    root.wait_variable(game_mode_var)

    # BLOCK again until the 2-second delay is over
    root.wait_variable(destroy_var)

    # Destroy frame after delay
    frame.destroy()

    return game_mode_var.get()



######################################## nickname_entry ########################################
def nickname_entry(root, number_of_players):
    from game import Player
    """ asks players to enter nicknames.
        entering a nickname is required.
        after enterance, update the objects of class Player and the players.csv file.
        returns two Player objects (the players, a player can be AI)
    """
    player1 = Player('', 'human', 0, 0)
    player2 = Player('', 'human', 0, 0)
    players_ready_var = tk.IntVar(value = 0)
    frame_destroyed_var = tk.IntVar(value=0)

    def destroy_frame_later():
        frame.destroy()
        frame_destroyed_var.set(1)

    def add_player_1():
        name = first_player_entry.get()
        if name and name != "A nickname is required.":
            player1.name = name
            first_player_label.destroy()
            first_player_entry.destroy()
            first_player_button.destroy()
            success_label_1 = tk.Label(frame, text = f"Player 1: {name}", font=("Segoe UI", 16), background="#ffffff", foreground="blue")
            success_label_1.grid(row=0, column=0)
            if number_of_players == 1 or (number_of_players == 2 and player2.name):
                ready_message = tk.Label(frame, text="Starting game...", font=("Segoe UI", 20), background="#ffffff",
                                         foreground="black")
                ready_message.grid(row=3, column=0)
                root.after(2000, destroy_frame_later)
                players_ready_var.set(1)
        else:
            first_player_entry.delete(0, tk.END)
            first_player_entry.insert(0, "A nickname is required.")
            first_player_entry.after(1000, lambda: first_player_entry.delete(0, tk.END))

    def add_player_2():
        name = second_player_entry.get()
        if name and name != "A nickname is required.":
            player2.name = name
            second_player_label.destroy()
            second_player_entry.destroy()
            second_player_button.destroy()
            success_label_2 = tk.Label(frame, text = f"Player 2: {name}", font=("Segoe UI", 16), background="#ffffff", foreground="red")
            success_label_2.grid(row=1, column=0)
            if player1.name:
                ready_message = tk.Label(frame, text="Starting game...", font=("Segoe UI", 20), background="#ffffff",
                                         foreground="black")
                ready_message.grid(row=3, column=0)
                root.after(2000, destroy_frame_later)
                players_ready_var.set(1)
        else:
            second_player_entry.delete(0, tk.END)
            second_player_entry.insert(0, "A nickname is required.")
            second_player_entry.after(1000, lambda: second_player_entry.delete(0, tk.END))

    # UI setup
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    first_player_label = tk.Label(frame, text = "Player 1, Enter Nickname: ", font=("Segoe UI", 16), background="#ffffff", foreground="blue")
    first_player_label.grid(row=0, column=0)
    first_player_entry = tk.Entry(frame)
    first_player_entry.grid(row=0, column=1)
    first_player_button = tk.Button(frame, text="✓", width=3, command = add_player_1)
    first_player_button.grid(row=0, column=2)
    frame.rowconfigure(0, pad=20)

    if (number_of_players == 2):
        second_player_label = tk.Label(frame, text="Player 2, Enter Nickname", font=("Segoe UI", 16), background="#ffffff", foreground="red")
        second_player_label.grid(row=1, column=0)
        second_player_entry = tk.Entry(frame)
        second_player_entry.grid(row=1, column=1)
        second_player_button = tk.Button(frame, text="✓", width=3, command = add_player_2)
        second_player_button.grid(row=1, column=2)
    else:
        player2.name = "AI🤖"
        player2.type = "machine"

    # BLOCK execution until both players are ready
    root.wait_variable(players_ready_var)

    # wait until the frame is actually destroyed
    root.wait_variable(frame_destroyed_var)

    return player1, player2



######################################## ask_encoding_length ########################################
def ask_encoding_length(root, min_len=3, max_len=6):
    """ creates an entry one th screen asking the user to
        enter the length of the secret number.
        allowed length is 3-6. if not allowed, wil notify and ask again.
        returns the entered number.
    """
    encoding_var = tk.IntVar(value=0)  # will store the result

    # UI setup
    frame = tk.Frame(root, bg="#ffffff")
    frame.pack(expand=True)  # place the frame in root with pack (ok here!)

    label = tk.Label(
        frame,
        text=f"Enter the length of the secret number ({min_len}-{max_len}):",
        font=("Segoe UI", 16),
        background="#ffffff",
        foreground="#333333"
    )
    label.grid(row=0, column=0, columnspan=2, pady=10)

    entry = tk.Entry(frame, font=("Segoe UI", 14))
    entry.grid(row=1, column=0, padx=5, pady=5)

    message_label = tk.Label(frame, text="", font=("Segoe UI", 12), bg="#ffffff", fg="red")
    message_label.grid(row=2, column=0, columnspan=2, pady=5)

    def submit_length():
        try:
            value = int(entry.get())
            if min_len <= value <= max_len:
                encoding_var.set(value)
            else:
                message_label.config(text=f"Please enter a number between {min_len} and {max_len}.")
                entry.delete(0, tk.END)
        except ValueError:
            message_label.config(text="Please enter a valid number.")
            entry.delete(0, tk.END)

    submit_button = tk.Button(frame, text="OK", width=6, command=submit_length)
    submit_button.grid(row=1, column=1, padx=5)

    # BLOCK execution until encoding_var is set
    root.wait_variable(encoding_var)

    # Destroy the frame after a valid input
    frame.destroy()

    return encoding_var.get()



######################################### clear root #########################################
def clear_root(root):
    """ clears all tkinter widgets on the screen """
    for widget in root.winfo_children():
        widget.destroy()



######################################### leaderboard #########################################
def show_leaderboard(root, csv_file="players.csv"):
    """ display a leaderboard sorted by most wins """
    # Read CSV file
    players = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            players.append({
                "Name": row["Name"],
                "Type": row["Type"],
                "Wins": int(row["Wins"]),
                "Losses": int(row["Losses"])
            })

    # Sort players by wins (descending)
    players.sort(key=lambda p: p["Wins"], reverse=True)

    # Title
    tk.Label(root, text="🏆 Leaderboard 🏆", font=("Segoe UI", 20, "bold"), fg="blue").pack(pady=20)

    # Column headers
    header_frame = tk.Frame(root)
    header_frame.pack(pady=5)
    tk.Label(header_frame, text="Rank", font=("Segoe UI", 14, "bold"), width=6).grid(row=0, column=0)
    tk.Label(header_frame, text="Name", font=("Segoe UI", 14, "bold"), width=15).grid(row=0, column=1)
    tk.Label(header_frame, text="Type", font=("Segoe UI", 14, "bold"), width=10).grid(row=0, column=2)
    tk.Label(header_frame, text="Wins", font=("Segoe UI", 14, "bold"), width=10).grid(row=0, column=3)
    tk.Label(header_frame, text="Losses", font=("Segoe UI", 14, "bold"), width=10).grid(row=0, column=4)

    # Colors for top 3
    medals = [
        ("🥇", "gold"),
        ("🥈", "silver"),
        ("🥉", "#cd7f32")  # bronze
    ]

    # Players list
    for i, p in enumerate(players):
        row_frame = tk.Frame(root)
        row_frame.pack()

        if i < 3:  # Top 3 players
            medal, color = medals[i]
            rank_text = f"{medal} {i+1}"
            fg_color = color
            font_style = ("Segoe UI", 12, "bold")
        else:
            rank_text = str(i+1)
            fg_color = "black"
            font_style = ("Segoe UI", 12)

        tk.Label(row_frame, text=rank_text, font=font_style, fg=fg_color, width=6).grid(row=0, column=0)
        tk.Label(row_frame, text=p["Name"], font=font_style, fg=fg_color, width=15).grid(row=0, column=1)
        tk.Label(row_frame, text=p["Type"], font=font_style, width=10).grid(row=0, column=2)
        tk.Label(row_frame, text=p["Wins"], font=font_style, fg="green", width=10).grid(row=0, column=3)
        tk.Label(row_frame, text=p["Losses"], font=font_style, fg="red", width=10).grid(row=0, column=4)

    # Back button
    tk.Button(root, text="Exit Game➯", font=("Segoe UI", 12), command=lambda: root.quit()).pack(pady=20)
    tk.Button(root, text="New Game↺", font=("Segoe UI", 12), command=lambda: restart()).pack(pady=40)

    def restart():
        root.destroy()
        main()

if __name__ == "__main__":
    main()