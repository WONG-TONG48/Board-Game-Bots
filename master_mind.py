import math
import asyncio
import time

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

async def analyse_pos(posibilties,current_item):
    probabilities = []
    for l in pos_outcoms:
        num_matches = 0
        for k in posibilties:
            if matches(current_item,l,k):
                num_matches += 1
        if num_matches != 0:
            probabilities.append(num_matches / total_num)
    num = 0
    for l in probabilities:
        num += l * math.log2(1/l)
    return num,current_item

async def run_funcs(num,posibilties):
    return await asyncio.gather(*(analyse_pos(posibilties,posibilties[i]) for i in range(num,num+min(50,len(posibilties)-num))))

async def main(posibilties):
    return await asyncio.gather(*(run_funcs(i,posibilties) for i in range(0,len(posibilties),50)))

best_starter = ['R','Br','Bl','Y','Br']
outcome = int(input('How many whites? ')), int(input('How many blacks? '))
posibilties = []
for k in pos_cobs:
    if matches(best_starter,outcome,k):
        posibilties.append(k)
print(math.log2(1 / (len(posibilties) / total_num)))
turn = 0
while len(posibilties) > 0:
    turn += 1
    highest_bits = (0,0)
    old_precent = 0
    pos_len = len(posibilties)
    try:
        start_time = time.time()
        for i in asyncio.run(main(posibilties)):
            for num in i:
                if num[0] > highest_bits[0]:
                    highest_bits = num
                    print(*highest_bits)
        print(time.time() - start_time)
    except KeyboardInterrupt:
        pass
    print(highest_bits[1])
    outcome = int(input('How many whites? ')), int(input('How many blacks? '))
    for k in pos_cobs:
        if k in posibilties:
            if not matches(highest_bits[1],outcome,k):
                posibilties.remove(k)
    print(math.log2(1 / (len(posibilties) / total_num)))

        

    
