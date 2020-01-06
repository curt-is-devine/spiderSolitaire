import Spider

Spider.fullDeck = ["AH", "2H", '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', \
        "AD", "2D", '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', \
        "AC", "2C", '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', \
        "AS", "2S", '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'] * 2

Spider.halfDeck = ["AD", "2D", '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', \
        "AS", "2S", '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'] * 4
            
Spider.easyDeck = ["AS", "2S", '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'] * 8

Spider.vals = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13, '1':1} #Added '1' for column testing


Spider.difficulty = 'H'
Spider.completed = [] #completed suits
Spider.score = 500
Spider.stack = []
Spider.board = [["AS", "AS", "AS"] for i in range(10)]
Spider.free = [2 for i in range(10)]

#dealRow validateMove()------------------------------------------------------------------------------------
print("Testing validateMove():")

print("validateMove() when the column input does not work")
card = "AS"
for col1 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    for col2 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if col1 == "T" and col2 == "T":
            assert Spider.validateMove(Spider.board, Spider.free, Spider.difficulty, col1, card, col2) == True
        else:
            assert Spider.validateMove(Spider.board, Spider.free, Spider.difficulty, col1, card, col2) == False
assert Spider.validateMove(Spider.board, Spider.free, Spider.difficulty, "TT", card, "2") == False
assert Spider.validateMove(Spider.board, Spider.free, Spider.difficulty, "2", card, "TT") == False