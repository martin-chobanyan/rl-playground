# valid states
# player: 12, 13, ... 20
# dealer: 2, 3, ... 11
# usable: True, False


def get_all_states():
    states = []
    # the player should always hit with a value 11 or less
    # thus a policy onl needs to be defined for states 12, 13, ... 20
    for player_hand_value in range(3, 21):
        # the value of the dealer's visible card (ace is treated as an eleven)
        for dealer_card_value in range(2, 12):
            # the third element is whether or not the player has a usable ace
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
