def get_all_states():
    states = []
    # the player should always hit with a value 11 or less
    # thus a policy onl needs to be defined for states 12, 13, ... 20
    for player_hand_value in range(12, 21):
        # the value of the dealer's visible card (ace is treated as one)
        for dealer_card_value in range(1, 11):
            # the third element is whether or not the player has a usable ace
            states.append((player_hand_value, dealer_card_value, True))
            states.append((player_hand_value, dealer_card_value, False))
    return states


def display_game_history(states, actions, rewards):
    for s, a, r in zip(states, actions, rewards):
        print(f'Player hand value: {s[0]}')
        print(f'Dealer card value: {s[1]}')
        print(f'Usable ace: {s[2]}')
        print(f'Hit: {a}')
        print(f'Reward: {r}')
        print()
