import random
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HandCricketGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hand Cricket Game")
        master.geometry("600x600")
        self.overs = 5
        self.wickets = 2
        self.total_balls = self.overs * 6
        self.current_ball = 0
        self.user_score = 0
        self.user_scores_list = []
        self.computer_score = 0
        self.computer_scores_list = []
        self.target = None
        self.current_innings = 1
        self.user_batting_first = None
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_welcome_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def setup_welcome_screen(self):
        self.clear_frame()
        label = tk.Label(self.main_frame, text="Welcome to Hand Cricket!", font=("Helvetica", 20))
        label.pack(pady=20)
        start_button = tk.Button(self.main_frame, text="Start Game", font=("Helvetica", 16), command=self.setup_game_config)
        start_button.pack(pady=10)

    def setup_game_config(self):
        self.clear_frame()
        title_label = tk.Label(self.main_frame, text="Game Configuration", font=("Helvetica", 18))
        title_label.pack(pady=10)
        overs_label = tk.Label(self.main_frame, text="Select number of overs:", font=("Helvetica", 14))
        overs_label.pack(pady=5)
        self.overs_var = tk.IntVar(value=5)
        overs_options = [("5 Overs", 5), ("10 Overs", 10), ("20 Overs", 20), ("50 Overs", 50)]
        for text, val in overs_options:
            tk.Radiobutton(self.main_frame, text=text, variable=self.overs_var, value=val, font=("Helvetica", 12)).pack(anchor=tk.W)
        toss_label = tk.Label(self.main_frame, text="Choose your toss call:", font=("Helvetica", 14))
        toss_label.pack(pady=10)
        toss_frame = tk.Frame(self.main_frame)
        toss_frame.pack(pady=5)
        heads_button = tk.Button(toss_frame, text="Heads", font=("Helvetica", 12), command=lambda: self.perform_toss(1))
        tails_button = tk.Button(toss_frame, text="Tails", font=("Helvetica", 12), command=lambda: self.perform_toss(2))
        heads_button.pack(side=tk.LEFT, padx=10)
        tails_button.pack(side=tk.LEFT, padx=10)

    def perform_toss(self, user_call):
        self.overs = self.overs_var.get()
        self.wickets = 2 if self.overs == 5 else (5 if self.overs == 10 else 10)
        self.total_balls = self.overs * 6
        self.current_ball = 0
        toss_result = random.randint(1, 2)
        self.clear_frame()
        if toss_result == user_call:
            toss_msg = "You won the toss!"
            self.user_won_toss = True
        else:
            toss_msg = "You lost the toss!"
            self.user_won_toss = False
        label = tk.Label(self.main_frame, text=toss_msg, font=("Helvetica", 16))
        label.pack(pady=10)
        if self.user_won_toss:
            choice_label = tk.Label(self.main_frame, text="Choose: Batting or Bowling", font=("Helvetica", 14))
            choice_label.pack(pady=5)
            batting_button = tk.Button(self.main_frame, text="Batting", font=("Helvetica", 12), command=lambda: self.start_innings(user_batting=True))
            bowling_button = tk.Button(self.main_frame, text="Bowling", font=("Helvetica", 12), command=lambda: self.start_innings(user_batting=False))
            batting_button.pack(pady=5)
            bowling_button.pack(pady=5)
        else:
            comp_choice = random.choice(["bat", "bowl"])
            info = tk.Label(self.main_frame, font=("Helvetica", 14))
            info.pack(pady=5)
            if comp_choice == "bat":
                info.config(text="Computer chose to bat first.")
                self.user_batting_first = False
                btn = tk.Button(self.main_frame, text="Start Bowling (Opponent Batting)", font=("Helvetica", 12), command=lambda: self.start_innings(user_batting=False))
            else:
                info.config(text="Computer chose to bowl first.")
                self.user_batting_first = True
                btn = tk.Button(self.main_frame, text="Start Batting", font=("Helvetica", 12), command=lambda: self.start_innings(user_batting=True))
            btn.pack(pady=10)

    def start_innings(self, user_batting):
        self.current_innings = 1
        self.user_score = 0
        self.computer_score = 0
        self.user_scores_list = []
        self.computer_scores_list = []
        self.current_ball = 0
        self.target = None
        self.user_batting_first = user_batting
        if user_batting:
            self.setup_batting_screen()
        else:
            self.setup_bowling_screen()

    def setup_batting_screen(self):
        self.clear_frame()
        inning_label = tk.Label(self.main_frame, text="Batting Innings", font=("Helvetica", 16))
        inning_label.pack(pady=10)
        self.score_label = tk.Label(self.main_frame, text=f"Score: {self.user_score} | Wickets left: {self.wickets}", font=("Helvetica", 14))
        self.score_label.pack(pady=5)
        self.ball_label = tk.Label(self.main_frame, text=f"Over: {self.current_ball//6}.{(self.current_ball%6)+1} / {self.overs}.0", font=("Helvetica", 14))
        self.ball_label.pack(pady=5)
        self.message_label = tk.Label(self.main_frame, text="", font=("Helvetica", 12))
        self.message_label.pack(pady=5)
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        for i in range(7):
            btn = tk.Button(button_frame, text=str(i), font=("Helvetica", 12), width=4, command=lambda run=i: self.handle_batting_choice(run))
            btn.grid(row=0, column=i, padx=5, pady=5)

    def handle_batting_choice(self, run):
        if self.current_ball >= self.total_balls or self.wickets <= 0:
            return
        weights = [0.3] + [0.7 / 6] * 6
        comp_run = random.choices(range(7), weights=weights)[0]
        self.current_ball += 1
        if run == comp_run:
            self.wickets -= 1
            self.user_scores_list.append(-1)
            self.message_label.config(text=f"Wicket! You chose {run} and computer chose {comp_run}.")
        else:
            self.user_score += run
            self.user_scores_list.append(run)
            self.message_label.config(text=f"You scored {run} runs. (Computer: {comp_run})")
        self.score_label.config(text=f"Score: {self.user_score} | Wickets left: {self.wickets}")
        self.ball_label.config(text=f"Over: {self.current_ball//6}.{(self.current_ball%6)+1} / {self.overs}.0")
        if self.target and self.current_innings == 2 and self.user_score >= self.target:
            self.message_label.config(text="You reached the target!")
            self.end_innings()
        elif self.current_ball >= self.total_balls or self.wickets == 0:
            self.end_innings()

    def setup_bowling_screen(self):
        self.clear_frame()
        inning_label = tk.Label(self.main_frame, text="Bowling Innings", font=("Helvetica", 16))
        inning_label.pack(pady=10)
        self.score_label = tk.Label(self.main_frame, text=f"Computer Score: {self.computer_score} | Wickets left: {self.wickets}", font=("Helvetica", 14))
        self.score_label.pack(pady=5)
        self.ball_label = tk.Label(self.main_frame, text=f"Over: {self.current_ball//6}.{(self.current_ball%6)+1} / {self.overs}.0", font=("Helvetica", 14))
        self.ball_label.pack(pady=5)
        self.message_label = tk.Label(self.main_frame, text="", font=("Helvetica", 12))
        self.message_label.pack(pady=5)
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        for i in range(7):
            btn = tk.Button(button_frame, text=str(i), font=("Helvetica", 12), width=4, command=lambda run=i: self.handle_bowling_choice(run))
            btn.grid(row=0, column=i, padx=5, pady=5)

    def handle_bowling_choice(self, bowl):
        if self.current_ball >= self.total_balls or self.wickets <= 0:
            return
        comp_run = random.choices(range(7), weights=[0.3] + [0.7 / 6] * 6)[0]
        self.current_ball += 1
        if bowl == comp_run:
            self.wickets -= 1
            self.computer_scores_list.append(-1)
            self.message_label.config(text=f"Wicket! You bowled {bowl}, computer played {comp_run}.")
        else:
            self.computer_score += comp_run
            self.computer_scores_list.append(comp_run)
            self.message_label.config(text=f"Computer scored {comp_run}. (You bowled {bowl})")
        self.score_label.config(text=f"Computer Score: {self.computer_score} | Wickets left: {self.wickets}")
        self.ball_label.config(text=f"Over: {self.current_ball//6}.{(self.current_ball%6)+1} / {self.overs}.0")
        if self.target and self.current_innings == 2 and self.computer_score >= self.target:
            self.message_label.config(text="Computer reached the target!")
            self.end_innings()
        elif self.current_ball >= self.total_balls or self.wickets == 0:
            self.end_innings()

    def end_innings(self):
        if self.current_innings == 1:
            self.target = (self.user_score if self.user_batting_first else self.computer_score) + 1
            next_msg = f"{'Computer' if self.user_batting_first else 'You'} need {self.target} to win."
            self.current_innings = 2
            self.wickets = 2 if self.overs == 5 else (5 if self.overs == 10 else 10)
            self.current_ball = 0
            if self.user_batting_first:
                self.computer_score = 0
                self.computer_scores_list = []
            else:
                self.user_score = 0
                self.user_scores_list = []
            self.clear_frame()
            label = tk.Label(self.main_frame, text=next_msg, font=("Helvetica", 14))
            label.pack(pady=10)
            next_btn = tk.Button(self.main_frame, text="Continue", font=("Helvetica", 12),
                                 command=self.setup_bowling_screen if self.user_batting_first else self.setup_batting_screen)
            next_btn.pack(pady=10)
        else:
            self.show_result()

    def show_result(self):
        self.clear_frame()
        result_text = "You won the match!" if (
            (self.user_batting_first and self.user_score > self.computer_score) or
            (not self.user_batting_first and self.user_score >= self.target)
        ) else "Computer won the match!"
        tk.Label(self.main_frame, text=result_text, font=("Helvetica", 18)).pack(pady=10)
        tk.Label(self.main_frame, text=f"Your Score: {self.user_score}\nComputer Score: {self.computer_score}", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.main_frame, text="Show Match Graph", font=("Helvetica", 12), command=self.show_graph).pack(pady=5)
        tk.Button(self.main_frame, text="Play Again", font=("Helvetica", 12), command=self.setup_game_config).pack(pady=5)
        tk.Button(self.main_frame, text="Quit", font=("Helvetica", 12), command=self.master.quit).pack(pady=5)

    def compute_cumulative(self, scores_list):
        cumulatives = []
        total = 0
        for s in scores_list:
            if s == -1:
                cumulatives.append(total)
            else:
                total += s
                cumulatives.append(total)
        return cumulatives

    def show_graph(self):
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Match Graph")
        user_cumulative = self.compute_cumulative(self.user_scores_list)
        computer_cumulative = self.compute_cumulative(self.computer_scores_list)
        fig, ax = plt.subplots(figsize=(6, 4))

        def plot_innings(cumulative, label, color, original_scores):
            balls = list(range(1, len(cumulative) + 1))
            ax.plot(balls, cumulative, color=color, label=label)
            for i, val in enumerate(cumulative):
                if original_scores[i] == -1:
                    ax.plot(balls[i], val, marker='o', color=color)

        if user_cumulative:
            plot_innings(user_cumulative, "Your Cumulative Score", 'blue', self.user_scores_list)
        if computer_cumulative:
            plot_innings(computer_cumulative, "Computer Cumulative Score", 'red', self.computer_scores_list)

        ax.set_xlabel("Balls")
        ax.set_ylabel("Cumulative Runs")
        ax.set_title("Cumulative Score per Ball")
        ax.legend()
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == '__main__':
    root = tk.Tk()
    game = HandCricketGUI(root)
    root.mainloop()
