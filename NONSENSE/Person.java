public class Person {
	String name;
	int age;
	static String default_name="Name";
	static int default_age=0;
	public Person(String Name,int Age){
		name=Name;
		age=Age;
	}
	public void tell(){
		System.out.println("姓名："+name+"，年龄："+age);
	}
	public static void main(){
		System.out.println("成功");
	}
}
class ClassDemo03{
	public static void main(String[]args){//参数为形参名为args的字符串数组？有什么用？
		Person per1=new Person("Name1",1);//静态初始化
		Person per2=null;//动态初始化
		per2=new Person(null,0);
		per2.name="Name2";
		per2.age=2;
		per1.tell();
		per2.tell();
		System.out.println(Person.default_name+Person.default_age);//尝试不实例化类调用静态变量
		Person.main();//尝试不实例化类调用静态方法以及多main方法【结论：程序只会运行唯一public类的main】
	}
}
//引用数据类型都可以先声明到null再另外用new开辟内存空间
