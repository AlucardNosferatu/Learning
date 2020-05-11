import java.util.Scanner;
public class game {
	public String text;
	public String text_0;
	public String text_1;
	public String text_2;
	Scanner input=new Scanner(System.in);
	public game(String Text,String Text_0,String Text_1,String Text_2){
		text=Text;
		text_0=Text_0;
		text_1=Text_1;
		text_2=Text_2;
	}
	public void read(Boolean Read){
		if(Read)
			System.out.println(text);
	}
	
	public void choose(int choice){
		switch(choice){
		case 1:
			text_0=text_1;
			break;
		case 2:
			text_0=text_2;
			break;
		default:
			break;
		}
		
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		game Game=new game("你要作死吗？","1.作死.2.不作.","人作死，就会死","不作死，不会死");
		Game.read(true);
	}

}
