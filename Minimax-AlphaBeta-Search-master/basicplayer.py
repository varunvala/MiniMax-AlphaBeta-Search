from util import memoize, run_search_function
import math
from time import time

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified.
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()

internal_depth =1
max_board_score = 0
column_choice =-1
MIN="min_search"
MAX="max_search"
nodes_expanded = 0
execution_time = 0
def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    time1 = time()
    global execution_time
    moves_list = []
    global internal_depth
    global max_board_score
    global max_column
    global column_choice
    get_next_moves_fn = get_all_next_moves(board)
    max_level_value = -1
    min_level_value = float("inf")
    #For all moves from this board which came from the opponent we need to get the maximum score if we are the CurrentPlayer, else
    #we need to get the minimum score
    for i in get_next_moves_fn:
        moves_list.append(i[1])
        if(board.get_current_player_id()==1):
            maxSearch_value = minimax_varun(i[1],depth-1,MAX,eval_fn)
            #Second argument is to ensure that we are not adding the token to the column that is already full
            if ((maxSearch_value < min_level_value)and ((board.get_height_of_column(i[0]))!=0)) :
                min_level_value = maxSearch_value
                column_choice = i[0]
        else:
            minSearch_value = minimax_varun(i[1],depth-1,MIN,eval_fn)
            if ((minSearch_value > max_level_value)and ((board.get_height_of_column(i[0]))!=0)) :
                max_level_value = minSearch_value
                column_choice = i[0]
    time2 = time()
    execution_time += time2 - time1
    board.update_execution_time(execution_time)
    return column_choice

    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    raise NotImplementedError

#Gives out maximum score for every board that is passed to this method if it is for CurrentPlayer, else it will give out minimum score
def minimax_varun(board, depth, Type, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    global nodes_expanded
    nodes_expanded += 1
    board.update_nodes_expanded(nodes_expanded)
    internal_moves_list = []
    global minimax_varun_score
    #if eval_fn.func_name=="new_evaluate" :
    #    print("nodes_expanded are: ",nodes_expanded)
    if Type=="min_search" :
        minimax_varun_score = -1
    else :
        minimax_varun_score = float("inf")

    if is_terminal(depth, board):
        minimax_varun_score = eval_fn(board)
    else:
        get_next_moves_fn = get_all_next_moves(board)
        for i in get_next_moves_fn:
            internal_moves_list.append(i[1])
            if Type == "min_search":
                #Here current player is trying to get the minimum of its children(which are max nodes)
                maxSearch_value = minimax_varun(i[1],depth-1,MAX,eval_fn)
                if maxSearch_value < minimax_varun_score :
                    minimax_varun_score = maxSearch_value
            else:
                #Here current player is trying to get the maximum of its children(which are min nodes)
                minSearch_value = minimax_varun(i[1],depth-1,MIN,eval_fn)
                if minSearch_value > minimax_varun_score :
                    minimax_varun_score = minSearch_value
    return minimax_varun_score

    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """

nodes_expanded_alphabeta = 0
def alpha_beta_varun(board, depth, Type, eval_fn,alpha_value=float("-inf"),beta_value=float("inf"),
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    global nodes_expanded_alphabeta
    nodes_expanded_alphabeta += 1
    board.update_nodes_expanded(nodes_expanded_alphabeta)
    global minimax_varun_score
    internal_moves_list = []

    if is_terminal(depth, board):
        return eval_fn(board)
    else:
        get_next_moves_fn = get_all_next_moves(board)
        for i in get_next_moves_fn:
            internal_moves_list.append(i[1])
            if Type == "min_search":
                #Here current player is trying to get the minimum of its children(which are max nodes)
                maxSearch_value = alpha_beta_varun(i[1],depth-1,MAX,eval_fn,alpha_value,beta_value)
                if maxSearch_value < beta_value :
                    beta_value = maxSearch_value
            else:
                #Here current player is trying to get the maximum of its children(which are min nodes)
                minSearch_value = alpha_beta_varun(i[1],depth-1,MIN,eval_fn,alpha_value,beta_value)
                if minSearch_value > alpha_value :
                    alpha_value = minSearch_value

            # Alpha-Beta Pruning
            if alpha_value>=beta_value:
                break

    if(Type=="min_search"):
        return beta_value
    else:
        return alpha_value

def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]

# Applies terminal functions and gets the evaluation scores
def new_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified.
    """

    #Logic for new_evaluate function:
    #1)Traverse through each of the columns
    #2)For each of the columns, find the top most element.
	    #If the topmost element = Current Player
		    	#3)Find the possible number of continuous elements of the same type in all the 4 directions from that cell(Horizontal,vertical and two diagonals)
			      #Take the max of these lengths and this becomes the score for that column and it will stored as a POSITIVE value
	    #Else
		    	#4)Find the possible number of continuous elements of the same type in all the 4 directions from that cell(Horizontal,vertical and two diagonals)
			      #Take the max of these lengths and this becomes the score for that column and it will stored as a NEGATIVE value
    #5)Sort these Positive and Negative scores
    #6)IF the highest negative score is greater than the highest positive score, then it means that the opposition has MORE chances to WIN.
    #So, that has to be blocked and so we will return that HIGHEST NEGATIVE value as the score for that board
    #7)ELSE we go ahead and return the HIGHEST POSITIVE value as the score for that board
    #->This logic has increasing the AGGRESSION of the player a lot and it makes senses we hope.

    posdict = {}
    negdict = {}
    for col in range(7):
        if(board.get_top_elt_in_column(col)==board.get_current_player_id()) :
            rowValue = board.get_height_of_column(col)
            score = board._max_length_from_cell(rowValue,col)
            posdict[col]=score
        elif(board.get_top_elt_in_column(col)==board.get_other_player_id()) :
            rowValue = board.get_height_of_column(col)
            score = -(board._max_length_from_cell(rowValue,col))
            negdict[col]=score


    sorted(posdict.values(),reverse= True)
    sorted(negdict.values())
    if((bool(posdict))and (bool(negdict))):
        if(abs(negdict.values()[0]) >= ((posdict.values()[0]))):
            return negdict[negdict.keys()[0]]
        else:
            return posdict[posdict.keys()[0]]
    elif(bool(posdict)):
        return posdict[posdict.keys()[0]]
    elif(bool(negdict)):
        return negdict[negdict.keys()[0]]
    else:
        return 0

# Longest Streak to win
# It uses longest_streak_to_win_evaluate evaluation function and weighted evaluation as heuristic
# It counts the number of tokens that are in the board at present
# If the total number of tokens are more than or equal to 20, it breaks
# And then it checks which player has more tokens on the board
def longest_streak_to_win_search(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    # Tracking the execution time
    time1 = time()
    noOfStreaks = 0
    board_height = board.board_height
    score1 = 0
    score2 = 0
    # Counting the tokens on the board
    for col in range(7):
        columnHeight = board.get_height_of_column(col)
        if(columnHeight != board_height):
            noOfStreaks += (board_height - columnHeight - 1)
    # Check if total no of tokens are more than or equal to 20
    if(noOfStreaks >= 20):
        score1 = board.longest_chain(1)
        score2 = board.longest_chain(2)
        # checks which player has more tokens on the board
        # Player 1 wins
        if(score1 > score2):
            print "Player 1 has won, Longest streak: ", score1
            print "Win for X!"
        # It is a tie
        elif(score1 == score2):
            print "It's a tie, longest streak: ", score1
        # Player 2 wins
        else:
            print "Player 2 has won, Longest streak: ", score2
            print "Win for O!"
        exit(0)
    global execution_time
    moves_list = []
    global internal_depth
    global max_board_score
    global max_column
    global column_choice
    get_next_moves_fn = get_all_next_moves(board)
    max_level_value = -1
    min_level_value = float("inf")
    #print (min_level_value)
    # Get number of valid moves
    for i in get_next_moves_fn:
        moves_list.append(i[1])
        if(board.get_current_player_id()==1):
            maxSearch_value = longest_streak_explore(i[1],depth-1,MAX,eval_fn)
            if ((maxSearch_value < min_level_value) and ((board.get_height_of_column(i[0]))!=0)) :
                min_level_value = maxSearch_value
                column_choice = i[0]
        else:
            minSearch_value = longest_streak_explore(i[1],depth-1,MIN,eval_fn)
            if ((minSearch_value > max_level_value)  and ((board.get_height_of_column(i[0]))!=0)) :
                max_level_value = minSearch_value
                column_choice = i[0]
    time2 = time()
    execution_time += time2 - time1
    noOfStreaks = 0
    for col in range(7):
        columnHeight = board.get_height_of_column(col)
        if(columnHeight != board_height):
            noOfStreaks += (board_height - columnHeight - 1)
    if(noOfStreaks > 20):
        score1 = board.longest_chain(1)
        score2 = board.longest_chain(2)
        if(score1 > score2):
            print("Player 1 has won, longest streak: ", score1)
        elif(score1 == score2):
            print("It's a tie, longest streak: ", score1)
        else:
            print("Player 2 has won, longest streak: ", score2)
        exit(0)
    return column_choice

weighted_eval_score = 0
# Applies terminal functions and gets the evaluation scores
def longest_streak_explore(board, depth, Type, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    global nodes_expanded
    global weighted_eval_score
    nodes_expanded += 1
    internal_moves_list = []
    global minimax_varun_score
    basic_score = 0
    weighted_eval_score = 0
    if is_terminal(depth, board):
        minimax_varun_score = eval_fn(board)
        basic_score = basic_evaluate(board)
        weighted_eval_score = (2 * basic_score) + (3 * minimax_varun_score)
    else:
        get_next_moves_fn = get_all_next_moves(board)
        for i in get_next_moves_fn:
            internal_moves_list.append(i[1])
            if Type == "min_search":
                maxSearch_value = longest_streak_explore(i[1],depth-1,MAX,eval_fn)
                if maxSearch_value < weighted_eval_score :
                    weighted_eval_score = maxSearch_value
            else:
                minSearch_value = longest_streak_explore(i[1],depth-1,MIN,eval_fn)
                if minSearch_value > weighted_eval_score :
                    weighted_eval_score = minSearch_value
    return weighted_eval_score

# Uses weighted evaluation as heuristic
def longest_streak_to_win_evaluate(board):
    posdict = {}
    negdict = {}
    for col in range(7):
        if(board.get_top_elt_in_column(col)==board.get_current_player_id()) :
            rowValue = board.get_height_of_column(col)+1
            score = board._max_length_from_cell(rowValue,col)
            posdict[col]=score
        elif(board.get_top_elt_in_column(col)==board.get_other_player_id()) :
            rowValue = board.get_height_of_column(col)+1
            score = -(board._max_length_from_cell(rowValue,col))
            negdict[col]=score

    sorted(posdict.values(),reverse= True)
    sorted(negdict.values())
    if((bool(posdict))and (bool(negdict))):
        if(abs(negdict.values()[0]) >= ((posdict.values()[0]))):
            return negdict[negdict.keys()[0]]
        else:
            return posdict[posdict.keys()[0]]
    elif(bool(posdict)):
        return posdict[posdict.keys()[0]]
    elif(bool(negdict)):
        return negdict[negdict.keys()[0]]
    else:
        return 0


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
longest_streak_to_win_player = lambda board: longest_streak_to_win_search(board, depth=4, eval_fn=longest_streak_to_win_evaluate)