package com.LostXmas;

import java.util.Scanner;

public class MainZZY {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        int m = in.nextInt();
        long x = 1;
        if (n >= 4) {
            x = 0;
        } else if (n == 0 || n == 1) {
            if (m == 1) {
                x = 0;
            } else x = 1;
        } else if (n == 2) {
            if (m <= 8) {
                x = 8 % m;
            } else x = 8;
        }else if (n==3){
            if (m<=720){
                x=0;
            }else for (int i = 720; i >0 ; i--) {
                int k=i%m;
                x=x*k;
            }
        }
        System.out.println(x);
    }
}