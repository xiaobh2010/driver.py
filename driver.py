from signal import *
from multiprocessing import Process
import os,time

def saler_handler(sig,frame):
    if sig==SIGINT:
        #这是在子进程中所以是获取父进程号
        os.kill(os.getppid(),SIGUSR1)
    elif sig==SIGQUIT:
        os.kill(os.getppid(),SIGUSR2)
    elif sig==SIGUSR1:
        print('到站了,下车吧')
        os._exit(0)

def driver_handler(sig,frame):
    #在父进程中
    if sig==SIGUSR1:
        print('老司机开车了')
    elif sig==SIGUSR2:
        print('系好安全带，小心')
    elif sig==SIGTSTP:
        os.kill(p.pid,SIGUSR1)

def saler():
    signal(SIGINT,saler_handler)
    signal(SIGQUIT,saler_handler)
    signal(SIGUSR1,saler_handler)
    signal(SIGTSTP,SIG_IGN)
    signal(SIGUSR2,SIG_IGN)

    while True:
        time.sleep(2)
        print('在路上．．．')

#主进程一般只做创建进程的流程控制
p=Process(name='zhangjie',target=saler)

#创建子进程
p.start()

#父进程处理信号部分
signal(SIGUSR1,driver_handler)
signal(SIGUSR2,driver_handler)
signal(SIGTSTP,driver_handler)
signal(SIGINT,SIG_IGN)
signal(SIGQUIT,SIG_IGN)

#保证子进程退出之后父进程才退出
p.join()
