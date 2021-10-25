list1 = ["harsh",18,"yash",19,"nikunj",19,"sahil",17]

#for item,age in list1:
 #   print(age ,"is the age of", item)

for item in list1:
    if str(item).isnumeric() and item>18:
        print(item)