package com.lost_xmas.Demo;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
public class MainApp {
    public static void main(String[] args) {
        System.out.println("用户的当前工作目录:"+System.getProperty("user.dir"));
        ApplicationContext context =
                new ClassPathXmlApplicationContext("./Beans.xml");
        HelloSpring obj = (HelloSpring) context.getBean("HelloSpring");
        obj.getMessage();
    }
}
