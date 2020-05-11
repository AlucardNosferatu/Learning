package com.LostXmas;

import java.util.Scanner;

public class TheLeastRoundWay {
    public TheLeastRoundWay(){
        Scanner S=new Scanner(System.in);
        int Size=S.nextInt();
        int Matrix[][][]=new int[Size][Size][3];
        for(int i=0;i<Size;i++){
            for(int j=0;j<Size;j++){
                Matrix[i][j][2]=S.nextInt();
                while((Matrix[i][j][2]%2==0)&&(Matrix[i][j][2]!=0)){
                    Matrix[i][j][2]/=2;
                    Matrix[i][j][0]++;
                }
                while((Matrix[i][j][2]%5==0)&&(Matrix[i][j][2]!=0)){
                    Matrix[i][j][2]/=5;
                    Matrix[i][j][1]++;
                }

            }
        }
        // TODO: 2019/9/11 NEED DP PROCESSOR

        System.out.println(Matrix);
    }
}
