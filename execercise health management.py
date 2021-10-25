print("enter name : ")
name = input()
if name == 'HARSH':
    print("Enter 1 to write what you eat.\nEnter 2 to write what execercise you do.")
    no = int(input())
    if no == 1:
        try:
            h = open("HARSH EAT.txt","x")
            print("enter what you eat\n")
            eat = input()
            h = open("HARSH EAT.txt","a")
            h.write(eat)
            h.close
        except Exception as file :
            print("enter what you eat\n")
            eat = input()
            h = open("HARSH EAT.txt","a")
            h.write(eat)
            h.close
    elif no==2:
        try:
            h = open("HARSH execercise.txt","x")
            print("enter which execercise you do.\n")
            eat = input()
            h = open("HARSH execercise.txt","a")
            h.write(eat)
            h.close
        except Exception as file :
            print("enter which execercise you do.\n")
            eat = input()
            h = open("HARSH execercise.txt","a")
            h.write(eat)
            h.close
elif name == 'NIKUNJ':
    print("Enter 1 to write what you eat.\nEnter 2 to write what execercise you do")
    no = int(input())
    if no == 1:
        try:
            h = open("NIKUNJ EAT.txt","x")
            print("enter what you eat\n")
            eat = input()
            h = open("NIKUNJ EAT.txt","a")
            h.write(eat)
            h.close
        except Exception as file :
            print("enter what you eat\n")
            eat = input()
            h = open("NIKUNJ EAT.txt","a")
            h.write(eat)
            h.close
    elif no==2:
        try:
            h = open("NIKUNJ execercise.txt","x")
            print("enter what you eat\n")
            eat = input()
            h = open("NIKUNJ execercise.txt","a")
            h.write(eat)
            h.close
        except Exception as me :
            print("enter which execercise you do\n")
            eat = input()
            h = open("NIKUNJ execercise.txt","a")
            h.write(eat)
            h.close
elif  name == 'YASH':
    print("Enter 1 to write what you eat.\nEnter 2 to write what execercise you do")
    no = int(input())
    if no == 1:
        try:
            h = open("YASH EAT.txt","x")
            print("enter what you eat\n")
            eat = input()
            h = open("YASH EAT.txt","a")
            h.write(eat)
            h.close
        except Exception as file :
            print("enter what you eat\n")
            eat = input()
            h = open("YASH EAT.txt","a")
            h.write(eat)
            h.close
    elif no==2:
        try:
            h = open("YASH execercise.txt","x")
            print("enter which execercise you do\n")
            eat = input()
            h = open("YASH execercise.txt","a")
            h.write(eat)
            h.close
        except Exception as me :
            print("enter which execercise you\n")
            eat = input()
            h = open("YASH execercise.txt","a")
            h.write(eat)
            h.close
else :
    print("Enter name of HARSH , NIKUNJ or YASH only")


