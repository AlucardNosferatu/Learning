package com.lost_xmas.Demo;

import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.beans.BeansException;

public class InitHelloSpring implements BeanPostProcessor{
    public Object postProcessBeforeInitialization(Object beanObj, String beanName) throws BeansException{
        if(beanName.equals("HS_0")){
            HelloSpring HS=(HelloSpring)beanObj;
            System.out.println("BeforeInit.");
            return HS;
        }
        return beanObj;
    }
    public Object postProcessAfterInitialization(Object beanObj, String beanName) throws BeansException{
        if(beanName.equals("HS_0")){
            HelloSpring HS=(HelloSpring)beanObj;
            System.out.println("AfterInit.");
            return HS;
        }
        return beanObj;
    }

}
