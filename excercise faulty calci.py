print("enter 1st no")
no1 = int(input())
print("enter 2nd no")
no2 = int(input())
print("which u want to select from this * / - +")
sym = input()
if sym == "*":
    if no1 == 45 and no2 == 3:
        print("555")
    else:
        print(no1*no2)   
elif sym == "+":
    if no1 == 56 and no2 == 9:
        print("77")
    else:
        print(no1+no2) 
elif sym == "-":
    print (no1-no2)
elif sym == "/":
    if no1 == 56 and no2 ==6:
        print("4")
    else:
        print(no1/no2)
else:
    print("enter valid oprator")    
   
