
import random

def my_random(keys,weights):
    list = []
    for i in range(len(weights)):
        for num in range(weights[i]):
            list.append(keys[i])

    j = random.randint(0,len(list)-1)
    return list[j]

    
#for i in range(10):
    #print(my_random(keys=['a','b','c'],weights = [1,1,2]))
    

def my_sum(*args,value = 1):
    '''Add Value To Numbers'''
    list = []
    for i in args:
        list.append(i+value)
    return list

#print(my_sum(10,10,9,3,5,5,4,6,4))

def get_my_counter():
    x = -1
    def inner(y = 1):
        nonlocal x
        x += y
        return x
    return inner

my_counter = get_my_counter()
print(my_counter())
print(my_counter())
print(my_counter())
