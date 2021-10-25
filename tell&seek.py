f=open("any.txt")
# print(f.tell())
print(f.readline())
f.seek(14) #reset the filepointer
# print(f.tell())
print(f.readline())
# print(f.tell())
f.close()