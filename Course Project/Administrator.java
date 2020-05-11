package CourseProject;
import java.awt.*;  
import java.awt.event.*; 
import java.sql.Connection; 
import java.sql.DriverManager; 
import java.sql.PreparedStatement; 
import java.sql.ResultSet; 
import java.sql.Statement; 
import java.sql.*; 
import javax.swing.JOptionPane; 
public class Administrator extends Frame implements ActionListener 

{  

	Label name=new Label("产品名称："); 
    TextField t1=new TextField(); 
    Label num=new Label("销售数量："); 
    TextField t2=new TextField();  
    Label cost=new Label("产品进价："); 
    TextField t3=new TextField(); 
    Label price=new Label("产品售价："); 
    TextField t4=new TextField(); 
    Label profits=new Label("产品利润："); 
    TextField t5=new TextField();  
    Label stock=new Label("剩余库存："); 
    TextField t6=new TextField(); 
    Button b1=new Button("添加"); 
    Button b2=new Button("查询"); 
    Button b3=new Button("修改"); 
    Button b4=new Button("删除"); 
    Button b5=new Button("关闭"); 
    public Administrator() 

    {  

       

    	this.setTitle("管理员操作界面");//设置窗口标题
         this.setLayout(null);  
         name.setBounds(50,40,60,20);  
         this.add(name);// 将姓名标签组件添加到容器
         t1.setBounds(120,40,80,20);// 设置文本框的初始位置
         this.add(t1);// 将文本框组件添加到容器
         num.setBounds(50,100,90,20); 
         this.add(num);  
         t2.setBounds(120,100,80,20); 
         this.add(t2);  
         cost.setBounds(50,160,60,20); 
         this.add(cost);  
         t3.setBounds(120,160,80,20); 
         this.add(t3);  
         price.setBounds(50,220,60,20); 
         this.add(price);  
         t4.setBounds(120,220,80,20); 
         this.add(t4);  
         profits.setBounds(50,280,60,20); 
         this.add(profits);  
         t5.setBounds(120,280,80,20); 
         this.add(t5);  
         stock.setBounds(50,340,60,20); 
         this.add(stock);  
         t6.setBounds(120,340,80,20); 
         this.add(t6);  
                 b1.setBounds(15,390,60,20);// 设置添加按钮的初始位置
                 this.add(b1);// 将登陆按钮组件添加到容器
                 b1.addActionListener(this);//   给添加按钮添加监听器
                 b2.setBounds(85,390,60,20);//   设置添加按钮的初始位置
                 this.add(b2);// 将登陆按钮组件添加到容器
                 b2.addActionListener(this);//  给添加按钮添加监听器
                 b3.setBounds(155,390,60,20);//  设置添加按钮的初始位置
                 this.add(b3);//将登陆按钮组件添加到容器
                 b3.addActionListener(this);//给
                 b4.setBounds(225,390,60,20);//设置添加按钮的初始位置
                 this.add(b4);//将登陆按钮组件添加到容器
                 b4.addActionListener(this);//给
                 b5.setBounds(120,450,60,20);//设置添加按钮的初始位置
                 this.add(b5);//将登陆按钮组件添加到容器
                 b5.addActionListener(this);//给添加按钮添加监听器
                 this.setVisible(true);//设置窗口的可见性
                 this.setSize(300,500);//设置窗口的大小
                 addWindowListener(new WindowAdapter() 
                 {     public void windowClosing(WindowEvent e) {  System.exit(0); }  });//通过内部类重写关闭窗体的方法
            }  
            public void actionPerformed(ActionEvent e) {//0 
         if(e.getSource()==b1){  //boolean b=true; 
         String url="jdbc:odbc:shujuku"; 
         try{
         Statement  stmt; 
         PreparedStatement psmt;                                   
         ResultSet rs;                                     
         Class.forName("sun.jdbc.odbc.JdbcOdbcDriver");    
         Connection con=DriverManager.getConnection(url); 
                        //con=DriverManager.getConnection(url);  
         stmt=con.createStatement(); 

         String name=t1.getText(); 
         String number=t2.getText();       
         String cost=t3.getText(); 
         String price=t4.getText(); 
         String profits=t5.getText(); 
         String stock=t6.getText();  
    
         psmt=con.prepareStatement("insert  into 学生信息表values('"+name+"','"+number+"','"+cost+"','"+price+"','"+profits+"','"+stock+"')"); 
         rs=psmt.executeQuery(); 
           con.close(); 
         }catch (Exception e1) { 
         e1.printStackTrace();   
         } 
        String warning=" 已录入！ ";// 必须在   try catch 之后
        JOptionPane.showMessageDialog(null,warning, "提示",JOptionPane.WARNING_MESSAGE); 
         } 

         if(e.getSource()==b2){//1 
         //boolean b=true; 
         try{//3 
         String url="jdbc:odbc:shujuku"; 
         Statement stmt;
         PreparedStatement psmt; 
         ResultSet rs;
         Class.forName("sun.jdbc.odbc.JdbcOdbcDriver"); 
            Connection con=DriverManager.getConnection(url); 
            psmt=con.prepareStatement("select  *  from 学生信息表 where  学号='"+t2.getText()+"'");  
                   rs=psmt.executeQuery(); 
                   rs.next();
         t1.setText(rs.getString(1)); 
         t2.setText(rs.getString(2)); 
         t3.setText(rs.getString(3)); 
         t4.setText(rs.getString(4)); 
         t5.setText(rs.getString(5)); 
         t6.setText(rs.getString(6)); 
                 }catch (Exception e2) { 

                 e2.printStackTrace();   
                 } 

         }  
                 if(e.getSource()==b3){//4 
         String mz=t1.getText(); 
         String xl=t2.getText(); 
         String jj=t3.getText(); 
         String sj=t4.getText(); 
         String lr=t5.getText();             
         String kc=t6.getText(); 
         try{ 
        Class.forName("sun.jdbc.odbc.JdbcOdbcDriver"); 
        Connection  con =DriverManager.getConnection("jdbc:odbc:shujuku"); 
        Statement stmt = con.createStatement();       
                               String sql="update 仓库存储表set 产品='"+mz+"' 销量='"+xl+"', 进价 ='"+jj+"',售价='"+sj+"',利润='"+lr+" where 库存='"+kc+"'";  
                              int n=stmt.executeUpdate(sql); 
        } 
         catch(Exception e3){ 
         e3.printStackTrace();   
         }  
         String warning=" 已成功修改该产品信息";//显示已成功删除
        JOptionPane.showMessageDialog(null,warning,"提  示   ",JOptionPane.WARNING_MESSAGE);                  } 
                 else if(e.getSource()==b4)// 处理删除事件
         { 
         try { 
        Class.forName("sun.jdbc.odbc.JdbcOdbcDriver"); 
        Connection con = 
        DriverManager.getConnection("jdbc:odbc:shujuku"); 
        String sql="delete from 学生信息表where 学号='"+t2.getText()+"'";//删除学生信息 
        }  
         catch (Exception e4) { 
        e4.printStackTrace();  
        } 
         String warning="已成功删除该产品信息";//  显示已成功删除
        JOptionPane.showMessageDialog(null,warning," 提示",JOptionPane.WARNING_MESSAGE); 
         }   
                 if(e.getSource()==b5)//判断语句
                    {  
                        dispose(); 
        } 
         }  
        public static void main(String args[])//主函数
        {              new Administrator(); 

        }}          
