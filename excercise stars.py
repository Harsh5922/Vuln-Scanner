a=int(input("enter no : "))
b=int(input("enter 1 or 0 : "))
c=bool(b)
if c==True:
    for i in range(1,a+1):
        for j in range(1,i+1):
            print("*",end="")
        print()
