package com.lost_xmas.Demo;

import org.aspectj.lang.annotation.*;

@Aspect
public class HelloAspect {
    private String Hello;

    public HelloAspect(String H){
        this.Hello=H;
    }
//    @Required
    public void setHello(String H){
        this.Hello=H;
    }
    public String getHello(){
        return this.Hello;
    }

    @Pointcut("execution(* com.lost_xmas.Demo.HelloSpring.getMsg(..))")
    private void cutIn(){
        System.out.println("This is a cut-in aspect.");
    }

    @Before("cutIn()")
    public void beforeAspect(){
        System.out.println("This will always show before running getMsg.");
    }

    @After("cutIn()")
    public void afterAspect(){
        System.out.println("This will always show after running getMsg.");
    }

    /**
     * This is the method which I would like to execute
     * when any method returns.
     */
    @AfterReturning(pointcut = "cutIn()", returning = "retVal")
    public void afterReturningAdvice(Object retVal){
        System.out.println("Returning:" + ((HelloAspect) retVal).getHello() );
    }
    /**
     * This is the method which I would like to execute
     * if there is an exception raised.
     */
    public void AfterThrowingAdvice(IllegalArgumentException ex){
        System.out.println("There has been an exception: " + ex.toString());
    }
}
