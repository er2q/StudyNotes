### MySQL修改、设置密码
```angular2html
use mysql; 
 
update user set authentication_string='' where user='root';--将字段置为空
 
ALTER user 'root'@'localhost' IDENTIFIED BY 'root';--修改密码为root
```