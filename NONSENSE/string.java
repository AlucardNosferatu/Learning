public class string {
public String string_0,string_1;
public char[] char_array_0,char_array_1;
public string(){
String string_0="abcd";//字符串abcd
char[] char_array_0=string_0.toCharArray();//字符数组abcd
String string_1=new String(char_array_0);//字符串abcd
char[] char_array_1={string_1.charAt(0)};//字符a
byte[] byte_array_0=string_1.getBytes();
}
public static void main(String[]args){
string strObject_0=new string();
int int_0=strObject_0.string_1.length();
int int_1=strObject_0.string_1.indexOf("a");
String string_2=strObject_0.string_1.substring(0,3);
strObject_0.method_0();
}
public void method_0(){
System.out.println(this);
}
}
