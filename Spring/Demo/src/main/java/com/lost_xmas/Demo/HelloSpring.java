package com.lost_xmas.Demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Required;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import javax.annotation.Resource;

public class HelloSpring {

    private HelloString Msg;
    private XmasObject Xmas;

//    public HelloSpring(XmasObject X){
//        this.Xmas=X;
////        System.out.println(this.Xmas.getName());
//    }


    @Required
    public void setMsg(HelloString message){
//        System.out.println("Setting Msg...");
        this.Msg  = message;
    }

    public HelloString getMsg(){
//        System.out.println(this.Msg.getHello());
//        System.out.println(this.Xmas.getName());
        return Msg;
    }

    @Resource(name="var4")
//    @Qualifier("var4")
    public void setXmas(XmasObject X){
        this.Xmas=X;
    }

    @Resource(name="var3")
//    @Qualifier("var3")
    public void setXmas2(XmasObject X){
        this.Xmas=X;
    }

    public XmasObject getXmas(){
        return this.Xmas;
    }

    @PostConstruct
    public void fellInLove(){
        System.out.println("We fell in love in 2016");
    }

    @PreDestroy
    public void restTogether(){
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