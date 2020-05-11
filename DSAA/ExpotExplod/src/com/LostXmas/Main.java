package com.LostXmas;

import java.util.Scanner;

public class Main {
    public static void ROFFF(){
        long r=1;
        Scanner S=new Scanner(System.in);
        System.out.println("Give me n:");
        long n = S.nextInt();
        System.out.println("Give me m:");
        long m = S.nextInt();
        if(n>=4){
            r=0;
        }
        else{
            n = Main.factorial(n);
            n = Main.factorial(n);
            long r_temp=1;
            long r_current=1;
            for(long i=n;i>=1;i--){
                r_current=i%m;
                //本次循环求出的余数
                r_temp*=r_current;
                //所有余数的积
                if(r_temp>m){//如果余数比m大，对余积再求余
                    r_temp%=m;
                }
            }
            r=r_temp;
        }
        System.out.println(r);
    }
    public static void main(String[] args) {
        Main.ROFFF();
    }
    public static long factorial(long n){
        if(n==1){
            return 1;
        }
        else{
            return n*factorial(n-1);
        }
    }
}
