package com.lost_xmas.Demo;
public class HelloSpring {
    private String Msg;
    public void setMessage(String message){
        this.Msg  = message;
    }
    public void getMessage(){
        System.out.println("Your Message : " + this.Msg);
    }
}