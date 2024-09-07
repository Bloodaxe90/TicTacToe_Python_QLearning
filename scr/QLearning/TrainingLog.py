import pandas as pd


class TrainingLog:
    def __init__(self) -> None:
        self.log = pd.DataFrame(columns=["EPISODE", "WINS", "LOSSES", "DRAWS", "EXPLORATION RATE", "LEARNING RATE", "Q-TABLE SIZE"])


    def add_data(self, episode: int, wins: int, losses: int, draws: int, exploration_rate: float,
                  learning_rate, q_table_size: int) -> None:
        new_data = pd.DataFrame([{
            "EPISODE": episode,
            "WINS": wins,
            "LOSSES": losses,
            "DRAWS": draws,
            "EXPLORATION RATE": exploration_rate,
            "LEARNING RATE": learning_rate,
            "Q-TABLE SIZE": q_table_size
        }]).dropna(axis=1, how='all')

        self.log = pd.concat([self.log, new_data], ignore_index=True)


    def save(self, path: str) -> None:
        self.log.to_csv(path, index=False)
