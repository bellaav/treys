import re
import pandas as pd

from treys import Evaluator
from treys import PLOEvaluator
from treys import Card



evaluator = Evaluator()
omaha_evaluator = PLOEvaluator()

df = pd.read_csv('/Users/iting/Downloads/actual_omaha.csv')


df['pocket_cards'] = None 
df['table'] = None
df['best_five_cards'] = None #Contains the best 5 ranking cards fit here, this takes into consideration the hand as well. ie, pair will always contain the pair in best 5
df['evaluation_result'] = None #The evaluation result is the best hand type in the cards given

# Iterate over the df to extract and transform card values
for index, row in df.iterrows():
    game_mode = row['game_mode'] 

    if game_mode == 'holdem':
        input_string = row[1]  # Assuming the card values are in the second column
        card_values = [input_string[i:i+2] for i in range(0, len(input_string), 2)] #Parses out the string into individual cards

        # Initialize 'pocket_cards' and 'table' lists
        pocket_cards = []
        table = []

        # Determine the pocket cards and table based on the number of cards
        if len(card_values) >= 2:
            #Takes the first 2 cards as the pocket cards and the remaining cards as cards on the river. Puts each card in the Card.new() function
            pocket_cards = [Card.new(card_values[0]), Card.new(card_values[1])] 
            table = [Card.new(card) for card in card_values[2:]] 

        # Update the df with the 'pocket_cards' and 'table' lists
        df.at[index, 'pocket_cards'] = pocket_cards
        df.at[index, 'table'] = table if table else None
    elif game_mode == 'omaha':
        input_string = row[1]  # Assuming the card values are in the second column
        card_values = [input_string[i:i+2] for i in range(0, len(input_string), 2)] #Parses out the string into individual cards

        # Initialize 'pocket_cards' and 'table' lists
        pocket_cards = []
        table = []

        # Determine the pocket cards and table based on the number of cards
        if len(card_values) >= 4:
            #Takes the first 2 cards as the pocket cards and the remaining cards as cards on the river. Puts each card in the Card.new() function
            pocket_cards = [Card.new(card_values[0]), Card.new(card_values[1]),Card.new(card_values[2]),Card.new(card_values[3])] 
            table = [Card.new(card) for card in card_values[4:]] 

        # Update the df with the 'pocket_cards' and 'table' lists
        df.at[index, 'pocket_cards'] = pocket_cards
        df.at[index, 'table'] = table if table else None

## double check
print(df.head(1))

#Iterate through the rows
for index, row in df.iterrows():
    table_value = row['table']
    pocket_card_value = row['pocket_cards']
    stripped_cards_value = row['stripped_cards']
    game_mode = row['game_mode'] 

    # Check if the length of 'stripped_cards' is greater than or equal to 10
    if len(stripped_cards_value) >= 10:

        #Check for the game mode
        if game_mode == 'holdem':
            # Call the evaluator.evaluate function and store the result in 'evaluation_result'
            #Rge original evaluator.evaluate was modified to also return the best performing 'combo' which is the best permutation of 5 cards out of the 6/7  
            best_hand, combo = evaluator.evaluate(table_value, pocket_card_value)
            df.at[index, 'evaluation_result'] = evaluator.class_to_string(evaluator.get_rank_class(best_hand))

            #Check that the combo is a tuple. If the combo is None, it means it went through the _five function, and the best 5 cards is the same 5 cards inputted
            if isinstance(combo, tuple):
                df.at[index, 'best_five_cards'] = "".join(Card.ints_to_pretty_str(list(combo)))
            elif combo == None:
                df.at[index, 'best_five_cards'] = df.at[index, 'stripped_cards']
            else:
                print("Weird, you shouldn't be here")
        elif game_mode == 'omaha':
            best_hand, combo = omaha_evaluator.evaluate(table_value, pocket_card_value)

            df.at[index, 'evaluation_result'] = evaluator.class_to_string(evaluator.get_rank_class(best_hand))
            if isinstance(combo, list):
                df.at[index, 'best_five_cards'] = "".join(Card.ints_to_pretty_str(list(combo)))
            elif combo == None:
                df.at[index, 'best_five_cards'] = df.at[index, 'stripped_cards']
            else:
                print("Weird, you shouldn't be here")
        else:
            "No game mode found"


csv_file_path = '/Users/iting/Downloads/output_snippet.csv'

# Export the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)  












