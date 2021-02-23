package com.lost_xmas.Demo;

public class XmasObject {
    private int Year;

    private String Name;

    private HelloSpring HS;

//    public XmasObject(HelloSpring H){
//        this.HS=H;
//        System.out.println("New XO."+this.HS.getMsg());
//    }

    public void setYear(int Y){
        this.Year=Y;
    }

    public void setName(String N){
        this.Name=N;
    }

    public int getYear(){
        return this.Year;
    }

    public String getName(){
        return this.Name;
    }
}
