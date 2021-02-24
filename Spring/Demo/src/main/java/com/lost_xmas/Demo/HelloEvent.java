package com.lost_xmas.Demo;

import org.springframework.context.ApplicationEvent;

public class HelloEvent extends ApplicationEvent {
    public HelloEvent(Object source) {
        super(source);
    }

    public String toString(){
        return "Hi!";
    }
}
