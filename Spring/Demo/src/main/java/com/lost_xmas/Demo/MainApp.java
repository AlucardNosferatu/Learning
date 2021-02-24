package com.lost_xmas.Demo;

import org.springframework.context.ApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
//import org.springframework.beans.factory.InitializingBean;
//import org.springframework.beans.factory.xml.XmlBeanFactory;
//import org.springframework.core.io.ClassPathResource;

public class MainApp {
    public static void main(String[] args) {
//        System.out.println("用户的当前工作目录:"+System.getProperty("user.dir"));
//        AbstractApplicationContext context = new ClassPathXmlApplicationContext("./Beans.xml");
        ConfigurableApplicationContext class_context = new AnnotationConfigApplicationContext(HelloFactory.class);
//        HS.setMsg(class_context.getBean(HelloString.class));
//        HS.getMsg().setHello("I Love Carol!");
        class_context.start();
        class_context.stop();
        HelloSpring HS = class_context.getBean(HelloSpring.class);
        HelloPublisher HP = (HelloPublisher) class_context.getBean("publisherFactory");
        HP.SayHi();
        System.out.println(HS.getMsg().getHello());
//        HelloSpring obj = (HelloSpring) context.getBean("HS_0");
//        HelloString Msg=(HelloString) context.getBean("HelloString");
//        HelloSpringJr objJr = (HelloSpringJr) context.getBean("HSJ_0");
//        XmlBeanFactory XBF = new XmlBeanFactory((new ClassPathResource("Beans.xml")));
//        HelloSpring obj = (HelloSpring) XBF.getBean("HS_0");
//        obj.getMsg();
//        obj.setMsg("She Is My Angel!!!");
//        obj = (HelloSpring) XBF.getBean("HS_0");
//        System.out.println(obj.getMsg().getHello());
//        System.out.println(obj.getXmas().getName());
//        objJr.getMsg();
//        objJr.getCode();
        class_context.registerShutdownHook();
    }
}
