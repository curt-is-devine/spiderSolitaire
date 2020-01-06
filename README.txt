GUI = more user friendly

Things learned:
	global variables in python
	text formatting of print statements
	copying 2-D arrays in python
	error testing/importing other files in python

Hangups:
	Testing values of cards. checking a-2, 9-t, t-j, etc. At first
		I was testing the values directly, but then I created 
		the hash map and that greatly helped the confusion
	was validating the move in 3 locations for legibility (one to 
		check inputs, one to check the moving column, and one 
		to check final column, but it was wasteful timewise, so 
		I condensed the three functions
	Started off with a lot of the functions as methods instead of 
		functions. Had to change once I got to the help option 
		to avoid overwriting the game board and data/storage 
		overhead
	LOTS of array indexing problems and +- problems considering 
		array layout and taking from end of array as opposed to 
		beginning
	The algorithm for detecting a loop was a pain in the butt
Ideas:
	working backward in these arrays is not the most intuitive/efficient.
		but then again, if i were to work from the front there 
		would be a lot of overhead. If i had the arrays set up in reverse 
		order, I would want to look at python's behind the scenes to 
		see the amount of overhead that may result in (obviously logically)
		this works easier for me, but technically it may not due to
		memory allocation of python arrays)
	If I kept a "bottom stacks" array globally, would this eliminate some 
		of the time overhead of availableMoves()/isComplete()?
	Hint option: "if lastCard == "XX"": Could go further with this by only allowing
			the tops of stacks to be moved or adding a DFS search 
			for the other stacks for a better help option
	Add an undo option

The A.I. algorithm for "hint":
	From observation/real experience, there is an endless loop whenever the same number
		of moves exists after a move and the same child cards are involved. But this is not
		necessarily the condition that needs met to be in this situation. Example: a stack
		from K-3 of Diamonds, a stack of K-3 of Spades, and then children on these stacks of 
		2-A of Clubs and 2-A of Hearts, with another stack having a 5 of any suit. My initial 
		idea was that I can just use a greedy approach to stacks, where you dont want to split 
		them up, that way if the random 5 is a Club or Heart, then the A.I. would not want to 
		split up that stack, and would be stuck in the more common loop condition described 
		above. However the problem still exists if the suit of that 5 is Diamond or Spade. 
		My next idea was that moves from a card of one suit to the exact same card would 
		be useless and the game may be able to ignore this. But in order for the game to weed 
		those moves out, a DFS of depth two would be needed. 
	Attempting to weed out suggestions that just infinitely loop.

	Three possibilities after moving a stack:
		1. The number of available moves increases
		2. The number of available moves decreases
		3. The number of available moves remains the same
	for each of these possibilities in move numbers, the moves themselves
	also fall into categories:
		1. Move an entire bottom stack
		2. Move from inside of a bottom stack
		3. Move results in a free column
		4. Move to a free column
	Available moves can only increase in cases 1 and 3. 1 specifically when multiple stacks/substacks can move to the parent
		and/or the parent can move to multiple locations
	Available moves can only decrease in cases 4 and 1. 1 specifically when a child's move blocks n moves and the parent
		only has n moves to/from it (since the move of the child counts as a move as well, need a net loss of moves).
	Available moves stay the same in all cases, but 3 and 4 in extreme cases where multiple columns are free and there are
		few available cards to move. Case 1 when moving to/from parents with the same values or when the child's movement 
		blocks as many moves as the parent can make/receive + 1. 2 will stay the same by identity of the split in the
		stack. 

	Observation: If the child has n available moves,
		at least n - 1 of those moves still exist after moving, 
		(n if the bottom of the parent is the same as that the stack moves to)
	Observation: After a move, the parent can only have new moves available TO IT 
		if the child is out of order. If not, then whatever the child moved to had
		the same possible moves as the parent now does and there is no net gain in 
		available moves (or loss). 
	Observation: A loop can only exist if the card being moved (child) is part of a loop 
		condition. There must be at least two parents that can keep trading the child back and forth.
		If multiple such child/parent pairs exist, then the loops can still be weeded out in this way.
		For cards that can only move to an open column and back to the same spot again, this is still 
		the case. Easiest to see loop conditions if all other available cards have been moved and only
		looping moves are left.
	Observation: When the game is in a perpetual loop state, no new moves are being added, as the stack is 
		just being passed around
