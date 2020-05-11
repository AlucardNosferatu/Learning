public class Zerozaki{
	String name="";
	Zerozaki CP=null;
	int score=0;
	String mood="";
	Boolean life=true;
	int suicide_countdown=5;
	public Zerozaki(String name,Zerozaki CP){
		this.name=name;
		this.CP=CP;
		}
	public static void main(String[]args){
		Zerozaki Senshiki=new Zerozaki("Senshiki",null);
		Zerozaki Renshiki=new Zerozaki("Renshiki",Senshiki);
		Senshiki.CP=Renshiki;
		Senshiki.ScoreEffect((int) Math.random()*100);
		Renshiki.MoodEffect(Renshiki.CP);
		if(Renshiki.suicide_countdown==0)
			Renshiki.suicide(Renshiki);
		if(Renshiki.life)
			narrow_door.enter=true;
		}
	public void ScoreEffect(int score){
		this.score=score;
		if(score<=60)
			System.out.println("显然不可能。");
		else if(score<=70)
			this.mood="非常糟糕";
		else if(score<=80)
			this.mood="很糟糕";
		else if(score<=90)
			this.mood="不太开心";
		else if(score<=95)
			this.mood="一般般";
		else if(score<=99)
			this.mood="还算可以";
		else if(score<=100)
			this.mood="较满意";
		else if(score==100)
			this.mood="开心";
		}
	public void MoodEffect(Zerozaki Senshiki){
		this.mood=Senshiki.mood;
		switch(this.mood){
		case "非常糟糕":
			this.farewell(Senshiki);
			if(this.farewell(Senshiki))
			this.suicide(this);
			break;
		case "很糟糕":
			this.comfort(Senshiki);
			this.hate(this);
			break;
		case "不太开心":
			this.comfort(Senshiki);
			this.hate(this);
			break;
		case "一般般":
			this.cheerup(Senshiki);
			this.criticize(this);
			break;
		case "还算可以":
			this.cheerup(Senshiki);
			this.criticize(this);
			break;
		case "较满意":
			this.encourage(Senshiki);
			this.comfort(this);
			break;
		case "开心":
			this.encourage(Senshiki);
			this.comfort(this);
			break;
		default:
			break;
			}
		}
	public Boolean farewell(Zerozaki Senshiki){
		Boolean last_index=true;
		if(this.life){
			if(this.fate()){
				last_index=true;
			}
			else
				last_index=false;
		}
		return last_index;
	}
	public void comfort(Zerozaki Senshiki){
		if(this.life){
			if(this.fate()){
				Senshiki.mood="非常糟糕";
			}
			else
				Senshiki.mood="不太开心";
		}
	}
	public void cheerup(Zerozaki Senshiki){
		if(this.life){
			if(this.fate()){
				Senshiki.mood="很糟糕";
			}
			else
				Senshiki.mood="一般般";
		}		
	}
	public void encourage(Zerozaki Senshiki){
		if(this.life){
			if(this.fate()){
				Senshiki.mood="不太开心";
			}
			else
				Senshiki.mood="还算可以";
			}
		}		
	public void castdown(Zerozaki Renshiki){
		if(this.life){
			if(this.fate()){
				this.suicide_countdown--;
				}
			else
				return;
			}
		}
	public void criticize(Zerozaki Renshiki){
		if(this.life){
			if(this.fate()){
				this.suicide_countdown-=2;
				}
			else
				return;
			}
		}
	public void hate(Zerozaki Renshiki){
		if(this.life){
			if(this.fate()){
				this.suicide_countdown-=3;
				}
			else
				return;
			}
		}
	public void suicide(Zerozaki Renshiki){
		if(this.life)
			if(this.fate())
				this.wrist_cutting(this);
			else
				return;
		if(this.life)
			if(this.fate())
				this.gas_poison(this);
			else
				return;
		if(this.life)
			if(this.fate())
				this.jump_off_a_building(this);
			else
				return;	
	}
	public void wrist_cutting(Zerozaki Renshiki){
		Boolean knife=false;
		if(this.fate())
			knife=true;
		if(knife)
			this.life=false;
		else
			return;
		}
	public void gas_poison(Zerozaki Renshiki){
		Boolean gas_cylinder=false;
		if(this.fate())
			gas_cylinder=true;
		if(gas_cylinder)
			this.life=false;
		else
			return;
		}
	public void jump_off_a_building(Zerozaki Renshiki){
		Boolean building=false;
		if(this.fate())
			building=true;
		if(building)
			this.life=false;
		else
			return;
		}
	public Boolean fate(){
		Boolean death=true;
		if(Math.random()*100>=75)
		death=false;
		return death;
		}
	}
class narrow_door{
	static Boolean enter=false;
}
