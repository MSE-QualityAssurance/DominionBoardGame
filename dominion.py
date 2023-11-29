import random

class Card:
    def __init__(self, name, cost, card_type, value=0):
        self.name = name
        self.cost = cost
        self.card_type = card_type
        self.value = value  # For Treasure cards

    def effect(self, player, game):
        # Example: Copper card adds coins
        if self.name == 'Copper':
            player.coins += 1


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.actions = 1
        self.buys = 1
        self.coins = 0

    def draw_hand(self):
        for _ in range(5):
            if self.deck:
                self.hand.append(self.deck.pop())
            else:
                self.shuffle_discard_into_deck()

    def shuffle_discard_into_deck(self):
        random.shuffle(self.discard_pile)
        self.deck.extend(self.discard_pile)
        self.discard_pile.clear()

    def play_action_card(self, card, game):
        # Check if the player has actions available
        if self.actions > 0:
            # Ensure the card is in the hand and is an action card
            if card in self.hand and card.card_type == 'Action':
                # Play the card
                card.effect(self, game)

                # Move the card from hand to discard pile
                self.hand.remove(card)
                self.discard_pile.append(card)

                # Decrease the number of available actions
                self.actions -= 1
            else:
                print("Cannot play this card")
        else:
            print("No more actions left")

    def play_treasure_cards(self):
        for card in self.hand[:]:  # Iterate over a copy of the hand
            if card.card_type == 'Treasure':
                # Play the card
                card.effect(self, None)  # Assuming the game object is not needed for treasures

                # Move the card from hand to discard pile
                self.hand.remove(card)
                self.discard_pile.append(card)

    def buy_card(self, card, game):
        # Check if the card is available in the supply and if the player has enough coins and buys
        if game.supply.get(card.name, 0) > 0 and self.coins >= card.cost and self.buys > 0:
            # Deduct the cost of the card from the player's coins
            self.coins -= card.cost

            # Decrease the number of buys
            self.buys -= 1

            # Move the card from the supply to the player's discard pile
            self.discard_pile.append(card)

            # Decrease the card count in the supply
            game.supply[card.name] -= 1
        else:
            print("Cannot buy this card")

    def end_turn(self):
        # Move all cards from hand to discard pile
        self.discard_pile.extend(self.hand)
        self.hand.clear()

        # Reset the player's actions, buys, and coins
        self.actions = 1
        self.buys = 1
        self.coins = 0

        # Draw a new hand for the next turn
        self.draw_hand()


class DominionGame:
    def __init__(self, players):
        self.players = players
        self.supply = {}
        self.trash = []

    def setup_game(self):
        # Initialize Supply
        self.init_supply()

        # Setup Players
        for player in self.players:
            self.setup_player_deck(player)
            player.draw_hand()

    def init_supply(self):
        # Add basic cards to the supply
        self.supply["Copper"] = [Card("Copper", 0, "Treasure", 1) for _ in range(60)]
        self.supply["Silver"] = [Card("Silver", 3, "Treasure", 2) for _ in range(40)]
        self.supply["Gold"] = [Card("Gold", 6, "Treasure", 3) for _ in range(30)]

        self.supply["Estate"] = [Card("Estate", 2, "Victory", 1) for _ in range(24)]
        self.supply["Duchy"] = [Card("Duchy", 5, "Victory", 3) for _ in range(12)]
        self.supply["Province"] = [Card("Province", 8, "Victory", 6) for _ in range(12)]

        # Add a few basic Kingdom cards
        # Example: Smithy - Costs 4, no immediate value, action effect to be defined
        self.supply["Smithy"] = [Card("Smithy", 4, "Action") for _ in range(10)]

        # Additional Kingdom cards can be added here

    def setup_player_deck(self, player):
        # Each player starts with 7 Coppers and 3 Estates
        player.deck = [Card("Copper", 0, "Treasure", 1) for _ in range(7)] + \
                      [Card("Estate", 2, "Victory", 1) for _ in range(3)]
        random.shuffle(player.deck)

    def play_round(self):
        for player in self.players:
            player.draw_hand()
            self.play_turn(player)
            player.end_turn()

    def play_turn(self, player):
        # Action Phase
        self.action_phase(player)

        # Buy Phase
        self.buy_phase(player)

        # Cleanup Phase
        self.cleanup_phase(player)

    def action_phase(self, player):
        # Players can play any number of Action cards (subject to available actions)
        for card in player.hand:
            if card.card_type == "Action" and player.actions > 0:
                player.play_action_card(card)
                player.actions -= 1

    def buy_phase(self, player):
        # Play all Treasure cards in hand
        player.play_treasure_cards()

        # Player can buy cards from the supply (subject to available buys and coins)
        for _ in range(player.buys):
            # Implement logic to choose and buy a card
            # Example: if player.coins >= cost_of_card and card in supply:
            #             player.buy_card(card)
            pass

    def cleanup_phase(self, player):
        # Discard hand and draw new hand
        player.discard_pile.extend(player.hand)
        player.hand = []
        player.draw_hand()

        # Reset actions, buys, and coins for the next turn
        player.actions = 1
        player.buys = 1
        player.coins = 0

    def play_game(self):
        pass

    def check_game_end(self):
        # Check if the Province pile is empty
        if not self.supply["Province"]:
            return True

        # Check if any three supply piles are empty
        empty_piles = sum(1 for pile in self.supply.values() if not pile)
        if empty_piles >= 3:
            return True

        return False

    def calculate_scores(self):
        player_scores = {}
        for player in self.players:
            score = 0
            all_cards = player.deck + player.discard_pile + player.hand
            for card in all_cards:
                if card.card_type == "Victory":
                    score += card.value
            player_scores[player.name] = score

        return player_scores

def main():
    players = [Player("Alice"), Player("Bob")]
    game = DominionGame(players)
    game.setup_game()
    while not game.check_game_end():
        game.play_round()
    game.calculate_scores()

if __name__ == "__main__":
    main()
