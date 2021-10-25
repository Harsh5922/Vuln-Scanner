h=10#global
def fun1(n):
    # h=9#local
    #if we want to change golbel var then we have to write global variabel name
    global h
    h = h +10
    print(h)
    print(n,h)
fun1("2")

x=89
def harsh():
    x = 20 
    def nik():
        global x
        x=88
    # print("before calling nik",x)
    nik()
    print("after calling nik",x)
harsh()
print(x)