package com.lost_xmas.Demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HelloFactory {

    @Bean
    public HelloFactory anotherFactory(){
        HelloFactory HF=new HelloFactory();
        return HF;
    }

    @Bean
    public HelloString stringFactory(){
        HelloString HS=new HelloString("I hope I can see her in the flesh someday.");
        return HS;
    }

    @Bean
    public HelloSpring springFactory(){
        HelloSpring HS=new HelloSpring();
        return HS;
    }

    @Bean
    public HelloSpringJr springJrFactory(){
        HelloSpringJr HSJ=new HelloSpringJr();
        return HSJ;
    }
}
