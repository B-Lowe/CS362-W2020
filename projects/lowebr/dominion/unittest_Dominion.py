import unittest
import Dominion
from collections import defaultdict

class TestAction_card(unittest.TestCase):
    def test_init(self):
        # Test a normal, planned initialization with appropriate data types in constructor
        TestCard = Dominion.Action_card("TestCard",1,2,3,4,5)

        self.assertEqual(TestCard.name, "TestCard")
        self.assertEqual(TestCard.cost, 1)
        self.assertEqual(TestCard.actions, 2)
        self.assertEqual(TestCard.cards, 3)
        self.assertEqual(TestCard.buys, 4)
        self.assertEqual(TestCard.coins, 5)

        # Test an initialization with characters in place of integers in constructor
        TestCard = Dominion.Action_card("TestCard",'a','b','c','d','e')
        self.assertEqual(TestCard.name, "TestCard")
        self.assertEqual(TestCard.cost, 'a')
        self.assertEqual(TestCard.actions, 'b')
        self.assertEqual(TestCard.cards, 'c')
        self.assertEqual(TestCard.buys, 'd')
        self.assertEqual(TestCard.coins, 'e')

        #Test that a TypeError is raised when nothing is passed to the constructor
        self.assertRaises(TypeError, Dominion.Action_card, 0)

        # Test a purposly incorrect initialization with inappropriate data types in constructor
        #self.assertRaises(TypeError, Dominion.Action_card, 2, 'a', 'b', 'c', 'd', 'e')
    
    def test_use(self):
        # Initialize a player
        TestPlayer = Dominion.Player("Test")

        # Initialize an action card
        TestCard = Dominion.Action_card("TestCard", 1, 2, 3, 4, 5)

        # Add TestCard to the TestPlayer hand
        TestPlayer.hand.append(TestCard)

        # Initialize a trash object
        trash = []

        # Run use function and check for expected outcomes
        TestCard.use(TestPlayer, trash)

        # Check that test card has been appended the played list
        self.assertEqual(TestPlayer.played[-1], TestCard)

        # Check that test card has been removed from the players hand
        self.assertFalse(TestCard in TestPlayer.hand)

    def test_augment(self):
        # Initialize a player
        TestPlayer = Dominion.Player("Test")

        # Initialize an action card
        TestCard = Dominion.Action_card("TestCard", 1, 2, 3, 4, 5)

        # Initialize player attributes that would normally be initialized in player.turn
        TestPlayer.actions=0
        TestPlayer.buys=0
        TestPlayer.purse=0

        # Run the augment function and check for expected outcomes
        TestCard.augment(TestPlayer)

        # Check that the TestCard actions have been added to the TestPlayer actions
        self.assertEqual(TestPlayer.actions, 2)

        # Check that the TestCard buys have been added to the TestPlayer buys
        self.assertEqual(TestPlayer.buys, 4)

        # Check that the TestCard coins have been added to the TestPlayer purse
        self.assertEqual(TestPlayer.purse, 5)

class TestPlayer_Class(unittest.TestCase):
    def test_action_balance(self):
        # Initialize a TestPlayer
        TestPlayer = Dominion.Player("Test")

        # Check that action_balance is 0 since no action cards are in the stack
        self.assertEqual(TestPlayer.action_balance(), 0)

        # Initialize an action card into the players hand
        TestCard = Dominion.Action_card("Test", 1, 2, 3, 4, 5)
        TestPlayer.hand.append(TestCard)

        # Check that the action_balance is 70/11 since 1 action card is present in the stack
        self.assertEqual(TestPlayer.action_balance(), 70/11)

    def test_calcpoints(self):
        # Initialize a test player
        TestPlayer = Dominion.Player("Test")

        # Assert that on initialization, calcpoints is equal to three, as three estates are present at init
        self.assertEqual(TestPlayer.calcpoints(), 3)

        # Add an Estate card to assert that calcpoints returns four
        TestPlayer.hand.append(Dominion.Estate())
        self.assertEqual(TestPlayer.calcpoints(), 4)

        # Add a Duchy card to assert that calcpoints increases by 3
        TestPlayer.deck.append(Dominion.Duchy())
        self.assertEqual(TestPlayer.calcpoints(), 7)
        
        # Add a Province card to assert that calcpoints increases by 6
        TestPlayer.deck.append(Dominion.Province())
        self.assertEqual(TestPlayer.calcpoints(), 13)

        # Add a curse card to assert that calcpoints decreases by 1
        TestPlayer.deck.append(Dominion.Curse())
        self.assertEqual(TestPlayer.calcpoints(), 12)

        # Add a garden card to assert that calcpoints increases by 1
        TestPlayer.deck.append(Dominion.Gardens())
        self.assertEqual(TestPlayer.calcpoints(), 13)

        # Set TestPlayer to less than 10 cards in the stack, and assert that garden card does not add a victory point
        TestPlayer.hand = []
        TestPlayer.deck = []
        TestPlayer.deck.append(Dominion.Gardens())
        self.assertEqual(TestPlayer.calcpoints(), 0)
    
    def test_draw(self):
        # Initialize a test player
        TestPlayer = Dominion.Player("Test")

        # Check that if the deck is zero, the discard pile is put back into the deck
        # Initialize the deck and hand to be empty
        TestPlayer.deck = []
        TestPlayer.hand = []

        # Initialize the discard pile
        TestCard = Dominion.Estate()
        TestPlayer.discard = [TestCard]

        # Assert that the hand now contains the Estate card
        TestPlayer.draw()
        self.assertEqual(TestPlayer.hand, [TestCard])

        # Check that if the deck is nonzero, the first object in the deck will be put into the hand
        # Initialize the hand to be empty
        TestPlayer.hand = []

        # Initialize the deck
        TestPlayer.deck = [TestCard]

        # Assert that the hand now contains the Estate card
        TestPlayer.draw()
        self.assertEqual(TestPlayer.hand, [TestCard])

        #Check that if we set dest to be something other than hand, the code still functions properly
        # Initialize the deck
        TestPlayer.deck = [TestCard]
        
        # Initialize the discard pile
        TestPlayer.discard = []

        # Set dest to discard and assert that discard contains the Estate card
        TestPlayer.draw(TestPlayer.discard)
        self.assertEqual(TestPlayer.discard, [TestCard])
    
    def test_cardsummary(self):
        # Initialize a test player
        TestPlayer = Dominion.Player("Test")

        # Assert that cardsummary returns a list of 7 copper and 3 estate and 3 victory points
        self.assertEqual(TestPlayer.cardsummary(), {"Copper": 7, "Estate": 3, "VICTORY POINTS": 3})

        # Check that when a copper is added, the copper shows 8 eight cards showing
        TestPlayer.deck.append(Dominion.Copper())
        self.assertEqual(TestPlayer.cardsummary(), {"Copper": 8, "Estate": 3, "VICTORY POINTS": 3})

        # Check that when a Duchy is added, it is now displayed and the victory points go up by 3
        TestPlayer.deck.append(Dominion.Duchy())
        self.assertEqual(TestPlayer.cardsummary(), {"Copper": 8, "Estate": 3, "Duchy": 1, "VICTORY POINTS": 6})

class TestGameover(unittest.TestCase):
    def test_gameover(self):
        # Initialize a Province supply and set it to be empty and assert that gamover returns true
        supply=defaultdict(list)
        supply["Province"]=[]
        self.assertEqual(Dominion.gameover(supply), True)

        # Initialize the province supply to be non-empty and assert that gameover returns false
        supply["Province"]=[Dominion.Province()]
        self.assertEqual(Dominion.gameover(supply), False)

        # Set three stacks to be empty and assert that gameover returns true
        supply["Copper"]=[]
        supply["Estate"]=[]
        supply["Silver"]=[]
        self.assertEqual(Dominion.gameover(supply), True)

if __name__ == '__main__':
    unittest.main()