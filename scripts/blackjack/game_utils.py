import random

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# game result codes
PLAYER_WIN = 1
DRAW_GAME = 0
PLAYER_LOSE = -1


def draw_card():
    """Draw a random card (no suits) from an infinite deck of cards

    Returns
    -------
    str
    """
    return random.choice(CARDS)


def get_hand_value(hand, ace_equals_one=False):
    """Get the blackjack value of a hand

    Parameters
    ----------
    hand: list[str]
        A list of the string card identifiers
    ace_equals_one: bool, optional
        If true, then all Aces will be counted as ones

    Returns
    -------
    int
        The integer hand value (highest value is returned without going over 21 if an ace is present)
    """
    hand_value = 0
    has_ace = False
    for card in hand:
        try:
            card_value = int(card)
        except ValueError:
            if card == 'A':
                has_ace = True
                card_value = 1
            else:
                card_value = 10
        hand_value += card_value
    if has_ace and not ace_equals_one:
        alt_hand_value = hand_value + 10
        if alt_hand_value <= 21:
            return alt_hand_value
    return hand_value


def has_usable_ace(hand):
    """Checks if a hand contains a usable ace (one that can be counted as an 11 without busting)

    Parameters
    ----------
    hand: list[str]

    Returns
    -------
    bool
    """
    has_ace = any(card == 'A' for card in hand)
    hand_value = get_hand_value(hand, ace_equals_one=True)
    return has_ace and (hand_value + 10 <= 21)


def check_blackjack(hand):
    return get_hand_value(hand) == 21


def check_bust(hand):
    return get_hand_value(hand) > 21


def check_under_17(hand):
    return get_hand_value(hand) < 17


def print_result(game_result):
    if game_result == PLAYER_WIN:
        print('Congratulations, you won!')
    elif game_result == PLAYER_LOSE:
        print('Sorry, you lost!')
    elif game_result == DRAW_GAME:
        print('It looks like you tied!')
    print()


def get_all_states():
    states = []
    for player_hand_value in range(12, 21):
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
