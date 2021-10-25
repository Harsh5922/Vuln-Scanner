import time
initial = time.time()
for i in range(20):
    print(i)
    time.sleep(1)
print(f"time to run for loop is {time.time()-initial}")