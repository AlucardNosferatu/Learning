package com.lost_xmas.Demo;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
//import org.springframework.beans.factory.InitializingBean;
//import org.springframework.beans.factory.xml.XmlBeanFactory;
//import org.springframework.core.io.ClassPathResource;

public class MainApp {
    public static void main(String[] args) {
        System.out.println("用户的当前工作目录:"+System.getProperty("user.dir"));
//        ApplicationContext context = new ClassPathXmlApplicationContext("./Beans.xml");
        AbstractApplicationContext context = new ClassPathXmlApplicationContext("./Beans.xml");
        HelloSpring obj = (HelloSpring) context.getBean("HS_0");
//        HelloSpringJr objJr = (HelloSpringJr) context.getBean("HSJ_0");
//        XmlBeanFactory XBF = new XmlBeanFactory((new ClassPathResource("Beans.xml")));
//        HelloSpring obj = (HelloSpring) XBF.getBean("HS_0");
//        obj.getMsg();
//        obj.setMsg("She Is My Angel!!!");
//        obj = (HelloSpring) XBF.getBean("HS_0");
        obj.getMsg();
//        objJr.getMsg();
//        objJr.getCode();
        context.registerShutdownHook();
    }
}
