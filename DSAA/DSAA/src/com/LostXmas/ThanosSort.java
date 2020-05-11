package com.LostXmas;

import java.util.Arrays;
import java.util.Scanner;

public class ThanosSort {
    int seq[];
    int seq2[];
    public ThanosSort(){
        Scanner S=new Scanner(System.in);
        int size=S.nextInt();
        seq=new int[size];
        for(int i=0;i<size;i++){
            seq[i]=S.nextInt();
        }
        int temp;
        boolean loop=true;
        while(loop){
            temp=0;
            ReplaceMainSeq();
            for(int i=0;i<seq.length;i++){
                if(seq[i]<temp){
                    SnapYourFinger();
                    loop=true;
                    break;
                }
                else{
                    temp=seq[i];
                    loop=false;
                }
            }

        }
        System.out.println(seq.length);
    }
    public void SnapYourFinger(){
        seq2=Arrays.copyOfRange(seq,seq.length/2,seq.length);
        seq= Arrays.copyOfRange(seq,0,seq.length/2);
    }

    public void ReplaceMainSeq(){
        if(seq2!=null){
            int seq_valid=1;
            int seq2_valid=1;
            for(int i=0;i<seq.length-1;i++){
                if (seq[i]<=seq[i+1]){
                    seq_valid++;
                }
                else{
                    break;
                }
            }
            for(int i=0;i<seq2.length-1;i++){
                if (seq2[i]<=seq2[i+1]){
                    seq2_valid++;
                }
                else{
                    break;
                }
            }
            if(seq2_valid>seq_valid){
                seq=seq2;
            }
        }
    }

    public static void main(String[] args) {
        ThanosSort TS=new ThanosSort();
    }
}
