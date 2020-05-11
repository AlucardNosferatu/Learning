package CourseProject;

import javax.swing.JFrame;//框架
import javax.swing.JOptionPane;
import javax.swing.JPanel;//面板
import javax.swing.JButton;//按钮
import javax.swing.JLabel;//标签
import javax.swing.JTextField;//文本框
import java.awt.Dimension;
import java.awt.Font;//字体
import java.awt.Color;//颜色
import java.awt.Toolkit;
import javax.swing.JPasswordField;//密码框
import java.awt.event.ActionListener;//事件监听
import java.awt.event.ActionEvent;//事件处理
import javax.swing.*;

public class Login extends JFrame {
	public JPanel pnluser;
	public JLabel lbluserLogIn;
	
	
	public JButton btn_m;
	public JButton btn_n;
	public JButton btn_t;
	
	public ButtonGroup bg;

	public Login() {
		pnluser = new JPanel();
		lbluserLogIn = new JLabel();
		
		
		btn_m = new JButton();
		btn_n = new JButton();
		btn_t = new JButton();
		
		
		userInit();
	}

	public void userInit() {
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);// 设置关闭框架的同时结束程序
		this.setSize(500, 300);// 设置框架大小为长300,宽200
		this.setResizable(false);// 设置框架不可以改变大小
		this.setTitle("恭喜发财Apple销售系统");// 设置框架标题
		this.pnluser.setLayout(null);// 设置面板布局管理
		this.pnluser.setBackground(Color.cyan);// 设置面板背景颜色
		this.lbluserLogIn.setText("请选择您要执行的操作");// 设置标签标题
		this.lbluserLogIn.setFont(new Font("宋体", Font.BOLD | Font.ITALIC, 20));// 设置标签字体
		this.lbluserLogIn.setForeground(Color.BLACK);// 设置标签字体颜色
		
		this.btn_m.setText("管理员");
		this.btn_n.setText("销售员");
		this.btn_t.setText("用户");
		this.lbluserLogIn.setBounds(100, 45, 280, 20);// 设置标签x坐标120,y坐标15,长60,宽20
		
		

	
		this.btn_m.setBounds(145, 120, 100, 40);
		this.btn_m.addActionListener(new ActionListener()// 匿名类实现ActionListener接口
				{
					public void actionPerformed(ActionEvent e) {
						btn_m_ActionEvent(e);
					}
				});
		this.btn_n.setBounds(145, 160, 100, 40);
		this.btn_n.addActionListener(new ActionListener()// 匿名类实现ActionListener接口
				{
					public void actionPerformed(ActionEvent e) {
						btn_n_ActionEvent(e);
					}
				});
		this.btn_t.setBounds(145, 200, 100, 40);
		this.btn_t.addActionListener(new ActionListener()// 匿名类实现ActionListener接口
				{
					public void actionPerformed(ActionEvent e) {
						btn_n_ActionEvent(e);
					}
				});
		this.pnluser.add(lbluserLogIn);
		this.pnluser.add(btn_m);
		this.pnluser.add(btn_n);
		this.pnluser.add(btn_t);
		
		this.add(pnluser);// 加载面板到框架
		this.setVisible(true);// 设置框架可显
	}


	public void btn_m_ActionEvent(ActionEvent e) {
		if(e.getSource()==btn_m){
			   this.setVisible(false);
			   new Manager();}
	}
	public void btn_n_ActionEvent(ActionEvent e) {
		if(e.getSource()==btn_n){
			   this.setVisible(false);
			   new Seller();}
	}
	public void btn_t_ActionEvent(ActionEvent e) {
		if(e.getSource()==btn_t){
			   this.setVisible(false);
			   new Guest();}
	}
	 class Manager extends JFrame{
		 Manager(){
			 final String userName = "manager";		
	  			final String passwrod = "123456";	
	  			JFrame jFrame = new JFrame("管理员登陆界面");	
	  			Dimension dimension = Toolkit.getDefaultToolkit().getScreenSize();	
	  			jFrame.setBounds(((int)dimension.getWidth() -1350) / 2, ((int)dimension.getHeight() -600) / 2, 280, 250);	
	  			jFrame.setResizable(false);		
	  			jFrame.setLayout(null);	
	  			jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);		
	  			JLabel label1 = new JLabel("管理员用户名");		
	  			label1.setBounds(40, 50, 100, 30);	
	  			jFrame.add(label1);				
	  			JLabel label2 = new JLabel("管理员密码");	
	  			label2.setBounds(40, 80, 100, 30);		
	  			jFrame.add(label2);			
	  			final JTextField text1 = new JTextField();	
	  			text1.setBounds(140, 55, 130, 20);	
	  			jFrame.add(text1);	
	  			final JPasswordField text2 = new JPasswordField();		
	  			text2.setBounds(140, 85, 130, 20);	
	  			jFrame.add(text2);				
	  			JButton button = new JButton("登陆");		
	  			button.setBounds(40, 125, 170, 40);		
	  			button.addActionListener(new ActionListener() {		
	  				@Override			
	  				public void actionPerformed(ActionEvent e) {
	  					if(userName.equals(text1.getText()) && passwrod.equals(text2.getText())) {	
	  						
	  						JOptionPane.showMessageDialog(null, "登陆成功", "提示", JOptionPane.INFORMATION_MESSAGE);
	  						
	  						this.dispose();//点击按钮时frame1销毁,new一个frame2..
	  						
	  						new guanliyuan(); // }}frame2是个单纯的界面
	  					
	  						} 
	  					
	  					else {					JOptionPane.showMessageDialog(null, "输入错误", "提示", JOptionPane.ERROR_MESSAGE);		
	  					text1.setText("");				
	  					text2.setText("");		
	  					}			
	  					}

					private void dispose() {
						// TODO Auto-generated method stub
						
					}		});		
	  			jFrame.add(button);	
	  						jFrame.setVisible(true);
	  				}		
	  						 
	  						
	  						
	  							}
	 class Seller extends JFrame{
		 Seller(){final String userName = "seller";		
			final String passwrod = "123456";	
			JFrame jFrame = new JFrame("销售员登陆界面");	//JFrame是一个类，具有
			Dimension dimension = Toolkit.getDefaultToolkit().getScreenSize();	
			jFrame.setBounds(((int)dimension.getWidth() - 200) / 2, ((int)dimension.getHeight() - 300) / 2, 300, 250);	
			jFrame.setResizable(false);		
			jFrame.setLayout(null);	
			jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);		
			JLabel label1 = new JLabel("销售员用户名");		
			label1.setBounds(50, 50, 100, 30);	
			jFrame.add(label1);				
			JLabel label2 = new JLabel("销售员密码");	
			label2.setBounds(50, 80, 100, 30);		
			jFrame.add(label2);			
			final JTextField text1 = new JTextField();	
			text1.setBounds(140, 55, 130, 20);	
			jFrame.add(text1);	
			final JPasswordField text2 = new JPasswordField();		
			text2.setBounds(140, 85, 130, 20);	
			jFrame.add(text2);				
			JButton button = new JButton("登陆");		
			button.setBounds(70, 125, 170, 40);		
			button.addActionListener(new ActionListener() {		
				@Override			
				public void actionPerformed(ActionEvent e) {
					if(userName.equals(text1.getText()) && passwrod.equals(text2.getText())) {	
						
						JOptionPane.showMessageDialog(null, "登陆成功", "提示", JOptionPane.INFORMATION_MESSAGE);				} else {					JOptionPane.showMessageDialog(null, "错误", "提示", JOptionPane.ERROR_MESSAGE);					text1.setText("");					text2.setText("");				}			}		});		jFrame.add(button);	
						jFrame.setVisible(true);
	}}

	  	
	  	
	    

	public static void main(String[] args) {
		new Login();
	}
}
