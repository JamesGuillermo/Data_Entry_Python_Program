import time
def linear_algo(num):
    for i in range(num):
        print(end="")

def quadratic_algo(num):
    for i in range(num):
        for j in range(num):
            print(end="")

num = 100
start = time.time()
linear_algo(num)
print("Linear time:", time.time() - start)

start = time.time()
quadratic_algo(num)
print("Quadratic time:", time.time() - start) 
