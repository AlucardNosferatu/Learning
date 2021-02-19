package com.lost_xmas.Demo;

public class HelloSpringJr {
    private int Code;
    private String Msg;

    public void setCode(int C)
    {
        this.Code=C;
    }

    public void getCode(){
        System.out.println(this.Code);
    }

    public void setMsg(String message){
        this.Msg  = message;
    }

    public void getMsg(){
        System.out.println(this.Msg);
    }

    public void start(){
        System.out.println("Sometimes I might get distracted by sth else.");
    }

    public void death(){
        System.out.println("She is the only one who never give me up.");
    }
}
