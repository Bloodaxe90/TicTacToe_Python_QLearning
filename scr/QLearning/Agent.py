import pickle

import numpy as np

from scr.Main.GameRules import GameRules


class Agent:

    def __init__(self, q_learning, player: str, gamma: float= 0.9, max_alpha: float= 0.3, min_alpha: float= 0.05, max_epsilon: float = 1, min_epsilon:float = 0.01, lambda_: float= 0.7):
        self.Q_LEARNING = q_learning

        self.PLAYER: str = player

        self.GAMMA: float = gamma #Discount Factor

        self.MAX_ALPHA: float = max_alpha
        self.MIN_ALPHA: float = min_alpha
        self.alpha: float = max_alpha #Learning Rate

        self.LAMBDA: float = lambda_

        self.MAX_EPSILON: float = max_epsilon
        self.MIN_EPSILON: float = min_epsilon
        self.epsilon = max_epsilon #Exploration Rate

        self.q_table: dict[str:float] = {}
        self.eligibility_trace: dict[str:float] = {}


    def update_q_value(self, current_state: np.array, action: tuple[int, int], player: str, reward: float, next_state: np.array) -> None:
        current_state_action_pair: str =  self.get_state_action_as_key(current_state, action, player)

        self.update_eligibility_trace(current_state_action_pair)

        for state_action_pair in self.eligibility_trace:
            old_q_value: float = self.get_q_value(state_action_pair)
            max_next_q_value: float = self.get_max_next_q_value(next_state, player)
            td_error: float = (reward + (self.GAMMA * max_next_q_value)) - old_q_value
            new_q_value: float = old_q_value + (self.alpha * (td_error * self.eligibility_trace[state_action_pair]))
            self.q_table[state_action_pair] = new_q_value

            self.decay_eligibility_trace(state_action_pair)


    def update_eligibility_trace(self, state_action_pair: str) -> None:
        if state_action_pair not in self.eligibility_trace:
            self.eligibility_trace[state_action_pair] = 0.0
        self.eligibility_trace[state_action_pair] += 1.0

    def decay_eligibility_trace(self, state_action_pair: str) -> None:
        self.eligibility_trace[state_action_pair] *= self.GAMMA * self.LAMBDA

    def decay_epsilon(self, episode, max_episodes, power: float= 2) -> None:

        #decay_rate = -math.log(self.MIN_EPSILON / self.MAX_EPSILON) / max_episodes
        # self.EPSILON = self.MIN_EPSILON + (self.MAX_EPSILON - self.MIN_EPSILON) * math.exp(-decay_rate * episode)
        fraction = episode/max_episodes
        self.epsilon = (self.MAX_EPSILON - self.MIN_EPSILON) * ((1 - fraction) ** power) + self.MIN_EPSILON



    def decay_alpha(self, episode, max_episodes, power: float= 1.5) -> None:
        fraction = episode / max_episodes
        self.alpha = (self.MAX_ALPHA - self.MIN_ALPHA) * ((1 - fraction) ** power) + self.MIN_ALPHA


    def get_reward(self, opponent_player: str, next_state: np.array) -> float:
        rewards = {
            self.PLAYER: 1,
            opponent_player: -1,
            "D": 0.5
        }
        return rewards.get(GameRules.check_terminal(next_state), 0.0)


    def get_action(self, state: np.array) -> tuple[int, int]:
        if np.random.rand() <= self.epsilon:
            return self.Q_LEARNING.get_random_action(state)
        else:
            return self.get_best_action(state)


    def get_best_action(self, current_state: np.array) -> tuple[int, int]:
        best_action: tuple[int, int] = (-1, -1)
        best_q_value: float = -float("inf")
        for action in self.Q_LEARNING.get_possible_actions(current_state):

            q_value: float = self.get_q_value(self.get_state_action_as_key(current_state, action, self.PLAYER))

            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action
        return best_action


    def get_max_next_q_value(self, next_state: np.array, player: str) -> float:
        return max(
            [self.get_q_value(self.get_state_action_as_key(next_state, action, player))
             for action in self.Q_LEARNING.get_possible_actions(next_state)]
            , default= 0)


    def get_q_value(self, state_action_pair: str) -> float:
        return self.q_table.get(state_action_pair, 0.0)

    def get_state_action_as_key(self, state: np.array, action: tuple[int, int], player: str) -> str:
        return f"{"".join(str(value) if value != "" else "_" for value in state.flat)}{action[0]}{action[1]}{player}"


    def serialise_q_table(self) -> None:
        serialised_q_table = pickle.dumps(self.q_table)
        with open(f"../Resources/Q-TABLE/q_table_{self.PLAYER}.pkl", "wb") as file:
            file.write(serialised_q_table)
            print(f"Q-Table serialised: {self.q_table}")


    def deserialize_q_table(self, target_policy: bool) -> None:
        policy_path = f"../Resources/Q-TABLE/q_table_{self.PLAYER}.pkl" if not target_policy else f"Resources/Q-TABLE/target_policy_{self.PLAYER}.pkl"
        with open(policy_path, "rb") as file:
            self.q_table = pickle.load(file)
            print(f"Q-Table deserialized: {self.q_table}")




