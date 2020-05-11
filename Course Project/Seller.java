package CourseProject;

	import java.awt.Dimension;
	import java.awt.Toolkit;
	import java.awt.event.ActionEvent;
	import java.awt.event.ActionListener;
	import javax.swing.JButton;
	import javax.swing.JFrame;
	import javax.swing.JLabel;
	import javax.swing.JOptionPane;
	import javax.swing.JPasswordField;
	import javax.swing.JTextField;
	public class Seller{
		public static void main(String[] args) {	
			final String userName = "seller";		
			final String passwrod = "123456";	
			JFrame jFrame = new JFrame("销售员登陆界面");
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


