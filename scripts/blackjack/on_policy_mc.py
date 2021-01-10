from blackjack_game import BlackjackGame
from game_utils import get_all_states


class BlackjackPolicy:
    def __init__(self):
        self.states = get_all_states()
        self.state_to_action = {s: False for s in self.states}

    def __call__(self, state):
        player_hand_value, *_ = state
        if player_hand_value < 12:
            return True
        elif player_hand_value == 21:
            return False
        else:
            return self.state_to_action[state]


def on_policy_monte_carlo(n_episodes, eps=0.1):
    # initiate the game and policy
    game = BlackjackGame()
    policy = BlackjackPolicy()

    # get the game history (sequence of states, actions, and rewards taken)
    game_result, (states, actions, rewards) = game.play(policy)



    return


if __name__ == '__main__':
    states = get_all_states()
    policy_fn = BlackjackPolicy()
    for state in states:
        print(state)
        print(policy_fn(state))
        print()
