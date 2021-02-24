package com.lost_xmas.Demo;

import org.springframework.context.ApplicationListener;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.event.ContextStartedEvent;
import org.springframework.context.event.ContextStoppedEvent;

@Configuration
public class HelloHandler{

    public class HelloStartContext implements ApplicationListener<ContextStartedEvent> {
        public void onApplicationEvent(ContextStartedEvent contextStartedEvent) {
            System.out.println("Context Started.");
        }
    }

    public class HelloStopContext implements ApplicationListener<ContextStoppedEvent> {
        public void onApplicationEvent(ContextStoppedEvent contextStoppedEvent) {
            System.out.println("Context Stopped.");
        }
    }

    public class HelloSayHi implements ApplicationListener<HelloEvent>{
        public void onApplicationEvent(HelloEvent helloEvent) {
            System.out.println(helloEvent.toString());
        }
    }

    @Bean
    public HelloStartContext startListenerFactory(){
        HelloStartContext HL=new HelloStartContext();
        return HL;
    }

    @Bean
    public HelloStopContext stopListenerFactory(){
        HelloStopContext HL=new HelloStopContext();
        return HL;
    }

    @Bean
    public HelloSayHi HiFactory(){
        HelloSayHi HS=new HelloSayHi();
        return HS;
    }
}
