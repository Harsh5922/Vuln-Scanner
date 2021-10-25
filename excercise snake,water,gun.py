import random
l = ["snake","water","gun"]
i = 0
Y = 0
C = 0
while(i<10):
    a = random.choice(l) 
    print("enter S-snake , W-water , G-gun")
    b=input()
    if b == 'S':
        if a == 'gun':
            print("comp - gun & you - snake")
            print("result - you lose ")
            C = C+1
        if a == 'water':
            print("comp - water & you -snake")
            print("result - you win")
            Y = Y+1
        if a == 'snake':
            print("comp - snake & you -snake")
            print("result - draw")
    if b == 'W':
        if a == 'gun':
            print("comp - gun & you - water")
            print("result - you win")
            Y = Y+1
        if a == 'water':
            print("comp - water & you - water")
            print("result - draw")
        if a == 'snake':
            print("comp - snake & you - water")
            print("result - you lose")
            C = C+1
    if b == 'G':
        if a == 'gun':
            print("comp - gun & you - gun")
            print("result - draw ")
        if a == 'water':
            print("comp - water & you - gun")
            print("result - you lose")
            C = C+1
        if a == 'snake':
            print("comp - snake & you - gun")
            print("result - you win")
            Y=Y+1
    print("game remaining",9-i) 
    i=i+1
    print("computer's score is",C)
    print("your score is",Y)       
