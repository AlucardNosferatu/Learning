package com.lost_xmas.demo.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller {
    @RequestMapping("/start")
    public String onStart(){
        return "Merry Christmas!";
    }
}
