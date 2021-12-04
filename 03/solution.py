with open('input.txt') as f:
    rows=f.readlines()

L=len(rows[0])-1   #1 because the last char is newline
gammaRate=[0]*L
epsilonRate=[0]*L
gamma=0
epsilon=0
for r in rows:
    for i in range(L):
        gammaRate[i] += int(r[i])
for i in range(L):
    if 2*gammaRate[i]>len(rows):
        gammaRate[i]=1
    else:
        gammaRate[i]=0
    epsilonRate[i]=1-gammaRate[i]
    
for i in range(L):
    gamma += gammaRate[i]*(2**(L-i-1))
    epsilon += epsilonRate[i]*(2**(L-i-1))    

print(gamma*epsilon)

L=len(rows[0])-1   #1 because the last char is newline
oxygen=0
allowed=[True] * len(rows)
for j in range(L):
    counts=[0,0]
    for i,r in enumerate(rows):
        if allowed[i]:
            counts[int(r[j])]+=1
    throw=0
    if counts[0]>counts[1]:
        throw=1
    for i,r in enumerate(rows):
        if int(r[j])==throw:
            allowed[i]=False
for i,r in enumerate(rows):
    if allowed[i]==True:
        oxygenBin=r
               
carbon=0
allowed=[True] * len(rows)
for j in range(L):
    counts=[0,0]
    for i,r in enumerate(rows):
        if allowed[i]:
            counts[int(r[j])]+=1
    throw=1
    if counts[0]>counts[1]:
        throw=0
    for i,r in enumerate(rows):
        if int(r[j])==throw:
            allowed[i]=False
    countAllowed=0
    for i,r in enumerate(rows):
        if allowed[i]:
            carbonBin=r
            countAllowed +=1
    if countAllowed==1:
        break        
            
for i in range(L):
    oxygen += int(oxygenBin[i])*(2**(L-i-1))
    carbon += int(carbonBin[i])*(2**(L-i-1))    

print(oxygen*carbon)


