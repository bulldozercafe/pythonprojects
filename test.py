import random

a=random.randint(2,9)
b=random.randint(2,9)
ask=-1

while(ask!=(a*b)):
    ask=input('%d*%d='%(a,b))
    print(ask)
    print((a*b))
    print(ask == (a*b))
    print(ask != (a * b))

print('Yes! The answer is %d!'%ask)
