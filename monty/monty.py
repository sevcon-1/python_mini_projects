import random as rand

def door():
    return rand.randint(1,3)

rounds = int(input("Enter number of rounds: "))
print(f"Playing {rounds} ... \n")

stick_you_win = 0
switch_you_lose = 0
switch_you_win = 0
stick_you_lose = 0

#TODO: Add timeit to see what happens moving the dict out.

for i in range(rounds):
    guess = door()
    car = door()

    #print(f"guess is door {guess} car is behind {car}")
    if guess == car:
        stick_you_win += 1
        switch_you_lose += 1
    else:
        stick_you_lose += 1
        switch_you_win += 1

    outcomes = {
        'stick_you_win': stick_you_win, 
        "stick_you_lose": stick_you_lose,
        "switch_you_lose": switch_you_lose, 
        "switch_you_win": switch_you_win
    }

for k,v in outcomes.items():
    print(k,v)
