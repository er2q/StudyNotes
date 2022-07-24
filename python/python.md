### 1.`python`变量
- 受保护的实例属性用单个下划线开头（后面会讲到）。
- 私有的实例属性用两个下划线开头（后面会讲到）。

### 2.元组

1.元组中的元素是无法修改的

2.元组在创建时间和占用的空间上面都优于列表

> **Note**
>
> 我们可以使用`sys`模块的`getsizeof`函数来检查存储同样的元素的元组和列表各自占用了多少内存空间，这个很容易做到。我们也可以在`ipython`中使用魔法指令`%timeit`来分析创建同样内容的元组和列表所花费的时间。

![image-20220627112425900](python.assets/image-20220627112425900.png)

### 3.同步\异步and阻塞\非阻塞（重点）

#### 同步:

>**Note**
>
>所谓同步，就是在发出一个功能调用时，在没有得到结果之前，该调用就不会返回。按照这个定义，其实绝大多数函数都是同步调用。但是一般而言，我们在说同步、异步的时候，特指那些需要其他部件协作或者需要一定时间完成的任务。
>
>```python
>#1. multiprocessing.Pool下的apply #发起同步调用后，就在原地等着任务结束，根本不考虑任务是在计算还是在io阻塞，总之就是一股脑地等任务结束
>#2. concurrent.futures.ProcessPoolExecutor().submit(func,).result()
>#3. concurrent.futures.ThreadPoolExecutor().submit(func,).result()
>```

#### 异步：

>**Note**
>
>异步的概念和同步相对。当一个异步功能调用发出后，调用者不能立刻得到结果。当该异步功能完成后，通过状态、通知或回调来通知调用者。如果异步功能用状态来通知，那么调用者就需要每隔一定时间检查一次，效率就很低（有些初学多线程编程的人，总喜欢用一个循环去检查某个变量的值，这其实是一 种很严重的错误）。如果是使用通知的方式，效率则很高，因为异步功能几乎不需要做额外的操作。至于回调函数，其实和通知没太多区别。
>
>```python
>#举例：
>#1. multiprocessing.Pool().apply_async() #发起异步调用后，并不会等待任务结束才返回，相反，会立即获取一个临时结果（并不是最终的结果，可能是封装好的一个对象）。
>#2. concurrent.futures.ProcessPoolExecutor(3).submit(func,)
>#3. concurrent.futures.ThreadPoolExecutor(3).submit(func,)
>```

#### 阻塞：

> **Note**
>
> 阻塞调用是指调用结果返回之前，当前线程会被挂起（如遇到io操作）。函数只有在得到结果之后才会将阻塞的线程激活。有人也许会把阻塞调用和同步调用等同起来，实际上他是不同的。对于同步调用来说，很多时候当前线程还是激活的，只是从逻辑上当前函数没有返回而已。
>
> ```python
> #举例：
> #1. 同步调用：apply一个累计1亿次的任务，该调用会一直等待，直到任务返回结果为止，但并未阻塞住（即便是被抢走cpu的执行权限，那也是处于就绪态）;
> #2. 阻塞调用：当socket工作在阻塞模式的时候，如果没有数据的情况下调用recv函数，则当前线程就会被挂起，直到有数据为止。
> ```

#### 非阻塞：

> **Note**
>
> 非阻塞和阻塞的概念相对应，指在不能立刻得到结果之前也会立刻返回，同时该函数不会阻塞当前线程。

#### 小结：

1. 同步与异步针对的是函数/任务的调用方式：同步就是当一个进程发起一个函数（任务）调用的时候，一直等到函数（任务）完成，而进程继续处于激活状态。而异步情况下是当一个进程发起一个函数（任务）调用的时候，不会等函数返回，而是继续往下执行当，函数返回的时候通过状态、通知、事件等方式通知进程任务完成。

2. 阻塞与非阻塞针对的是进程或线程：阻塞是当请求不能满足的时候就将进程挂起，而非阻塞则不会阻塞当前进程

### 4.僵尸进程与孤儿进程

参考博客：http://www.cnblogs.com/Anker/p/3271773.html

一：僵尸进程（有害）
　　**僵尸进程：一个进程使用fork创建子进程，如果子进程退出，而父进程并没有调用wait或waitpid获取子进程的状态信息，那么子进程的进程描述符仍然保存在系统中。这种进程称之为僵死进程**。详解如下

我们知道在unix/linux中，正常情况下子进程是通过父进程创建的，子进程在创建新的进程。子进程的结束和父进程的运行是一个异步过程,即父进程永远无法预测子进程到底什么时候结束，如果子进程一结束就立刻回收其全部资源，那么在父进程内将无法获取子进程的状态信息。

因此，UNⅨ提供了一种机制可以保证父进程可以在任意时刻获取子进程结束时的状态信息：
1、在每个进程退出的时候，内核释放该进程所有的资源，包括打开的文件，占用的内存等。但是仍然为其保留一定的信息（包括进程号the process ID，退出状态the termination status of the process，运行时间the amount of CPU time taken by the process等）
2、直到父进程通过wait / waitpid来取时才释放. 但这样就导致了问题，如果进程不调用wait / waitpid的话，那么保留的那段信息就不会释放，其进程号就会一直被占用，但是系统所能使用的进程号是有限的，如果大量的产生僵死进程，将因为没有可用的进程号而导致系统不能产生新的进程. 此即为僵尸进程的危害，应当避免。

　　任何一个子进程(init除外)在exit()之后，并非马上就消失掉，而是留下一个称为僵尸进程(Zombie)的数据结构，等待父进程处理。这是每个子进程在结束时都要经过的阶段。如果子进程在exit()之后，父进程没有来得及处理，这时用ps命令就能看到子进程的状态是“Z”。如果父进程能及时 处理，可能用ps命令就来不及看到子进程的僵尸状态，但这并不等于子进程不经过僵尸状态。  如果父进程在子进程结束之前退出，则子进程将由init接管。init将会以父进程的身份对僵尸状态的子进程进行处理。

二：孤儿进程（无害）

　　**孤儿进程：一个父进程退出，而它的一个或多个子进程还在运行，那么那些子进程将成为孤儿进程。孤儿进程将被init进程(进程号为1)所收养，并由init进程对它们完成状态收集工作。**

　　孤儿进程是没有父进程的进程，孤儿进程这个重任就落到了init进程身上，init进程就好像是一个民政局，专门负责处理孤儿进程的善后工作。每当出现一个孤儿进程的时候，内核就把孤 儿进程的父进程设置为init，而init进程会循环地wait()它的已经退出的子进程。这样，当一个孤儿进程凄凉地结束了其生命周期的时候，init进程就会代表党和政府出面处理它的一切善后工作。因此孤儿进程并不会有什么危害。

我们来测试一下（创建完子进程后，主进程所在的这个脚本就退出了，当父进程先于子进程结束时，子进程会被init收养，成为孤儿进程，而非僵尸进程），文件内容

```python
import os
import sys
import time

pid = os.getpid()
ppid = os.getppid()
print 'im father', 'pid', pid, 'ppid', ppid
pid = os.fork()
#执行pid=os.fork()则会生成一个子进程
#返回值pid有两种值：
#    如果返回的pid值为0，表示在子进程当中
#    如果返回的pid值>0，表示在父进程当中
if pid > 0:
    print 'father died..'
    sys.exit(0)

# 保证主线程退出完毕
time.sleep(1)
print 'im child', os.getpid(), os.getppid()

执行文件，输出结果：
im father pid 32515 ppid 32015
father died..
im child 32516 1
```

看，子进程已经被pid为1的init进程接收了，所以僵尸进程在这种情况下是不存在的，存在只有孤儿进程而已，孤儿进程声明周期结束自然会被init来销毁。


三：僵尸进程危害场景：

　　**例如有个进程，它定期的产 生一个子进程，这个子进程需要做的事情很少，做完它该做的事情之后就退出了，因此这个子进程的生命周期很短，但是，父进程只管生成新的子进程，至于子进程 退出之后的事情，则一概不闻不问，这样，系统运行上一段时间之后，系统中就会存在很多的僵死进程，倘若用ps命令查看的话，就会看到很多状态为Z的进程。 严格地来说，僵死进程并不是问题的根源，罪魁祸首是产生出大量僵死进程的那个父进程。因此，当我们寻求如何消灭系统中大量的僵死进程时，答案就是把产生大 量僵死进程的那个元凶枪毙掉（也就是通过kill发送SIGTERM或者SIGKILL信号啦）。枪毙了元凶进程之后，它产生的僵死进程就变成了孤儿进 程，这些孤儿进程会被init进程接管，init进程会wait()这些孤儿进程，释放它们占用的系统进程表中的资源，这样，这些已经僵死的孤儿进程 就能瞑目而去了。**

四：测试

```python
#1、产生僵尸进程的程序test.py内容如下

#coding:utf-8
from multiprocessing import Process
import time,os

def run():
    print('子',os.getpid())

if __name__ == '__main__':
    p=Process(target=run)
    p.start()

    print('主',os.getpid())
    time.sleep(1000)


#2、在unix或linux系统上执行
[root@vm172-31-0-19 ~]# python3  test.py &
[1] 18652
[root@vm172-31-0-19 ~]# 主 18652
子 18653

[root@vm172-31-0-19 ~]# ps aux |grep Z
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root     18653  0.0  0.0      0     0 pts/0    Z    20:02   0:00 [python3] <defunct> #出现僵尸进程
root     18656  0.0  0.0 112648   952 pts/0    S+   20:02   0:00 grep --color=auto Z

[root@vm172-31-0-19 ~]# top #执行top命令发现1zombie
top - 20:03:42 up 31 min,  3 users,  load average: 0.01, 0.06, 0.12
Tasks:  93 total,   2 running,  90 sleeping,   0 stopped,   1 zombie
%Cpu(s):  0.0 us,  0.3 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  1016884 total,    97184 free,    70848 used,   848852 buff/cache
KiB Swap:        0 total,        0 free,        0 used.   782540 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND                                                                                                                                        
root      20   0   29788   1256    988 S  0.3  0.1   0:01.50 elfin                                                                                                                      


#3、
```

>等待父进程正常结束后会调用wait／waitpid去回收僵尸进程
>
>但如果父进程是一个死循环，永远不会结束，那么该僵尸进程就会一直存在，僵尸进程过多，就是有害的
>
>**解决方法一**：杀死父进程
>
>**解决方法二**：对开启的子进程应该记得使用join，join会回收僵尸进程
>
>参考python2源码注释

```python
class Process(object):
    def join(self, timeout=None):
        '''
        Wait until child process terminates
        '''
        assert self._parent_pid == os.getpid(), 'can only join a child process'
        assert self._popen is not None, 'can only join a started process'
        res = self._popen.wait(timeout)
        if res is not None:
            _current_process._children.discard(self)
```

> join方法中调用了wait，告诉系统释放僵尸进程。discard为从自己的children中剔除
>
> **解决方法三**：http://blog.csdn.net/u010571844/article/details/50419798

> #答案：可以
>
> #分析：
>
> p.join()是像操作系统发送请求，告知操作系统p的id号不需要再占用了，回收就可以，
>
> 此时在父进程内还可以看到p.pid,但此时的p.pid是一个无意义的id号，因为操作系统已经将该编号回收
>
> 打个比方：
>
> 我党相当于操作系统，控制着整个中国的硬件，每个人相当于一个进程，每个人都需要跟我党申请一个身份证号
>
> 该号码就相当于进程的pid，人死后应该到我党那里注销身份证号，p.join()就相当于要求我党回收身份证号，但p的家人（相当于主进程）
>
> 仍然持有p的身份证，但此刻的身份证已经没有意义

### 5.守护进程

> 1.什么时候将进程设置为守护进程？
>
> 当子进程执行的任务在父进程代码运行完毕后就没有存在的必要了，那该子进程就应该被设置为守护进程。
>
> 其一：守护进程会在主进程代码执行结束后就终止
>
> 其二：守护进程内无法再开启子进程,否则抛出异常：AssertionError: daemonic processes are not allowed to have children
>
> 注意：进程之间是互相独立的，主进程代码运行结束，守护进程随即终止
