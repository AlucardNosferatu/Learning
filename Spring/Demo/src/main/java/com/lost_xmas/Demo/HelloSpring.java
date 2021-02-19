package com.lost_xmas.Demo;
public class HelloSpring {
    private String Msg;
    public void setMsg(String message){
        this.Msg  = message;
    }

    public void getMsg(){
        System.out.println(this.Msg);
    }

    public void start(){
        System.out.println("We fell in love in 2016");
    }

    public void death(){
        System.out.println("Even death won't separate us.");
//        Only Singleton Will Call This During Shutdown
    }
}