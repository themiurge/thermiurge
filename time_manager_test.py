import time_manager as tm

tm.set_sim(tm.now())

start = tm.now()
print(start)

def timer_test(a, b, c, n1='zio', n2='cane'):
    print (a, b, c, n1, n2)

t = tm.Timer(2.0, timer_test, [1, 2, 3], { 'n2' : 'porco' })
t.start()
t2 = tm.Timer(1.0, timer_test, [1, 2, 3], { 'n1' : 'mio' })
t2.start()
#for i in range(10):
#    print (i+1)
#    tm.wait(1.0)
tm.wait(10.0)

print((tm.now() - start).total_seconds(), "seconds elapsed")
