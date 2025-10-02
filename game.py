import random
from dataManager import update_player_log
from main import *

############################## class Player #################################
class Player:
    def __init__(self, name, type, wins, losses):
        self.name = name
        self.type = type
        self.wins = wins
        self.losses = losses

    def __str__(self):
        return f"{self.name}, you have {self.wins} wins and {self.losses} losses"

    def record_win(self):
        self.wins+=1

    def record_loss(self):
        self.losses+=1


############################## class Tournament #################################
class Tournament:
    def __init__(self, player1, player2, encoding_length, root):
        self.player1 = player1
        self.player2 = player2
        self.encoding_length = encoding_length
        self.root = root
        self.attempts = self.calculate_attempts()
        self.left_frame = tk.Frame(self.root, bg="lightblue", width=300, height=400)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame = tk.Frame(self.root, bg="lightcoral", width=300, height=400)
        self.right_frame.pack(side="right", fill="both", expand=True)
        tk.Label(self.left_frame, text=f"Player 1: {self.player1.name}", font=("Segoe UI", 16),
                 bg="lightblue", fg="blue").place(relx=0.5, rely=0.1, anchor="center")
        tk.Label(self.right_frame, text=f"Player 2: {self.player2.name}", font=("Segoe UI", 16),
                 bg="lightcoral", fg="red").place(relx=0.5, rely=0.1, anchor="center")

    def startGame(self):
        if self.player2.type == "machine":
            currentGame = GameSinglePlayer(self.player1, self.encoding_length, self.root, self.attempts, self.left_frame, self.right_frame)
            currentGame.playSinglePlayer()
        else:
            currentGame = GameTwoPlayer(self.player1, self.player2, self.encoding_length, self.root, self.attempts, self.left_frame, self.right_frame)
            currentGame.playTwoPlayer()

    def calculate_attempts(self):
        """ calculate the amount of attempts based on the length of the secret number """
        if self.encoding_length == 3:
            return 6
        elif self.encoding_length == 4:
            return 10
        elif self.encoding_length == 5:
            return 14
        else:
            return 18


############################## class Game Single Player #################################
class GameSinglePlayer:
    def __init__(self, player, encoding_length, root, attempts, left_frame, right_frame):
        """ constructor of a single player game """
        self.player = player
        self.encoding_length = encoding_length
        self.root = root
        self.guess_index = 0
        self.attempts = attempts
        self.left_frame = left_frame
        self.right_frame = right_frame

    def playSinglePlayer(self):
        """ Play a Single-Player game """
        # cute encoding animation: add underscores
        labels = []
        for i in range(self.encoding_length):
            lbl = tk.Label(self.right_frame, text="_", font=("Segoe UI", 32),
                           bg="lightcoral", fg="black")
            lbl.place(relx=0.5 + (i - self.encoding_length/2) * 0.1, rely=0.5, anchor="center")
            labels.append(lbl)

        # ENCODED NUMBER - random
        self.encoded_number = random.sample(range(10), self.encoding_length)

        # RESULT FRAME - for user input and guess log
        result_frame = tk.Frame(self.left_frame, bg="lightblue")
        result_frame.pack(pady=100)

        # Prompt label (only once)
        prompt_label = tk.Label(result_frame,
                                text=f"Enter your guess ({self.encoding_length} unique digits):",
                                font=("Segoe UI", 14), bg="lightblue", fg="black")
        prompt_label.pack(pady=5)

        # Entry for guess
        self.guess_var = tk.StringVar()
        entry = tk.Entry(result_frame, textvariable=self.guess_var, font=("Segoe UI", 14))
        entry.pack(pady=5)
        entry.focus()

        # Message label for errors
        msg_label = tk.Label(result_frame, text="", font=("Segoe UI", 12), bg="lightblue", fg="red")
        msg_label.pack()

        # Submit button
        btn = tk.Button(result_frame, text="Submit")
        btn.pack(pady=5)

        # History frame (persistent log of all guesses)
        history_frame = tk.Frame(result_frame, bg="white")
        history_frame.pack(pady=10, fill="x")

        # Digit labels to show last guess
        digit_frame = tk.Frame(result_frame, bg="lightblue")
        digit_frame.pack()
        self.digit_labels = []
        for _ in range(self.encoding_length):
            lbl = tk.Label(digit_frame, text="_", font=("Segoe UI", 20),
                           bg="lightblue", fg="black")
            lbl.pack(side="left", padx=5)
            self.digit_labels.append(lbl)

        # ASK FOR GUESS
        def ask_for_guess():
            valid_guess = tk.StringVar()

            def submit():
                val = self.guess_var.get()
                if not val.isdigit():
                    msg_label.config(text="Guess must contain digits only.")
                    entry.delete(0, tk.END)
                elif len(val) != self.encoding_length:
                    msg_label.config(text=f"Guess must be {self.encoding_length} digits.")
                    entry.delete(0, tk.END)
                elif len(set(val)) != len(val):
                    msg_label.config(text="All digits must be unique.")
                    entry.delete(0, tk.END)
                else:
                    valid_guess.set(val)
                    entry.delete(0, tk.END)
                    msg_label.config(text="")  # clear error message

            btn.config(command=submit)
            self.root.wait_variable(valid_guess)
            return [int(d) for d in valid_guess.get()]

        # COUNT BULLS AND COWS
        def count_bulls_and_cows(secret, guess):
            bulls = 0
            cows = 0
            secret_copy = secret[:]
            guess_copy = guess[:]

            # Count bulls
            for i in range(len(secret)):
                if guess[i] == secret[i]:
                    bulls += 1
                    secret_copy[i] = guess_copy[i] = -1  # mark matched

            # Count cows
            for g in guess_copy:
                if g != -1 and g in secret_copy:
                    cows += 1
                    secret_copy[secret_copy.index(g)] = -1

            return bulls, cows

        # UPDATE RESULTS
        def update_result(guess_digits, bulls, cows):
            gameOver = False
            # Reset digit labels
            for lbl in self.digit_labels:
                lbl.config(text="_")

            def reveal_digit(index=0):
                nonlocal gameOver
                if index < len(self.digit_labels):
                    self.digit_labels[index].config(text=str(guess_digits[index]))
                    result_frame.after(200, lambda: reveal_digit(index + 1))
                else:
                    self.guess_index += 1

                    # Add guess to history
                    tk.Label(history_frame,
                             text=f"{''.join(map(str, guess_digits))} → Bulls: {bulls}, Cows: {cows}",
                             font=("Segoe UI", 12), bg="white").pack(anchor="w")

                    if bulls == self.encoding_length:
                        gameOver = True
                        tk.Label(self.left_frame, text="🎉 Congratulations! You guessed it!",
                                 font=("Segoe UI", 16), bg="lightblue", fg="purple").pack(pady=5)
                        self.player.wins += 1
                        update_player_log(self.player)
                    elif self.guess_index >= self.attempts:
                        gameOver = True
                        tk.Label(self.left_frame,
                                 text=f"😢 You lost! The secret number was {''.join(map(str, self.encoded_number))}.",
                                 font=("Segoe UI", 16), bg="lightblue", fg="red").pack(pady=5)
                        self.player.losses += 1
                        update_player_log(self.player)
                    else:
                        # Continue guessing
                        self.root.after(200, handle_guess)

                if gameOver:
                    self.root.after(2000, lambda: show_final_screen())

            reveal_digit()

        # SHOW FINAL SCREEN
        def show_final_screen():
            clear_root(self.root)
            show_leaderboard(self.root)

        # HANDLE GUESS
        def handle_guess():
            guess_digits = ask_for_guess()
            bulls, cows = count_bulls_and_cows(self.encoded_number, guess_digits)
            update_result(guess_digits, bulls, cows)

        # START GUESSING
        def start_guessing():
            handle_guess()

        # START AI ANIMATION
        def add_star(index=0):
            if index < len(labels):
                labels[index].config(text="*")
                self.right_frame.after(800, lambda: add_star(index + 1))
            else:
                start_guessing()

        add_star()




############################## class Game Two Player #################################
class GameTwoPlayer:
    ############################### constructor ###################################
    def __init__(self, player1, player2, encoding_length, root, attempts, left_frame, right_frame):
        """ constructor of a two player game """
        self.player1 = player1
        self.player2 = player2
        self.encoding_length = encoding_length
        self.root = root
        self.attempts1 = 1
        self.attempts2 = 1
        self.total_attempts = attempts
        self.left_frame = left_frame
        self.right_frame = right_frame
        self.current_player = 1


    ############################### main game ###################################
    def playTwoPlayer(self):
        """ The main function which runs a 2-player game """
        # Step 1: Get both secret codes
        self.secret1 = self.ask_for_secret_code(self.player1, self.left_frame)
        self.animate_secret_code(self.left_frame, self.secret1)

        self.secret2 = self.ask_for_secret_code(self.player2, self.right_frame)
        self.animate_secret_code(self.right_frame, self.secret2)

        # Step 2: Setup guess areas
        self.player1_guess = tk.Frame(self.left_frame, bg="white")
        self.player2_guess = tk.Frame(self.right_frame, bg="white")

        self.guess_var1,  self.submit_btn1, self.input_frame1, self.history_frame1 = self.create_guess_area(self.player1_guess)
        self.guess_var2,  self.submit_btn2, self.input_frame2, self.history_frame2 = self.create_guess_area(self.player2_guess)

        # Step 3: Setup turn labels
        self.create_turn_labels()

        # Step 4: Attach submit button callbacks
        self.setup_submit_buttons()

        # Step 5: Start game
        self.next_turn()

    ############################### secret code input ###################################
    def ask_for_secret_code(self, player, frame):
        """ Ask a player to enter a secret code on their given frame """
        secret_var = tk.StringVar()
        valid_code = tk.StringVar()

        # Label
        label = tk.Label(
            frame,
            text=f"{player.name}, enter your secret code:",
            font=("Segoe UI", 16),
            bg=frame["bg"],
            fg="black"
        )
        label.place(relx=0.5, rely=0.4, anchor="center")

        # Entry field (show stars)
        entry = tk.Entry(
            frame,
            textvariable=secret_var,
            font=("Segoe UI", 16),
            show="*",
            justify="center"
        )
        entry.place(relx=0.5, rely=0.5, anchor="center")
        entry.focus()

        # Error message label
        error_label = tk.Label(
            frame,
            text="",
            font=("Segoe UI", 12),
            bg=frame["bg"],
            fg="red"
        )
        error_label.place(relx=0.5, rely=0.6, anchor="center")

        # Submit button
        def submit():
            val = secret_var.get()
            if not val.isdigit():
                error_label.config(text="Code must contain digits only.")
            elif len(val) != self.encoding_length:
                error_label.config(text=f"Code must be exactly {self.encoding_length} digits long.")
            elif len(set(val)) != self.encoding_length:
                error_label.config(text="All digits must be unique.")
            else:
                valid_code.set(val)  # valid input

        btn = tk.Button(
            frame,
            text="Submit",
            font=("Segoe UI", 14),
            command=submit
        )
        btn.place(relx=0.5, rely=0.7, anchor="center")

        # Wait until valid code is entered
        self.root.wait_variable(valid_code)

        # Clean up widgets
        label.destroy()
        entry.destroy()
        error_label.destroy()
        btn.destroy()
        # Return secret number as list of digits
        return [int(digit) for digit in valid_code.get()]

    ############################### animate secret ###################################
    def animate_secret_code(self, frame, code_digits):
        """ animate stars below the player's name and add a press-and-hold reveal button. """
        stars_frame = tk.Frame(frame, bg=frame["bg"])
        stars_frame.place(relx=0.5, rely=0.12, anchor="n")  # below player's name

        star_labels = []
        for i in range(len(code_digits)):
            lbl = tk.Label(stars_frame, text="_", font=("Segoe UI", 24), bg=frame["bg"], fg="black")
            lbl.pack(side="left", padx=5)
            star_labels.append(lbl)

        # Animate stars one by one
        def add_star(index=0):
            if index < len(star_labels):
                star_labels[index].config(text="*")
                stars_frame.after(400, lambda: add_star(index + 1))

        add_star()

        # Functions to show and hide secret
        def show_code(event=None):
            for i, lbl in enumerate(star_labels):
                lbl.config(text=str(code_digits[i]))

        def hide_code(event=None):
            for lbl in star_labels:
                lbl.config(text="*")

        # Reveal button with press-and-hold
        reveal_btn = tk.Button(stars_frame, text="Reveal", font=("Segoe UI", 10))
        reveal_btn.pack(side="left", padx=10)

        reveal_btn.bind("<ButtonPress-1>", show_code)  # when pressed, show digits
        reveal_btn.bind("<ButtonRelease-1>", hide_code)  # when released, hide again

    ############################### guessing area ###################################
    def create_guess_area(self, frame):
        """Create guess entry, bulls/cows labels, submit button, and history frame."""
        frame.place(relx=0.5, rely=0.2, anchor="n")  # top-aligned

        guess_var = tk.StringVar()

        # Input area
        input_frame = tk.Frame(frame, bg="white")
        input_frame.grid(row=0, column=0, pady=5)

        tk.Label(input_frame, text="Enter your guess:", font=("Segoe UI", 14), bg="white", fg="black") \
            .grid(row=0, column=0, columnspan=3, pady=5)

        entry = tk.Entry(input_frame, textvariable=guess_var, font=("Segoe UI", 14), width=12, justify="center")
        entry.grid(row=1, column=0, columnspan=3, pady=5)
        entry.focus()

        submit_btn = tk.Button(input_frame, text="Submit Guess", font=("Segoe UI", 12))
        submit_btn.grid(row=3, column=0, columnspan=3, pady=5)

        # History frame (kept visible)
        history_frame = tk.Frame(frame, bg="white")
        history_frame.grid(row=1, column=0, pady=5, sticky="w")

        return guess_var, submit_btn, input_frame, history_frame

    ############################### turn labels ###################################
    def create_turn_labels(self):
        """Create 'Your turn' labels above each player's name."""
        # Left player's turn label
        self.turn_label_left = tk.Label(self.left_frame, text="Your Turn!", font=("Segoe UI", 14, "bold"),
                                        bg="lightblue", fg="purple")
        self.turn_label_left.place(relx=0.5, rely=0.02, anchor="n")  # near top center

        # Right player's turn label
        self.turn_label_right = tk.Label(self.right_frame, text="Your Turn!", font=("Segoe UI", 14, "bold"),
                                         bg="lightcoral", fg="purple")
        self.turn_label_right.place(relx=0.5, rely=0.02, anchor="n")  # near top center

        # Start by showing left player's turn
        self.turn_label_left.lift()
        self.turn_label_right.place_forget()

    def show_turn(self, player_number):
        """Show the turn label for the given player number (1 or 2)."""
        if player_number == 1:
            self.turn_label_left.place(relx=0.5, rely=0.02, anchor="n")
            self.turn_label_right.place_forget()
        else:
            self.turn_label_right.place(relx=0.5, rely=0.02, anchor="n")
            self.turn_label_left.place_forget()

    ############################### turns ###################################
    def next_turn(self):
        """Show the current player's guess frame or end game"""
        # Hide only input frames, leave history visible
        self.input_frame1.grid_remove()
        self.input_frame2.grid_remove()

        if self.current_player == 1 and self.attempts1 <= self.total_attempts:
            self.input_frame1.grid()  # show input for player 1
            self.show_turn(1)
        elif self.current_player == 2 and self.attempts2 <= self.total_attempts:
            self.input_frame2.grid()  # show input for player 2
            self.show_turn(2)

    ############################### submit button setup ###################################
    def setup_submit_buttons(self):
        def submit1():
            val = self.guess_var1.get()
            # Clear previous error
            self.error_label1.config(text="")

            # Input validation
            if not val.isdigit():
                self.error_label1.config(text="Code must contain digits only.")
                return
            elif len(val) != self.encoding_length:
                self.error_label1.config(text=f"Code must be exactly {self.encoding_length} digits long.")
                return
            elif len(set(val)) != self.encoding_length:
                self.error_label1.config(text="All digits must be unique.")
                return

            # Compute bulls and cows
            guess = [int(ch) for ch in val]
            bulls = sum(guess[i] == self.secret2[i] for i in range(self.encoding_length))
            cows = sum(d in self.secret2 for d in guess) - bulls

            # Add guess to history
            tk.Label(self.history_frame1, text=f"{val}  →  Bulls: {bulls}, Cows: {cows}",
                     font=("Segoe UI", 12), bg="white").pack(anchor="w")

            self.guess_var1.set("")  # clear input

            # Check win
            if bulls == self.encoding_length:
                end_game(self.player1, self.player2, self.left_frame)

            # Check if player ran out of moves
            if self.attempts1 >= self.total_attempts:
                lose_label = tk.Label(self.left_frame,
                                      text=f"💀 {self.player1.name} ran out of moves! {self.player2.name} wins!",
                                      font=("Segoe UI", 16, "bold"), fg="red", bg=self.left_frame["bg"])
                lose_label.place(relx=0.5, rely=0.5, anchor="center")
                self.player1.losses += 1
                self.player2.wins += 1
                update_player_log(self.player1)
                update_player_log(self.player2)
                self.root.after(2000, show_final_screen)
                return

            # Next turn
            self.attempts1 += 1
            self.current_player = 2
            self.next_turn()

        def submit2():
            val = self.guess_var2.get()
            # Clear previous error
            self.error_label2.config(text="")

            # Input validation
            if not val.isdigit():
                self.error_label2.config(text="Code must contain digits only.")
                return
            elif len(val) != self.encoding_length:
                self.error_label2.config(text=f"Code must be exactly {self.encoding_length} digits long.")
                return
            elif len(set(val)) != self.encoding_length:
                self.error_label2.config(text="All digits must be unique.")
                return

            # Compute bulls and cows
            guess = [int(ch) for ch in val]
            bulls = sum(guess[i] == self.secret1[i] for i in range(self.encoding_length))
            cows = sum(d in self.secret1 for d in guess) - bulls

            # Add guess to history
            tk.Label(self.history_frame2, text=f"{val}  →  Bulls: {bulls}, Cows: {cows}",
                     font=("Segoe UI", 12), bg="white").pack(anchor="w")

            self.guess_var2.set("")  # clear input

            # Check win
            if bulls == self.encoding_length:
                end_game(self.player2, self.player1, self.right_frame)
                return

            # Check if player ran out of moves
            if self.attempts2 >= self.total_attempts:
                lose_label = tk.Label(self.right_frame,
                                      text=f"💀 {self.player2.name} ran out of moves! {self.player1.name} wins!",
                                      font=("Segoe UI", 16, "bold"), fg="red", bg=self.right_frame["bg"])
                lose_label.place(relx=0.5, rely=0.5, anchor="center")
                self.player2.losses += 1
                self.player1.wins += 1
                update_player_log(self.player1)
                update_player_log(self.player2)
                self.root.after(2000, show_final_screen)
                return

            # Next turn
            self.attempts2 += 1
            self.current_player = 1
            self.next_turn()

        def end_game(winner, loser, winner_frame):
            winner.wins += 1
            loser.losses += 1
            update_player_log(winner)
            update_player_log(loser)
            win_label = tk.Label(winner_frame, text=f"🎉 {winner.name} wins! 🎉",
                                 font=("Segoe UI", 16, "bold"), fg="green", bg=winner_frame["bg"])
            win_label.place(relx=0.5, rely=0.5, anchor="center")
            self.root.after(2000, show_final_screen)

        def show_final_screen():
            clear_root(self.root)
            show_leaderboard(self.root)

        # Attach commands
        self.submit_btn1.config(command=submit1)
        self.submit_btn2.config(command=submit2)

        # Create error labels for each player (if not already)
        if not hasattr(self, "error_label1"):
            self.error_label1 = tk.Label(self.input_frame1, text="", font=("Segoe UI", 12), fg="red", bg="white")
            self.error_label1.grid(row=4, column=0, columnspan=3)
        if not hasattr(self, "error_label2"):
            self.error_label2 = tk.Label(self.input_frame2, text="", font=("Segoe UI", 12), fg="red", bg="white")
            self.error_label2.grid(row=4, column=0, columnspan=3)
