# def fact_itretive(n):
#     fac=1
#     for i in range(n):
#         fac = fac * (i+1)
#     return fac

# num = int(input("enter the number"))
# print(fact_itretive(num))

# def fact_recursive(n):
#    if n == 1:
#        return 1
#    else:
#        return n * fact_recursive(n-1)

num = int(input("enter the number"))
# print(fact_itretive(num))



def fibonacci(n):
    if n==1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
print(fibonacci(num))