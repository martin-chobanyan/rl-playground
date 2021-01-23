# valid states
# player: 12, 13, ... 20
# dealer: 2, 3, ... 11
# usable: True, False


def get_all_states():
    states = []
    for player_hand_value in range(3, 21):
        for dealer_card_value in range(2, 12):
            states.append((player_hand_value, dealer_card_value, False))
            states.append((player_hand_value, dealer_card_value, True))
    return states


def enumerate_states():
    states = get_all_states()
    return dict(zip(states, range(len(states))))


def display_game_history(states, actions, rewards):
    all_states = get_all_states()
    for s, a, r in zip(states, actions, rewards):
        player_hand, dealer_card, usable_ace = all_states[s]
        print(f'Player hand value: {player_hand}')
        print(f'Dealer card value: {dealer_card}')
        print(f'Usable ace: {usable_ace}')
        print(f'Hit: {a}')
        print(f'Reward: {r}')
        print()
