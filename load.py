import pickle

def save(score):
    with open('highscore.dat', 'wb') as file:
        pickle.dump(score, file)

def load():
    with open('highscore.dat', 'rb') as file:
        try:
            highscore = pickle.load(file)
        except EOFError:
            highscore = 0
    return highscore


