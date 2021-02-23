package com.lost_xmas.Demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Required;

public class HelloString {
    private String Hello;

    public HelloString(String H){
        this.Hello=H;
    }
//    @Required
    public void setHello(String H){
        this.Hello=H;
    }
    public String getHello(){
        return this.Hello;
    }
}
