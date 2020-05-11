package com.LostXmas;

import java.util.Scanner;

public class Nineteen {
    String Str;
    public Nineteen(){
        Scanner S=new Scanner(System.in);
        int count=0;
        Str=S.nextLine();
        for(int i=0;i<Str.length()-8;i++){
            if(Str.charAt(i)=='n'){
                if(Str.substring(i,i+8).equals("nineteen")){
                    count++;
                }
            }
        }
        System.out.println(count);
    }
}
