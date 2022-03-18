# 一、什么事Celery
## 1.1、celery是什么
> Celery是一个简单、灵活且可靠的、处理大量消息的分布式系统，专注于实时处理的异步任务队列，同时也支持任务调度。

![img](readme.assets/2522678-d369b6a4c4265225.png)

> Celery的框架有三部分组成，消息中间件（message broker），任务执行单元（worker）和任务执行结果存储（task result store）组成。

**消息中间件**

Celery本身不提供消息服务，但是可以方便的和第三方提供的消息中间件集成。包括，RabbitMQ, Redis等等

**任务执行单元**

Worker是Celery提供的任务执行的单元，worker并发的运行在分布式的系统节点中。



**任务结果存储**

Task result store用来存储Worker执行的任务的结果，Celery支持以不同方式存储任务的结果，包括AMQP, redis等

另外， Celery还支持不同的并发和序列化的手段

- 并发：Prefork, Eventlet, gevent, threads/single threaded
- 序列化：pickle, json, yaml, msgpack. zlib, bzip2 compression， Cryptographic message signing 等等

## 1.2、使用场景

celery是一个强大的 分布式任务队列的异步处理框架，它可以让任务的执行完全脱离主程序，甚至可以被分配到其他主机上运行。我们通常使用它来实现异步任务（async task）和定时任务（crontab)。

异步任务：将耗时操作任务提交给Celery去异步执行，比如发送短信/邮件、消息推送、音视频处理等等

定时任务：定时执行某件事情，比如每天数据统计

## 1.3、Celery具有一下优点

> Simple(简单)
> Celery 使用和维护都非常简单，并且不需要配置文件。
>
> Highly Available（高可用）
> woker和client会在网络连接丢失或者失败时，自动进行重试。并且有的brokers 也支持“双主”或者“主／从”的方式实现高可用。
>
> Fast（快速）
> 单个的Celery进程每分钟可以处理百万级的任务，并且只需要毫秒级的往返延迟（使用 RabbitMQ, librabbitmq, 和优化设置时）
>
> Flexible（灵活）
> Celery几乎每个部分都可以扩展使用，自定义池实现、序列化、压缩方案、日志记录、调度器、消费者、生产者、broker传输等等。

