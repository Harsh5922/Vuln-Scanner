b = 16
g=1
print("this is a game of guess the no\n you have to guess no in 5 moves \n")
while(g<=5):
    print("enter no you guess")
    a = int(input())
    if (a>20):
        print("plz enter no b/w 0 to 20\n")
    elif(a>b):
        print("your no is grater\n")
    elif(a<b):
        print("your no is smaller\n")
    else:
        print("you won")
        break
    print(5-g,"no of guesses left")
    g=g+1
    if(g>5):
        print("game over")
