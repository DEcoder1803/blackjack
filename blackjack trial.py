import random

class Card:
    def __init__(self, face, value, symbol):
        self.face = face
        self.value = value
        self.symbol = symbol

def display_cards(cards, hidden):
    def get_top_line(cards):
        return '\t ________________' * len(cards)

    def get_blank_line(cards, hidden):
        line = '\t|                |' * len(cards)
        if hidden:
            line += '\t|                |'
        return line

    def get_face_line(cards, hidden):
        line = ''.join(f'\t|  {card.face:<2}            |' if card.face in ['J', 'Q', 'K', 'A'] else f'\t|  {card.value:<2}            |' for card in cards)
        if hidden:
            line += '\t|                |'
        return line

    def get_hidden_lines(hidden):
        lines = [
            '\t|      * *       |',
            
            '\t|    *     *     |',
            
            '\t|   *       *    |',
            '\t|   *       *    |',
            '\t|          *     |',
            '\t|         *      |',
            '\t|        *       |',
            
            
        ]
        return lines if hidden else []

    def get_symbol_line(cards, hidden):
        line = ''.join(f'\t|       {card.symbol}        |' for card in cards)
        if hidden:
            line += '\t|          *     |'
        return line

    def get_bottom_face_line(cards, hidden):
        line = ''.join(f'\t|            {card.face:<2}   |' if card.face in ['J', 'Q', 'K', 'A'] else f'\t|           {card.value:<2}   |' for card in cards)
        if hidden:
            line += '\t|        *       |'
        return line

    def get_bottom_line(cards):
        return '\t|________________|' * len(cards)

    print(get_top_line(cards))
    print(get_blank_line(cards, hidden))
    print(get_face_line(cards, hidden))
    for _ in range(5):
        print(get_blank_line(cards, hidden))
    for hidden_line in get_hidden_lines(hidden):
        print(hidden_line)
    print(get_symbol_line(cards, hidden))
    print(get_blank_line(cards, hidden))
    print(get_bottom_face_line(cards, hidden))
    print(get_bottom_line(cards))
    print()

def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

def handle_ace_adjustment(hand, total):
    for card in hand:
        if total > 21 and card.value == 11:
            card.value = 1
            total -= 10
    return total

def play_blackjack(deck):
    player_hand, dealer_hand = [], []
    player_total, dealer_total = 0, 0

    # Initial dealing
    for _ in range(2):
        player_card = draw_card(deck)
        player_hand.append(player_card)
        player_total += player_card.value
        player_total = handle_ace_adjustment(player_hand, player_total)

        print('PLAYER CARDS:')
        display_cards(player_hand, False)
        print('PLAYER SCORE =', player_total)
        input('Continue...')

        dealer_card = draw_card(deck)
        dealer_hand.append(dealer_card)
        dealer_total += dealer_card.value
        dealer_total = handle_ace_adjustment(dealer_hand, dealer_total)

        print('DEALER CARDS:')
        if len(dealer_hand) == 1:
            display_cards(dealer_hand, False)
            print('DEALER SCORE =', dealer_total)
        else:
            display_cards(dealer_hand[:-1], True)
            print('DEALER SCORE =', dealer_total - dealer_hand[-1].value)
        input('Continue...')

    if player_total == 21:
        print('PLAYER HAS A BLACKJACK! PLAYER WINS!')
        return

    print('DEALER CARDS:')
    display_cards(dealer_hand[:-1], True)
    print('DEALER SCORE =', dealer_total - dealer_hand[-1].value)
    print('PLAYER CARDS:')
    display_cards(player_hand, False)
    print('PLAYER SCORE =', player_total)

    while player_total < 21:
        choice = input('Enter H to Hit or S to Stand: ').upper()
        if choice not in ['H', 'S']:
            print('Invalid choice! Try Again...')
            continue

        if choice == 'S':
            break
        else:
            player_card = draw_card(deck)
            player_hand.append(player_card)
            player_total += player_card.value
            player_total = handle_ace_adjustment(player_hand, player_total)

            print('DEALER CARDS:')
            display_cards(dealer_hand[:-1], True)
            print('DEALER SCORE =', dealer_total - dealer_hand[-1].value)
            print('PLAYER CARDS:')
            display_cards(player_hand, False)
            print('PLAYER SCORE =', player_total)

    print('PLAYER CARDS:')
    display_cards(player_hand, False)
    print('PLAYER SCORE =', player_total)
    print('DEALER IS REVEALING THEIR CARDS....')
    display_cards(dealer_hand, False)
    print('DEALER SCORE =', dealer_total)

    if player_total == 21:
        print('PLAYER HAS A BLACKJACK, PLAYER WINS!')
        return

    if player_total > 21:
        print('PLAYER BUSTED! GAME OVER!')
        return

    input('Continue...')
    while dealer_total < 17:
        print('DEALER DECIDES TO HIT...')
        dealer_card = draw_card(deck)
        dealer_hand.append(dealer_card)
        dealer_total += dealer_card.value
        dealer_total = handle_ace_adjustment(dealer_hand, dealer_total)

        print('PLAYER CARDS:')
        display_cards(player_hand, False)
        print('PLAYER SCORE =', player_total)
        print('DEALER CARDS:')
        display_cards(dealer_hand, False)
        print('DEALER SCORE =', dealer_total)
        if dealer_total > 21:
            break
        input('Continue...')

    if dealer_total > 21:
        print('DEALER BUSTED! YOU WIN!')
    elif dealer_total == 21:
        print('DEALER HAS A BLACKJACK! PLAYER LOSES!')
    elif dealer_total == player_total:
        print('TIE GAME!')
    elif player_total > dealer_total:
        print('PLAYER WINS!')
    else:
        print('DEALER WINS!')

def initialize_deck():
    suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
    suit_symbols = {'Hearts': '\u2661', 'Diamonds': '\u2662', 'Spades': '\u2664', 'Clubs': '\u2667'}
    card_values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
    return [Card(face, value, suit_symbols[suit]) for suit in suits for face, value in card_values.items()]

if __name__ == '__main__':
    deck = initialize_deck()
    play_blackjack(deck)
import praw
import enchant

def reddit_bot(subreddit_name, trigger_phrase):
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id='your_client_id',
        client_secret='your_client_secret',
        username='your_username',
        password='your_password',
        user_agent='your_user_agent'
    )

    # Choose the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Initialize the dictionary for suggesting similar words
    dictionary = enchant.Dict('en_US')

    # Stream comments from the subreddit
    for comment in subreddit.stream.comments():
        if trigger_phrase in comment.body.lower():
            # Extract the word after the trigger phrase
            word = comment.body.lower().replace(trigger_phrase, '').strip()
            similar_words = dictionary.suggest(word)
            reply_text = ' '.join(similar_words)
            
            # Reply to the comment with suggested words
            comment.reply(reply_text)

if __name__ == '__main__':
    reddit_bot(subreddit_name='Python', trigger_phrase='useful bot')


