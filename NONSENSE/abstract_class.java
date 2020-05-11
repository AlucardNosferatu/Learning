 abstract class Person_0{
	private String name;
	private int age;
	public Person_0(String name,int age){
		this.name=name;
		this.age=age;
		}
	public String getName(){
		return name;
		}
	public int getAge(){
		return age;
		}
	public void say(){
		System.out.println(this.getContent());
	}
	public abstract String getContent();
	}
class Student extends Person_0{
	private float score;
	public Student(String name,int age,float score){
		super(name,age);
		this.score=score;
	}
	public String getContent(){
		return "学生信息-->姓名："+super.getName()+"；年龄："+super.getAge()+"；成绩："+this.score;
	}
}
class Worker extends Person_0{
	private float salary;
	public Worker(String name, int age,float salary) {
		super(name, age);
		this.salary=salary;
		}
	public String getContent() {
		return "工人信息-->姓名："+super.getName()+"；年龄："+super.getAge()+"；工资："+this.salary;
		}
	}
public class abstract_class {
	public static void main(String[]args){
		Person_0 per1=null;
		Person_0 per2=null;
		per1=new Student("苗木诚",18,75.0f);
		per2=new Worker("哀川润",28,90000.0f);
		per1.say();
		per2.say();
		}
	}
