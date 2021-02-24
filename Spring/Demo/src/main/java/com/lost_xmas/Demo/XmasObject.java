package com.lost_xmas.Demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;

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

    @Autowired
    @Qualifier("xmas_string2")
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
