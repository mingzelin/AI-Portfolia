"""
This is the only file you should change in your submission!

Name: MINGZEEEE
id: 20655470
email: m59lin@edu.uwaterloo.ca

"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, NEG_INFINITY, INFINITY


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

# STUDENT_ID = 20655470
# AGENT_NAME = MINGZELIN
# COMPETE = TRUE

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    if board.is_tie():
        #if the game is tie
        score = 0
    elif board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -2000 - (42 - board.num_tokens_on_board())
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


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.

# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.

     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.

     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.

     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """
    best_val = None
    id = 1
    #init both values to worst possible
    alpha = NEG_INFINITY #my turn
    beta  = NEG_INFINITY #his turn

    for move, new_board in get_next_moves_fn(board):
       #if variables are init, we need to change view before pass to children
        arg1 = alpha
        arg2 = beta

        #pass on to children in their view
        if(alpha!=NEG_INFINITY):
            arg1 = -arg1
        if(beta!=NEG_INFINITY):
            arg2 = -arg2
        pair = alphabeta_find_board_value(id, arg1, arg2, new_board, depth-1, eval_fn,
                                                    get_next_moves_fn, is_terminal_fn)
        #receive children assume that pair is in their view
        #translate pair
        #pair[1] keep view on beta of children node
        if(pair[0]!=NEG_INFINITY): #change view on alpha of children node
            pair[0] = -pair[0]

        #init best_val
        if best_val is None:
            alpha = pair[0]
            best_val = (alpha, move, new_board)


        #update according to most benifit alpha or beta
        #previous is not my turn, only beta is guranteed to be set
        if(pair[0]!=NEG_INFINITY):
            if(pair[0]>alpha):
                alpha = pair[0]
                best_val = (alpha, move, new_board)
        if((-pair[1])>alpha):
            alpha = -pair[1]
            best_val = (alpha, move, new_board)
        #no need to prune for root

    #print("ALPHABETA: Decided on column {} with rating {}".format(best_val[1], best_val[0]))
    return best_val[1]


#function return the pair of alpha beta pair
def alphabeta_find_board_value(id, alpha, beta, board, depth, eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """

    #the id pass in is the owner of parent node
    if(id==1):
        id=2
        my_turn = False
    else:
        id=1
        my_turn = True


    #base case: return alpha beta pair
    if is_terminal_fn(depth, board):
        eval = eval_fn(board)
        if(my_turn):
            alpha=eval
        else:
            beta=eval
        result = [alpha, beta, True]
        return result

    best_val = None


    for move, new_board in get_next_moves_fn(board):
        #if variables are init, we need to change view before pass to children
        arg1 = alpha
        arg2 = beta

        #pass on to children in their view
        if(alpha!=NEG_INFINITY):
            arg1 = -arg1
        if(beta!=NEG_INFINITY):
            arg2 = -arg2
        pair = alphabeta_find_board_value(id, arg1, arg2, new_board, depth-1, eval_fn,
                                                    get_next_moves_fn, is_terminal_fn)

        #receive children assume that pair is in their view
        #translate pair from children
        if(my_turn):
            #pair[1] keep view on beta of children node
            if(pair[0]!=NEG_INFINITY): #change view on alpha of children node
                pair[0] = -pair[0]
        else:
            #pair[0] keep view on alpha of children node
            if(pair[1]!=NEG_INFINITY): #change view on beta of children node
                pair[1] = -pair[1]




        #update according to most benifit alpha or beta
        if(my_turn): #previous is not my turn, only beta is guranteed to be set
            if(pair[0]!=NEG_INFINITY):
                if(pair[0]>alpha):
                    alpha = pair[0]
            if((-pair[1])>alpha):
                alpha = -pair[1]
        else:
            #previous is my turn, only alpha is guranteed to be set
            if((-pair[0])>beta):
                beta = -pair[0]
            if(pair[1]!=NEG_INFINITY):
                if(pair[1]>beta):
                    beta = pair[1]

        #pruning decision
        #if beta>=alpha prune, because beta will only find an even larger value for itself
        #there's no need to continue search on the same branch
        if(alpha!=NEG_INFINITY): #alpha is init
            if(beta!=NEG_INFINITY): #beta is init
                if(my_turn):
                    if(not (my_turn and pair[2]==True)): #if max turn and depth == 1, do not prune
                        if(beta<=alpha):
                            #prune
                            break
                else:
                    if(not (my_turn and pair[2]==True)): #if max turn and depth == 1, do not prune
                        if(beta>=alpha):
                            #prune
                            break

    result = [alpha, beta, False] #return everything in its view

    return result


# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=5, eval_fn=focused_evaluate)
#TODO focused_evaluate   8


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)



def isSpace(board, y, x):
    if(board.get_cell(y, x)==0): #the spot is free
        if(y==5): #If at bottom, then is must be ok
            return True
        else:
            if(board.get_cell(y+1, x)!=0): #the spot below is occupied
                return True
    return False



##prediction and heuristic function for competition
#prediction:
##return 1 for win, return 2 for lose, return 3 for unsure
#heuristic:
##count availability of unsealed continuous blocks heuristic
##7 pt for single side unsealed block 2
##14 pt for double side unsealed block 2
##100pt for single side unsealed block 3
##unsealed block 3 is not considered for my side heuristic as it is a win or lose
def predict_win(board, heuristic):
    curr_id = board.get_current_player_id()
    other_id = board.get_other_player_id()

    #init heuristic count
    h_my = 0
    h_opponent = 0

    #part1: check whether current win
    filtered1 = filter(lambda x: len(x) == 2, board.chain_cells(curr_id))
    len2_list = list(filtered1)
    filtered2 = filter(lambda x: len(x) == 3, board.chain_cells(curr_id))
    len3_list = list(filtered2)

    ##check whether any len3 are able to have one more
    for item in len3_list:
        if((item[0][0]==item[1][0])and(item[1][0]==item[2][0])):
            ##horizontal
            max = -1
            min = 100
            for row in item:
                if(row[1]>max):
                    max = row[1]
                if(row[1]<min):
                    min = row[1]
            if((min-1)>=0): #in bounds
                if(isSpace(board, item[0][0], min-1)): ##1 empty space
                    ##found 4th on the left
                    return 1
            elif((max+1)<=6): #in bounds
                if(isSpace(board, item[0][0], max+1)): ##1 empty space
                    ##found 4th on the right
                    return 1
        elif((item[0][1]==item[1][1])and(item[1][1]==item[2][1])):
            ##vertical
            max = -1
            min = 100
            for row in item:
                if(row[0]>max):
                    max = row[0]
                if(row[0]<min):
                    min = row[0]
            if((min-1)>=0): #in bounds
                if(isSpace(board, min-1, item[0][1])): ##1 empty space
                    ##found 4th on the top
                    return 1
            elif((max+1)<=5): #in bounds
                if(isSpace(board, max+1, item[0][1])): ##1 empty space
                    ##found 4th on the bottom
                    return 1
        else:
            ##diagnol
            ymax = -1
            x_ymax = -1
            ymin = 100
            x_ymin = -1
            for row in item:
                if(row[0]>ymax):
                    ymax = row[0]
                    x_ymax = row[1]
                if(row[0]<ymin):
                    ymin = row[0]
                    x_ymin = row[1]
            if(x_ymax>x_ymin): #downhill diagnol
                if(((x_ymax+1)<=6)and((ymax+1)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax+1))): ##1 empty space
                        ##found 4th
                        return 1
                if(((x_ymin-1)>=0)and((ymin-1)>=0)):#in bounds
                    if(isSpace(board, (ymin-1), (x_ymin-1))): ##1 empty space
                        ##found 4th
                        return 1
            else: #uphill diagnol
                if(((x_ymax-1)>=0)and((ymax+1)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax-1))): ##1 empty space
                        ##found 4th
                        return 1
                if(((x_ymin+1)<=6)and((ymin-1)>=0)):#in bounds
                    if(isSpace(board, (ymin-1), (x_ymin+1))): ##1 empty space
                        ##found 4th
                        return 1

    ##check whether any len2 are able to have one more
    for item in len2_list:
        if(item[0][0]==item[1][0]):
            ##horizontal
            max = -1
            min = 100
            for row in item:
                if(row[1]>max):
                    max = row[1]
                if(row[1]<min):
                    min = row[1]
            if((min-2)>=0): #in bounds
                if(isSpace(board, item[0][0], min-1)): ##1 empty space
                    h_my+=7
                    if(board.get_cell(item[0][0], min-2)==curr_id):##1 self occupied space
                        ##found 4th on the left
                        return 1
            if((max+2)<=6): #in bounds
                if(isSpace(board, item[0][0], max+1)): ##1 empty space
                    h_my+=7
                    if(board.get_cell(item[0][0], max+2)==curr_id):##1 self occupied space
                        ##found 4th on the right
                        return 1
        if(item[0][1]==item[1][1]):
            ##vertical
            max = -1
            min = 100
            for row in item:
                if(row[0]>max):
                    max = row[0]
                if(row[0]<min):
                    min = row[0]
            if((min-2)>=0): #in bounds
                if(isSpace(board, min-1, item[0][1])): ##1 empty space
                    h_my+=7
                    if(board.get_cell(min-2, item[0][1])==curr_id):##1 self occupied space
                        ##found 4th on the top
                        return 1
            if((max+2)<=5): #in bounds
                if(isSpace(board, max+1, item[0][1])): ##1 empty space
                    h_my+=7
                    if(board.get_cell(max+2, item[0][1])==curr_id):##1 self occupied space
                        ##found 4th on the bottom
                        return 1
        else:
            ##diagnol
            ymax = -1
            x_ymax = -1
            ymin = 100
            x_ymin = -1
            for row in item:
                if(row[0]>ymax):
                    ymax = row[0]
                    x_ymax = row[1]
                if(row[0]<ymin):
                    ymin = row[0]
                    x_ymin = row[1]
            if(x_ymax>x_ymin): #downhill diagnol
                if(((x_ymax+2)<=6)and((ymax+2)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax+1))): ##1 empty space
                        h_my+=7
                        if(board.get_cell((ymax+2), (x_ymax+2))==curr_id):##1 self occupied space
                            ##found 4th
                            return 1
                if(((x_ymin-2)>=0)and((ymin-2)>=0)):#in bounds
                    if(isSpace(board, (ymin-1), (x_ymin-1))): ##1 empty space
                        h_my+=7
                        if(board.get_cell((ymin-1), (x_ymin-1))==curr_id):##1 self occupied space
                            ##found 4th
                            return 1
            else:#uphill diagnol
                if(((x_ymax-2)>=0)and((ymax+2)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax-1))): ##1 empty space
                        h_my+=7
                        if(board.get_cell((ymax+2), (x_ymax-2))==curr_id):##1 self occupied space
                            ##found 4th
                            return 1
                if(((x_ymin+2)<=6)and((ymin-2)>=0)):#in bounds
                    if(isSpace(board, (ymin-1), (x_ymin+1))): ##1 empty space
                        h_my+=7
                        if(board.get_cell((ymin-2), (x_ymin+2))==curr_id):##1 self occupied space
                            ##found 4th
                            return 1

    #part2: check whether opponent win
    filtered1 = filter(lambda x: len(x) == 2, board.chain_cells(other_id))
    len2_list = list(filtered1)
    filtered2 = filter(lambda x: len(x) == 3, board.chain_cells(other_id))
    len3_list = list(filtered2)
    #count num of single space by len3,
    #when there are 2 distinct single space by len3, opponent must win
    count = 0
    space_x = -1
    space_y = -1
    ##check whether any len3 are able to have one more
    for item in len3_list:
        if((item[0][0]==item[1][0])and(item[1][0]==item[2][0])):
            ##horizontal
            max = -1
            min = 100
            for row in item:
                if(row[1]>max):
                    max = row[1]
                if(row[1]<min):
                    min = row[1]
            if((min-1)>=0): #in bounds
                if(isSpace(board, item[0][0], min-1)):
                    #space on one sides
                    if(count==0):
                        count+=1
                        space_y=item[0][0]
                        space_x=min-1
                        h_opponent+=100
                    else:
                        if((space_y!=item[0][0])or(space_x!=min-1)):
                            return 2

            if((max+1)<=6): #in bounds
                if(isSpace(board, item[0][0], max+1)):
                    #space on one sides
                    if(count==0):
                        count+=1
                        space_y=item[0][0]
                        space_x=max+1
                        h_opponent+=100
                    else:
                        if((space_y!=item[0][0])or(space_x!=max+1)):
                            return 2
        elif((item[0][1]==item[1][1])and(item[1][1]==item[2][1])):
            ##vertical
            max = -1
            min = 100
            for row in item:
                if(row[0]>max):
                    max = row[0]
                if(row[0]<min):
                    min = row[0]
            if((min-1)>=0): #in bounds
                if(isSpace(board, min-1, item[0][1])):
                    #space on one sides
                    if(count==0):
                        count+=1
                        space_y=min-1
                        space_x=item[0][1]
                        h_opponent+=100
                    else:
                        if((space_y!=min-1)or(space_x!=item[0][1])):
                            return 2
            if((max+1)<=5): #in bounds
                if(isSpace(board, max+1, item[0][1])):
                   #space on one sides
                    if(count==0):
                        count+=1
                        space_y=max+1
                        space_x=item[0][1]
                        h_opponent+=100
                    else:
                        if((space_y!=max+1)or(space_x!=item[0][1])):
                            return 2
        else:
            ##diagnol
            ymax = -1
            x_ymax = -1
            ymin = 100
            x_ymin = -1
            for row in item:
                if(row[0]>ymax):
                    ymax = row[0]
                    x_ymax = row[1]
                if(row[0]<ymin):
                    ymin = row[0]
                    x_ymin = row[1]
            if(x_ymax>x_ymin): #downhill diagnol
                if(((x_ymax+1)<=6)and((ymax+1)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax+1))):
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=ymax+1
                            space_x=x_ymax+1
                            h_opponent+=100
                        else:
                            if((space_y!=ymax+1)or(space_x!=x_ymax+1)):
                                return 2
                if(((x_ymin-1)>=0)and((ymin-1)>=0)): #in bounds
                    if(isSpace(board, (ymin-1), (x_ymin-1))):
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=ymin-1
                            space_x=x_ymin-1
                            h_opponent+=100
                        else:
                            if((space_y!=ymin-1)or(space_x!=x_ymin-1)):
                                return 2
            else: #uphill diagnol
                if(((x_ymax-1)>=0)and((ymax+1)<=5)):#in bounds
                    if(isSpace(board, (ymax+1), (x_ymax-1))):
                       #space on one sides
                        if(count==0):
                            count+=1
                            space_y=ymax+1
                            space_x=x_ymax-1
                            h_opponent+=100
                        else:
                            if((space_y!=ymax+1)or(space_x!=x_ymax-1)):
                                return 2
                if(((x_ymin+1)<=6)and((ymin-1)>=0)): #in bounds
                    if(isSpace(board, (ymin-1), (x_ymin+1))):
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=ymin-1
                            space_x=x_ymin+1
                            h_opponent+=100
                        else:
                            if((space_y!=ymin-1)or(space_x!=x_ymin+1)):
                                return 2
    ##check whether any len2 are able to have one more
    for item in len2_list:
        if(item[0][0]==item[1][0]):
            ##horizontal
            max = -1
            min = 100
            for row in item:
                if(row[1]>max):
                    max = row[1]
                if(row[1]<min):
                    min = row[1]
            if((min-2)>=0): #in bounds
                if(isSpace(board, item[0][0], min-1)): ##1 empty space
                    h_opponent+=7
                    if(board.get_cell(item[0][0], min-2)==curr_id):##1 self occupied space
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=item[0][0]
                            space_x=min-1
                            h_opponent+=93
                        else:
                            if((space_y!=item[0][0])or(space_x!=min-1)):
                                return 2
            if((max+2)<=6): #in bounds
                if(isSpace(board, item[0][0], max+1)): ##1 empty space
                    h_opponent+=7
                    if(board.get_cell(item[0][0], max+2)==curr_id):##1 self occupied space
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=item[0][0]
                            space_x=max+1
                            h_opponent+=93
                        else:
                            if((space_y!=item[0][0])or(space_x!=max+1)):
                                return 2
        if(item[0][1]==item[1][1]):
            ##vertical
            max = -1
            min = 100
            for row in item:
                if(row[0]>max):
                    max = row[0]
                if(row[0]<min):
                    min = row[0]
            if((min-2)>=0): #in bounds
                if(isSpace(board, min-1, item[0][1])): ##1 empty space
                    h_opponent+=7
                    if(board.get_cell(min-2, item[0][1])==curr_id):##1 self occupied space
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=min-1
                            space_x=item[0][1]
                            h_opponent+=93
                        else:
                            if((space_y!=min-1)or(space_x!=item[0][1])):
                                return 2
            if((max+2)<=5): #in bounds
                if(isSpace(board, max+1, item[0][1])): ##1 empty space
                    h_opponent+=7
                    if(board.get_cell(max+2, item[0][1])==curr_id):##1 self occupied space
                        #space on one sides
                        if(count==0):
                            count+=1
                            space_y=max+1
                            space_x=item[0][1]
                            h_opponent+=93
                        else:
                            if((space_y!=max+1)or(space_x!=item[0][1])):
                                return 2
        else:
            ##diagnol
            ymax = -1
            x_ymax = -1
            ymin = 100
            x_ymin = -1
            for row in item:
                if(row[0]>ymax):
                    ymax = row[0]
                    x_ymax = row[1]
                if(row[0]<ymin):
                    ymin = row[0]
                    x_ymin = row[1]
            if(x_ymax>x_ymin): #downhill diagnol
                if(((x_ymax+2)<=6)and((ymax+2)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax+1))): ##1 empty space
                        h_opponent+=7
                        if(board.get_cell((ymax+2), (x_ymax+2))==curr_id):##1 self occupied space
                            #space on one sides
                            if(count==0):
                                count+=1
                                space_y=ymax+1
                                space_x=x_ymax+1
                                h_opponent+=93
                            else:
                                if((space_y!=ymax+1)or(space_x!=x_ymax+1)):
                                    return 2
                if(((x_ymin-2)>=0)and((ymin-2)>=0)):#in bounds
                    if(isSpace(board, (ymin-1), (x_ymin-1))): ##1 empty space
                        h_opponent+=7
                        if(board.get_cell((ymin-1), (x_ymin-1))==curr_id):##1 self occupied space
                            #space on one sides
                            if(count==0):
                                count+=1
                                space_y=ymin-1
                                space_x=x_ymin-1
                                h_opponent+=93
                            else:
                                if((space_y!=ymin-1)or(space_x!=x_ymin-1)):
                                    return 2
            else:#uphill diagnol
                if(((x_ymax-2)>=0)and((ymax+2)<=5)): #in bounds
                    if(isSpace(board, (ymax+1), (x_ymax-1))): ##1 empty space
                        h_opponent+=7
                        if(board.get_cell((ymax+2), (x_ymax-2))==curr_id):##1 self occupied space
                            #space on one sides
                            if(count==0):
                                count+=1
                                space_y=ymax+1
                                space_x=x_ymax-1
                                h_opponent+=93
                            else:
                                if((space_y!=ymax+1)or(space_x!=x_ymax-1)):
                                    return 2
                if(((x_ymin+2)<=6)and((ymin-2)>=0)):#in bounds
                    if(isSpace(board, (ymin-1), (x_ymin+1))): ##1 empty space
                        h_opponent+=7
                        if(board.get_cell((ymin-2), (x_ymin+2))==curr_id):##1 self occupied space
                            #space on one sides
                            if(count==0):
                                count+=1
                                space_y=ymin-1
                                space_x=x_ymin+1
                                h_opponent+=93
                            else:
                                if((space_y!=ymin-1)or(space_x!=x_ymin+1)):
                                    return 2
    heuristic[0] = h_my - h_opponent
    return 3



# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.

def better_evaluate(board):
    if board.is_tie():
        #if the game is tie
        score = 0
    elif board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -2000 - (42 - board.num_tokens_on_board())
    else:
        heuristic = [0]
        result=predict_win(board, heuristic)
        h = heuristic[0]
        if(result==1): #predicted win
            score = 1000 + (42 - board.num_tokens_on_board())
        elif(result==2): #predicted lose
            score =  -1000 - (42 - board.num_tokens_on_board())
        elif(result==3): #unsure
            score = board.longest_chain(board.get_current_player_id()) * 10
            # # Prefer having your pieces in the center of the board.
            # for row in range(6):
            #     for col in range(7):
            #         if board.get_cell(row, col) == board.get_current_player_id():
            #             score -= abs(3-col)
            #         elif board.get_cell(row, col) == board.get_other_player_id():
            #             score += abs(3-col)
            
            #available (not sealed) blocks heuristic
            #count the num of my available blocks
            #count the num of opponent available blocks
            #get net diff = my available blocks - opponent available blocks
            score+=h
    return score


# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(focused_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)


# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=8)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
