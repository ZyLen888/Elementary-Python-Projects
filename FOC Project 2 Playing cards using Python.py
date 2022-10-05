def comp10001huxxy_score(cards):
    '''This function calculates the score the cards in player's hand.
    
    Arguments: A list 
           a list of cards held by a player, each in the format of a 2-letter 
           string
    Return: Integer
            A non-negative integer indicating the score for the combined cards
    '''
    # To initiate the record of the total score
    total_score = 0
    # iterate through cards 
    for card in cards:
        # Get the value of each cards, and accumulate
        total_score += get_score(card)

    # return sum
    return total_score
    
def get_score(card):
    '''This is a function that calculates the value of a single card
    
    Argument: A string of a card (ex.'AC')
    
    Return: An interger, based on the value of the card 
    '''
    # Set the all possible letters / numbers appearing in card
    values = "A234567890JQK"
    # Using indexing method to find the value of each letter / number
    return values.index(card[0]) + 1

def comp10001huxxy_valid_table(groups):
    '''This function evaluates whether the table state is valide of not.
    
    Argument: groups: A list of lists of cards. 
              each list of cards (2-element string) represents a single group 
              on the table, and the combined list of lists represents the 
              combined groups played to the table.
    Return: A boolean indicating whether the table is valid or not.
    '''
    
    # Iterate through each group
    for group in groups:
        if not valid_run(group) and not valid_n_of_a_kind(group):
            return False
    return True 

def valid_run(group):
    '''This function verifies if a group is a valid run or not.
        Argument:
        group: A list of cards
        
        Return:
        A boolean value that indicates if the group is valid run or not.
        '''
    
    # 1. At least three cards
    if len(group)< 3:
        return False 
    
    # Sort the group in ascending value
    sorted_groups = sorted(group, key=get_score)
    
    # iterate through each card in group
    for i in range(0, len(group) - 1): 
        # 2. Continuous sequence of value ('A','2','3','4')
        if get_score(sorted_groups[i + 1]) - get_score(sorted_groups[i]) != 1:
            return False
        # 3. Alternating colour ('red','black','red','black')
        if get_colour(sorted_groups[i + 1]) == get_colour(sorted_groups[i]):
            return False
    return True  
    

    
def get_score(card):
    '''This is a function that calculates the value of a single card
    
    Argument: 
        card:A string of a card (ex.'AC')
    
    Return: 
        An interger, based on the value of the card 
    '''
    # Set the all possible letters / numbers appearing in card
    values = "A234567890JQK"
    # Using indexing method to find the value of each letter / number
    return values.index(card[0]) + 1

def get_colour(card):
    '''This function identifies the colour of a single card
    
    Argument: 
        card:A string of a card (ex.'AC')
    
    Return: 
        A string, based on the colour of the card 
    '''
    if card[1] in 'CS':
        return 'black'
    elif card[1] in 'HD':
        return 'red'

def valid_n_of_a_kind(group):
    '''This function verifies if a group is a valid N of a kind or not.
    
        Argument:
            group: A list of cards
        
        Return:
            A boolean value that indicates if the group is valid N-of-a
            -kind or not.
        '''
    
    # 1. Number of cards > 3
    if len(group)< 3:
        return False 
    
    # 2. Same cards value
    # Store value of first card in variable
    initial_value = get_score(group[0])
    
    for i in range(1, len(group)): 
        if get_score(group[i]) != initial_value: 
            return False 
            
    # 3. No repeated suits 
    
    # Recording number of UNIQUE suits 
    num_of_suit = 0
    suit_list = []
    for i in range(0, len(group)):
        if group[i][1] not in suit_list:
            suit_list.append(group[i][1])
            num_of_suit += 1
        else:
            suit_list = suit_list
            num_of_suit = num_of_suit
    
    # number of cards <= 4, then number of suits == number of cards 
    if len(group) <= 4:
        if num_of_suit != len(group):
            return False 
    # number of cards > 4, all suits should be present    
    elif len(group) > 4: 
        if num_of_suit != 4:
            return False
    return True
    
# DO NOT DELETE/EDIT THIS LINE OF CODE, AS IT IS USED TO PROVIDE ACCESS TO
# THE FUNCTIONS FROM THE PREVIOUS QUESTION
from hidden import comp10001huxxy_valid_table

def comp10001huxxy_valid_play(play, play_history, active_player, hand, table):
    '''This function checks if a play if valid given the current game state.
    Argument: 
        play: A 3-tuple representing the play
            play_turn: player who plays 
            play_type: 
                0: draw a card (implicitly ends the turn)
                1: play a card
                2: move a card 
                3: end turn
            play_details:
                0: None
                1: (card, to_group)
                2: (card, from_group, to_group)
                3: None
        play_history: A list of 3-tuple representing all the plays
        active_player: An integer representing the current player
        hand: A list of all cards held by active_player
        table: A list of lists of cards represnting what on the table
    Return:
    A boolean value indicating whether the player is valid
        '''
    
    # Check for player
    if play[0] != active_player:
        return False
    
    # play type 0: draw a card, and end turn
    if play[1] == 0:
        # Check if player has made type 1 play in this turn
        if has_made_type_1_plays(play_history, play[0]):
            return False
        else: 
            return True  
    
    # play type 1: play a card
    if play[1] == 1:
        # Check if this is a valid play a card to group
        # 1. Check if card - play[2][0] exists in hand
        if play[2][0] not in hand:
            return False
        # 2. Check if to_group - play[2][1] is valid group(bigger than 0,     
        # smaller and equal to len of table)
        if not (play[2][1] <= len(table)):
            return False
        return True
    
    # play type 2: move a card 
    if play[1] == 2:
        # Check if player has made a type 1 play before this play
        if not has_made_type_1_plays(play_history, play[0]):
            return False
        # Check if this is a valid move a card from group 1 to group 2 
        # 1. Check if card - play[2][0] exists in hand
        if play[2][0] not in hand:
            return False        
        # 2. Check if from_group: play[2][1] is a valid group (bigger than 0, 
        # smaller than len of table) (NOT EQUAL)
        # FROM_GROUP AND TO_GROUP HAVE DIFFERENT RANGE (otherwise index error)
        if not (play[2][1] < len(table)):
            return False
        # 3. Check if to_group - play[2][2] is valid group(bigger than 0,     
        # smaller and equal to len of table)
        if not (play[2][2] <= len(table)):
            return False
        return True
        
    # play type 3: end a turn
    if play[1] == 3:
        # 1. Check if player has made a type 1 play before this play
        # if player has not  made any type 1 play prior to type 3 play 
        # in this turn - return False
        # You can't end a turn without playing a card before 
        if not has_made_type_1_plays(play_history, play[0]):
            return False
        # 2. Check if player has completed openning turn
        # if player has not made type 3 play in the history:
        if not has_completed_openning_turn(play_history, play[0]):
            # Check total scores of cards played to table in this turn >= 24
            if total_score(play_history) < 24:
                return False
        
        # 3. Check for valid Table    
        if not comp10001huxxy_valid_table(table):
            return False
        
    return True  
    
def has_completed_openning_turn(play_history, player):
    '''This function checks if the player has completed an openning turn 
    or not. 
    
    Arguments:
        play_history: a list of 3-tuples representing all plays that have 
        taken place in the game so far (in chronological order).
        
        player: an integer between 0 and 3 inclusive which represents 
        which the player number of the player whose turn it is to play.
        
    Return:
        A boolean value that indicates whether a player has completed an 
        openning turn or not.
    '''
    for play in play_history: 
        if play[0] == player and play[1] == 3:
            return True 
    return False    

def has_made_type_1_plays(play_history, player):
    '''This function checks if one player has made a type 1 play before 
        Argument: 
            play_history: A list of 3-tuple representing all the plays
            player: An integer representing the current player
        Return:
            A boolean value'''
    for play in play_history[::-1]:
        if play[0] != player:
            break 
        if play[1] == 1:    
            return True
    return False

def total_score(play_history):
    '''This function calculates the score the cards in player's hand.
    
    Argument: 
        play_history: A list of 3-tuple representing all the plays 
    
    Return:
        An ingeter that calculates the score of cards in player's hand. 
    '''
    # To initiate the record of the total score
    total_score = 0
    # iterate through cards in history  
    for history in play_history:
        # Get the value of each cards, and accumulate
        total_score += get_score(history[2][0])
    # return sum
    return total_score
    
def get_score(card):
    '''This is a function that calculates the value of a single card
    
    Argument: 
        card: A string of a card (ex.'AC')
    
    Return: 
        An interger, based on the value of the card 
    '''
    # Set the all possible letters / numbers appearing in card
    values = "A234567890JQK"
    # Using indexing method to find the value of each letter / number
    return values.index(card[0]) + 1
    
from itertools import combinations
from copy import deepcopy
# list of plays in a turn 
turn = []


def comp10001huxxy_play(play_history, active_player, hand, table):
    '''This function generates a play for an active player.
    
    Arguments:
        play_history: a list of 3-tuples representing all plays that have 
        taken place in the game so far (in chronological order).
        
        active_player: an integer between 0 and 3 inclusive which represents 
        which the player number of the player whose turn it is to play.
        
        hand: a list of the cards held by the player attempting the play.
        
        table: a list of list of cards representing the table
    
    Return:
        A 3-tuple representing the play
            play_turn: player who plays 
            play_type: 
                0: draw a card (implicitly ends the turn)
                1: play a card
                2: move a card 
                3: end turn
            play_details:
                0: None
                1: (card, to_group)
                2: (card, from_group, to_group)
                3: None
    '''
    
    global turn 
    if has_completed_openning_turn(play_history, active_player): 
        return active_player, 0, None
    
    else:
        if not turn: 
            if not has_made_type_1_plays(play_history, active_player):
                turn = opening_strategy(active_player, hand, table)
                return turn[0]
            else: 
                return active_player, 3, None
        else:
            turn.pop(0)

    
    
def opening_strategy(active_player, hand, table):
    '''This function plays cards for opening turn
    
    Argument:
        play_history: a list of 3-tuples representing all plays that have 
        taken place in the game so far (in chronological order).
        active_player: an integer between 0 and 3 inclusive which represents 
        which the player number of the player whose turn it is to play.
        table: a list of list of cards representing the table
    
    Return:
        A list of possible plays (3-tuples)
    
    '''
    # Consider groups at the start of turn 
    for i in range(len(table) + 1):
        # if i is new group
        if i == len(table):
            candidate_cards = [card for card in hand]
            for combination in combinations(candidate_cards, 4):
                return [(active_player, i, (card, i)) for card in combination]   
        else: 
            candidates = run_candidates(table[i]) + noak_candidates(table[i])
            
        candidate_cards = [card for card in hand if card in candidates]
        for combination in combinations(candidate_cards, 4):
            if sum(get_score(card) for card in combination) >= 24:
                copy_table = deepcopy(table)
                copy_table[i] += list(combination)
                if is_valid_table(copy_table):
                    return [(active_player, i, (card, i)) for card in 
                            combination]
            
        
def noak_candidates(group):
    '''Finding the possible cards to place before or after a group on the 
    table
    
    Argument:
        group: A list of cards
    
    Return:
        A list of potential cards that can be added to the N-of-a-kind 
        group on the table. 
    '''
    if group[0][0] != group[1][0]:
        return []
    value = group[0][0]
    return [value + s for s in 'CDHS']

def run_candidates(group):
    '''Finding the possible cards to place before or after a group on the 
    table
    
    Argument:
        group: A list of cards
    
    Return:
        A list of potential cards that can be added to the run group on
        the table. 
    
    '''
    literal = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
               7: '7', 8: '8', 9: '9', 10: '0', 11: 'J', 12: "Q", 13: "K"}
    sorted_group = sorted(group, key=get_score)
    if group[0][0] == "A":
        if group[0][1] in 'CS':
            before = []
            after = [literal[get_score(sorted_group[-1]) + 1] + s 
                     for s in "DH"]
        if group[0][1] in 'DH':
            before = []
            after = [literal[get_score(sorted_group[-1]) + 1] + s 
                     for s in "CS"] 
        return [before + after] 

    if group[-1][0]== "K":
        if group[0][1] in 'CS':
            after = []
            before = [literal[get_score(sorted_group[0]) - 1] + s 
                      for s in "DH"]
        if group[0][1] in 'DH':
            after = []
            before = [literal[get_score(sorted_group[0]) - 1] + s 
                      for s in "CS"]
        return [before + after] 

    if group[0][1] in 'CS':
        before = [literal[get_score(sorted_group[0]) - 1] + s for s in "DH"]
        after = [literal[get_score(sorted_group[-1]) + 1] + s for s in "DH"]
    if group[0][1] in 'DH':
        before = [literal[get_score(sorted_group[0]) - 1] + s for s in "CS"]
        after = [literal[get_score(sorted_group[-1]) + 1] + s for s in "CS"]        

    return [before + after]    
    
def has_completed_openning_turn(play_history, active_player):
    '''This function checks if the player has completed an openning turn 
    or not. 
    
    Arguments:
        play_history: a list of 3-tuples representing all plays that have 
        taken place in the game so far (in chronological order).
        
        active_player: an integer between 0 and 3 inclusive which represents 
        which the player number of the player whose turn it is to play.
        
    Return:
        A boolean value that indicates whether a player has completed an 
        openning turn or not.
    
    '''
    if play_history:
        for play in play_history: 
            if play[0] == active_player and play[1] == 3:
                return True
    else:        
        return False 

def get_score(card):
    '''This is a function that calculates the value of a single card
    
    Argument: 
        card: A string of a card (ex.'AC')
    
    Return: An interger, based on the value of the card 
    '''
    # Set the all possible letters / numbers appearing in card
    values = "A234567890JQK"
    # Using indexing method to find the value of each letter / number
    return values.index(card[0]) + 1

def has_made_type_1_plays(play_history, active_player):
    '''This function checks if one player has made a type 1 play before 
        Argument: 
            play_history: A list of 3-tuple representing all the plays
            player: An integer representing the current player
        Return:
            A boolean value'''
    for play in play_history[::-1]:
        if play[0] != active_player:
            break 
        if play[1] == 1:    
            return True
    return False

def is_valid_table(table):
    '''This function evaluates whether the table state is valide of not.
    
    Argument: groups: A list of lists of cards. 
              each list of cards (2-element string) represents a single group 
              on the table, and the combined list of lists represents the 
              combined groups played to the table.
    Return: A boolean indicating whether the table is valid or not.
    '''
    
    # Iterate through each group
    for group in table:
        if not valid_run(group) and not valid_n_of_a_kind(group):
            return False
    return True 

def valid_run(group):
    '''This function verifies if a group is a valid run or not.
        Argument:
        group: A list of cards
        
        Return:
        A boolean value that indicates if the group is valid run or not.
        '''
    
    # 1. At least three cards
    if len(group)< 3:
        return False 
    
    # Sort the group in ascending value
    sorted_groups = sorted(group, key=get_score)
    
    # iterate through each card in group
    for i in range(0, len(group) - 1): 
        # 2. Continuous sequence of value ('A','2','3','4')
        if get_score(sorted_groups[i + 1]) - get_score(sorted_groups[i]) != 1:
            return False
        # 3. Alternating colour ('red','black','red','black')
        if get_colour(sorted_groups[i + 1]) == get_colour(sorted_groups[i]):
            return False
    return True  
    

def get_colour(card):
    '''This function identifies the colour of a single card
    
    Argument: A string of a card (ex.'AC')
    
    Return: A string, based on the colour of the card 
    '''
    if card[1] in 'CS':
        return 'black'
    elif card[1] in 'HD':
        return 'red'

def valid_n_of_a_kind(group):
    '''This function verifies if a group is a valid N of a kind or not.
       Argument:
            group: A list of cards
        
       Return:
            A boolean value that indicates if the group is valid N-of-a-
            kind or not.
        '''
    
    # 1. Number of cards > 3
    if len(group)< 3:
        return False 
    
    # 2. Same cards value
    # Store value of first card in variable
    initial_value = get_score(group[0])
    
    for i in range(1, len(group)): 
        if get_score(group[i]) != initial_value: 
            return False 
            
    # 3. No repeated suits 
    
    # Recording number of UNIQUE suits 
    num_of_suit = 0
    suit_list = []
    for i in range(0, len(group)):
        if group[i][1] not in suit_list:
            suit_list.append(group[i][1])
            num_of_suit += 1
        else:
            suit_list = suit_list
            num_of_suit = num_of_suit
    
    # number of cards <= 4, then number of suits == number of cards 
    if len(group) <= 4:
        if num_of_suit != len(group):
            return False 
    # number of cards > 4, all suits should be present    
    elif len(group) > 4: 
        if num_of_suit != 4:
            return False
    return True