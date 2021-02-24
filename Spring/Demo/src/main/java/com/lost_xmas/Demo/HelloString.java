package com.lost_xmas.Demo;

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

    public void beforeAspect(){
        System.out.println("This will always show before running getMsg.");
    }

    public void afterAspect(){
        System.out.println("This will always show after running getMsg.");
    }

    /**
     * This is the method which I would like to execute
     * when any method returns.
     */
    public void afterReturningAdvice(Object retVal){
        System.out.println("Returning:" + ((HelloString) retVal).getHello() );
    }
    /**
     * This is the method which I would like to execute
     * if there is an exception raised.
     */
    public void AfterThrowingAdvice(IllegalArgumentException ex){
        System.out.println("There has been an exception: " + ex.toString());
    }
}
