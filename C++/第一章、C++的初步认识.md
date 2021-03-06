### 第一章、C++的初步认识

### 1.2最简单的C++程序

#### 1.1 输出一行字符串："This is a C++ program."。

##### 源程序

```c++
// 输出一行字符串："This is a C++ program."。

#include<iostream>				// 包含头文件iostream

using namespace std;			// 使用C++的命名空间std

int main()
{
	cout << "This is a C++ program." << endl;
	return 0;
}
```

##### 输出

```C+++
This is a C++ program.
```

##### 注

标准`C++`规定`main`函数**必须**声明为`int`型，即此主函数返回一个整型的函数值。

#### 1.2 求a和b两个数之和

##### 源程序

```c++
// 求a和b两个数之和

#include<iostream>							// 预处理指令

using namespace std;						// 使用命名空间std
			
int main()									// 主函数首部
{											// 函数体开始
	int a, b, sum;							// 定义变量
	cin >> a >> b;							// 输入变量a和b的值
	sum = a + b;							// 赋值语句
	cout << "a + b = " << sum << endl;		// 输出语句
	return 0;								// 如果程序正常结束，向操作系统返回一个零值
}											// 函数结束
```

##### 输出

![image-20220327163238076](1.2最简单的C++程序\image-20220327163238076.png)

##### 注

在`C++`新标注中，使用不带后缀`.h`的头文件，**标准库中的类和函数都在“命名空间`std`”中声明。**因此，如果程序中包含了新形式的头文件(无后缀的头文件，如：`iostream`)，必须使用`using namespace std;`。

#### 1.3 给定两个数x和y，求两个数中的最大值

##### 源程序

```
// 给定两个数x和y，求两个数中的最大值
#include<iostream>						// 预处理指令

using namespace std;

int max(int x, int y)					// 定义max函数，函数值为整型，形式参数x，y为整型
{										// max函数体开始
	if (x > y)							// if语句，如果x>y，返回x
		return x;				
	else                                // 否则返回y
	{
		return y;
	}
}

int main()								// 主函数
{										// 主函数开始
	int x, y, m;						// 变量声明
	cin >> x >> y;						// 输入变量a和b的值
	m = max(x, y);						// 调用max函数，将得到的值赋给m
	cout << "max = " << m << endl;		// 输出大数m的值
	return 0;							// 如果程序正常结束，向操作系统返回一个零值
}										// 主函数结束
```

##### 输出

![image-20220327165036246](1.2最简单的C++程序\image-20220327165036246.png)

#### 1.4 包含类的C++程序

##### 源程序

```
// 包含类的C++程序
#include<iostream>									// 预处理指令

using namespace std;

class Student										// 声明一个类，类名为Student
{
public:												// 以下为类中公用部分
	void setdata()									// 定义公用函数setdata
	{
		cin >> num;									// 输入num的值
		cin >> score;								// 输入score的值
	}
	void display()									// 定义公用函数display
	{
		cout << "num = " << num << endl;			// 输出num的值
		cout << "score = " << score << endl;		// 输出score的值
	}

private:											// 以下为类的私有部分，
	int num;										// 私有变量num
	int score;										// 私有变量score
};													// 类的声明结束

Student stud1, stud2;								// 定义stud1和stud2为Student类的变量，称为对象

int main()											// 主函数首部
{
	stud1.setdata();								// 调用stud1的setdata函数
	stud2.setdata();
	stud1.display();
	stud2.display();
	return 0;
}
```

##### 输出

![image-20220327173320509](1.2最简单的C++程序\image-20220327173320509.png)

