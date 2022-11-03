from functions import *

Deck = List[int]


def play_normal_round(p1_deck_: Deck, p2_deck_: Deck) -> bool:
    """ Returns true if Plater 1 wins. """
    p1_wins = (p1_deck_[0] > p2_deck_[0])
    update_decks(p1_deck_, p2_deck_, p1_wins)
    return p1_wins


def update_decks(p1_deck_: Deck, p2_deck_: Deck, p1_wins_: bool) -> None:
    if p1_wins_:
        p1_deck_.append(p1_deck_[0])
        p1_deck_.append(p2_deck_[0])
    else:
        p2_deck_.append(p2_deck_[0])
        p2_deck_.append(p1_deck_[0])
    del p1_deck_[0]
    del p2_deck_[0]


def recursive_combat(p1_deck_: Deck, p2_deck_: Deck, past_hands_: Set[Tuple[Tuple[int], Tuple[int]]]) -> bool:
    """ Returns true if Plater 1 wins. """
    while p1_deck_ != [] and p2_deck_ != []:
        this_hand = (tuple(p1_deck_), tuple(p2_deck_))
        if this_hand in past_hands_:
            return True
        else:
            past_hands_.add(this_hand)
            if len(p1_deck_) > p1_deck_[0] and len(p2_deck_) > p2_deck_[0]:
                new_p1_deck = p1_deck_.copy()[1:p1_deck_[0] + 1]
                new_p2_deck = p2_deck_.copy()[1:p2_deck_[0] + 1]
                winner_is_p1 = recursive_combat(new_p1_deck, new_p2_deck, set())
                update_decks(p1_deck_, p2_deck_, winner_is_p1)
            else:
                play_normal_round(p1_deck_, p2_deck_)
    return p1_deck_ != []


def compute_score(p1_deck_: Deck, p2_deck_: Deck) -> int:
    winner = (p1_deck_ if p1_deck_ != [] else p2_deck_)
    return sum([(len(winner) - i) * winner[i] for i in range(len(winner))])


def main():
    logging.basicConfig(level=logging.DEBUG)
    data = read_file("data/22.in")

    p1 = []
    p2 = []
    for line in data:
        if "Player 1" in line:
            deck = p1
        elif "Player 2" in line:
            deck = p2
        elif line == "":
            continue
        else:
            deck.append(int(line))
    logging.debug(f"\tPlayer 1's deck is: {p1}\n\t\t\tPlayer 2's deck is: {p2}")

    p1_1 = p1.copy()
    p2_1 = p2.copy()
    while p1_1 != [] and p2_1 != []:
        play_normal_round(p1_1, p2_1)
    logging.info(f"The score of the winning player is {compute_score(p1_1, p2_1)}")

    p1_2 = p1.copy()
    p2_2 = p2.copy()
    recursive_combat(p1_2, p2_2, set())
    logging.info(f"The score of the winning player is {compute_score(p1_2, p2_2)}")


start_time = time.time_ns()
main()
logging.info(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
