import math
import pyautogui as pag
import time
import numpy as np

cols = ['G','R','Bl','Br','W','O','Y','Bk']
x = [831, 902, 974, 1066, 1132]
y = {'Bl':464, 'G':433, 'R':393, 'O':356, 'Br':301, 'Bk':269, 'W':236, 'Y':192}
y2 = [905, 865, 827, 789, 745, 704, 669]
x2 = (600, 726)

pos_cobs = []
for i in cols:
    for j in cols:
        for k in cols:
            for t in cols:
                for l in cols:
                    pos_cobs.append([i,j,k,t,l])
total_num = len(pos_cobs)

pos_outcoms = []
for i in range(6):
    for l in range(6 - i):
        pos_outcoms.append((i,l))
pos_outcoms.remove((4,1))

def enter_code(code):
    for i in range(5):
        pag.click(x[i],y[code[i]])

def matches(comb,outcome,guess):
    comb = comb[:]
    guess = guess[:]
    whites = 0
    temp = []
    for i,j,l in zip(comb,guess,range(5)):
        if i == j:
            whites += 1
            temp.append(l)
    if whites != outcome[0]:
        return False
    for j,i in enumerate(temp):
        comb.pop(i - j)
        guess.pop(i - j)
    blacks = 0
    for j,i in enumerate(comb):
        if i in guess and guess[j] != i:
            blacks += 1
            for l,k in enumerate(guess):
                if k == i:
                    guess[l] = ' '
                    break
    if blacks != outcome[1]:
        return False
    return True

def get_score(turn):
    ss = pag.screenshot(region=(640,y2[turn],126,1))
    ss = np.array(ss)
    blacks = 0
    whites = 0
    for i in range(5):
        col = list(ss[0][i*31])
        if col == [0,0,0]:
            blacks += 1
        elif col == [252,252,252]:
            whites += 1
    return blacks,whites
    

best_starter = ['R','Br','Bl','Y','Br']
pag.click(1050, 1050)
pag.click(385, 376)
time.sleep(0.4)
enter_code(best_starter)
posibilties = []
outcome = get_score(0)
for k in pos_cobs:
    if matches(best_starter,outcome,k):
        posibilties.append(k)
print(math.log2(1 / (len(posibilties) / total_num)))
turn = 0
while len(posibilties) > 0:
    turn += 1
    highest_bits = (0,0)
    temp1 = 0
    old_precent = 0
    pos_len = len(posibilties)
    start_time = time.time()
    try:
        for i in posibilties:
            probabilities = []
            temp1 += 1
            if temp1*100//pos_len > old_precent:
                old_precent = temp1*100//pos_len
                if time.time() - start_time > 10:
                    raise KeyboardInterrupt
            for l in pos_outcoms:
                num_matches = 0
                for k in posibilties:
                    if matches(i,l,k):
                        num_matches += 1
                if num_matches != 0:
                    probabilities.append(num_matches / total_num)
            num = 0
            for l in probabilities:
                num += l * math.log2(1/l)
            if num > highest_bits[0]:
                highest_bits = (num,i)
                print(*highest_bits)
    except KeyboardInterrupt:
        pass
    print(highest_bits[1])
    enter_code(highest_bits[1])
    outcome = get_score(turn)
    for k in pos_cobs:
        if k in posibilties:
            if not matches(highest_bits[1],outcome,k):
                posibilties.remove(k)
    print(math.log2(1 / (len(posibilties) / total_num)))

        

    
