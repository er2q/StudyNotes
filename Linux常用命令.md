#### linux复制文件夹中前N个文件
```
ls |head -n N|xargs -i cp {} /home/autoware/workplace
```
> N 是文件个数
