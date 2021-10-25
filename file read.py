""" 
"r"- open file for reading - default
"w"- open a file for writing
"x"- create file if not exists
"a"- add more content to a file
"t"- text mode - default
"b"- binary mode
"+"-read and write
"""
z = open("any.txt")
# print(z.readline())
#  print(z.readlines())
# t = z.read(3)
# for line in z:
#     print(line)
# # print(t)
z.close()