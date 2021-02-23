package com.lost_xmas.Demo;
public class HelloSpring {
    private String Msg;

    private XmasObject Xmas;

    public HelloSpring(XmasObject X){
        this.Xmas=X;
        System.out.println(this.Xmas.getName());
    }

    public void setMsg(String message){
        System.out.println("Setting Msg...");
        this.Msg  = message;
    }

    public String getMsg(){
        System.out.println(this.Msg);
        return Msg;
    }

    public void setXmas(XmasObject X){
        this.Xmas=X;
    }

    public XmasObject getXmas(){
        return this.Xmas;
    }
    public void start(){
        System.out.println("We fell in love in 2016");
    }

    public void death(){
        System.out.println("Even death won't separate us.");
//        Only Singleton Will Call This During Shutdown
    }
}

//1.Constructor
//2.Setter
//3.BeforeInit
//4.InitMethod
//5.AfterInit
//6.UsingObject
//7.DestroyMethod