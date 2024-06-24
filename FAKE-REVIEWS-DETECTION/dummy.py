result = list(range(100))
count = 0
def recommends(r):
    global count
    
    if count % 5 == 0:
        print(r[count:count + 5])
    count += 5


click  = 0 
while click<20:
    recommends(result)
    click+=1