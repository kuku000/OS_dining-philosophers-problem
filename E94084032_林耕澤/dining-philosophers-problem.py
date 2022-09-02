import threading
import random
import time

 #繼承執行緒—哲學家的class
class Philosopher(threading.Thread):
    #確認大家是不是都吃了
    running = True  

    def __init__(self, index, chopstick_Left, chopstick_Right):
        threading.Thread.__init__(self)
        self.index = index
        self.chopstick_Left = chopstick_Left
        self.chopstick_Right = chopstick_Right

    def run(self):
        while(self.running):
            #哲學家在思考
            time.sleep(5)
            print ('Philosopher'+str(self.index)+' is hungry.' )
            self.dine()

    def dine(self):
        # 如果兩邊筷子沒人用哲學家就會吃 
        chopstick1, chopstick2 = self.chopstick_Left, self.chopstick_Right
        while self.running:
            #acquire左邊的筷子
            chopstick1.acquire(True) 
            locked = chopstick2.acquire(False)
            #如果右邊的筷子被locked的話,就把左邊的筷子也放回去 
            if locked: break 
            chopstick1.release()
            print ('Philosopher'+str(self.index)+ ' swaps chopsticks.')
            chopstick1, chopstick2 = chopstick2, chopstick1
        else:
            return
        self.dining()
        #吃完飯後把兩邊筷子都放回去
        chopstick2.release()
        chopstick1.release()
 
    def dining(self):			
        print ('Philosopher' +str(self.index)+' starts eating. ')
        time.sleep(10)
        print ( 'Philosopher'+str(self.index)+' finishes eating and leaves to think.')

def main():
    #初始化Semaphore—共五支筷子
    chopsticks = [threading.Semaphore() for n in range(5)] 
    print('total chopsticks :',len(chopsticks))
    #初始化哲學家LIST一共五個哲學家（1～5號）每個哲學家會拿起他右手邊的筷子和左手邊的筷子
    philosophers= [Philosopher(i, chopsticks[i%5], chopsticks[(i+1)%5])
            for i in range(1,6)]
    print('total philosophers :',len(philosophers))
    #random.seed(2105)
    Philosopher.running = True
    for i in philosophers: i.start()
    time.sleep(50)
    Philosopher.running = False
    print ("finishing.")
   


main()

