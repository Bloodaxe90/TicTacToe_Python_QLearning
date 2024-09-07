from collections import Counter

import numpy as np
from PySide6.QtWidgets import QPushButton

from scr.QLearning.Agent import Agent
from scr.Main.GameRules import GameRules
from scr.QLearning.TrainingLog import TrainingLog
from scr.Main.TicTacToe import TicTacToe


class QLearning(TicTacToe):
    def __init__(self, game_controller, max_episodes: int = 100000) -> None:
        super().__init__(game_controller)
        self.p1_agent_log = TrainingLog()

        self.MAX_EPISODES: int = max_episodes

        self.P1_AGENT: Agent = Agent(self, self.P1)
        self.P2_AGENT: Agent = Agent(self, self.P2)

        self.current_agent: Agent = self.P1_AGENT

    def play(self, b: QPushButton) -> None:
        b.setText(self.P1_AGENT.PLAYER)
        self.board = self.GAME_CONTROLLER.get_string_actual_board()
        if not self.check_game_over():
            best_action: tuple[int, int] = self.P2_AGENT.get_best_action(self.board)
            self.GAME_CONTROLLER.actual_board[best_action].setText(self.P2_AGENT.PLAYER)
            self.board = self.GAME_CONTROLLER.get_string_actual_board()
            self.check_game_over()


    def train(self) -> None:
        print("TRAINING HAS BEGUN")
        terminal_tracker: list[str] = []

        for episode in range(1, self.MAX_EPISODES +1):

            #Resetting board for next episode
            starting_agent = self.current_agent
            self.board = np.empty((3, 3), dtype=str)
            self.P1_AGENT.eligibility_trace = {}
            self.P2_AGENT.eligibility_trace = {}

            while GameRules.check_terminal(self.board) == "":

                #Choosing action based on the current player
                current_state = self.board.copy()
                action: tuple[int, int] = self.current_agent.get_action(current_state)

                #Playing the chosen action and making the environment represent the next state
                self.board[action] = self.current_agent.PLAYER

                next_state = self.board.copy()

                current_player_reward: float = self.current_agent.get_reward(self.get_opponent_agent().PLAYER, next_state)
                opponent_reward: float = self.get_opponent_agent().get_reward(self.current_agent.PLAYER, next_state)

                # Updating Q-value
                self.current_agent.update_q_value(current_state, action, self.current_agent.PLAYER,
                                                  current_player_reward, next_state)
                self.get_opponent_agent().update_q_value(current_state, action, self.current_agent.PLAYER,
                                                         opponent_reward, next_state)

                # Changing agent
                self.current_agent = self.get_opponent_agent()

            #Ensuring other agent starts
            if self.current_agent == starting_agent:
                self.current_agent = self.get_opponent_agent()

            #Decay Exploration Rate
            self.P1_AGENT.decay_epsilon(episode, self.MAX_EPISODES)
            self.P2_AGENT.decay_epsilon(episode, self.MAX_EPISODES)

            # Decay Learning Rate
            self.P1_AGENT.decay_alpha(episode, self.MAX_EPISODES)
            self.P2_AGENT.decay_alpha(episode, self.MAX_EPISODES)

            # Debugging
            terminal_tracker.append(GameRules.check_terminal(self.board))
            if episode % 1000 == 0 and episode != 0:
                self.add_diagnostics_data(episode, terminal_tracker)
                terminal_tracker = []

        self.p1_agent_log.save(f"/Users/eric/PycharmProjects/TicTacToe/Resources/TrainingLogs/{self.P1_AGENT.PLAYER}_log.csv")
        print("TRAINING HAS FINISHED")


    def get_opponent_agent(self) -> Agent:
        return self.P1_AGENT if self.current_agent == self.P2_AGENT else self.P2_AGENT

    def save_policies(self) -> None:
        self.P1_AGENT.serialise_q_table()
        self.P2_AGENT.serialise_q_table()

    def load_policies(self, target_policy: bool =False) -> None:
        self.P1_AGENT.deserialize_q_table(target_policy)
        self.P2_AGENT.deserialize_q_table(target_policy)

    def add_diagnostics_data(self, episode: int, terminal_tracker: list[str]) -> None:
        counts = Counter(terminal_tracker)
        self.p1_agent_log.add_data(episode, counts.get(self.P1_AGENT.PLAYER, 0), counts.get(self.P2_AGENT.PLAYER, 0), counts.get("D", 0), self.P1_AGENT.epsilon, self.P1_AGENT.alpha, len(self.P1_AGENT.q_table))

        print(f"{episode} episodes complete "
              f"| {self.P1_AGENT.PLAYER} Wins:{counts.get(self.P1_AGENT.PLAYER, 0)} "
              f"| {self.P2_AGENT.PLAYER} Wins:{counts.get(self.P2_AGENT.PLAYER, 0)} "
              f"| Draws:{counts.get("D", 0)} "
              f"| Exploration rate: {self.P1_AGENT.epsilon} "
              f"| Learning rate: {self.P1_AGENT.alpha} "
              f"| Q-Table Size: {len(self.P1_AGENT.q_table)}")

    def reset_q_tables(self) -> None:
        self.P1_AGENT.q_table = {}
        self.P2_AGENT.q_table = {}



