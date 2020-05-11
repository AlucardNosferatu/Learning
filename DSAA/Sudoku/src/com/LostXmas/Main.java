package com.LostXmas;

import java.util.Objects;
import java.util.Scanner;

public class Main {
    //    char[][] values;
    private String[][] values = new String[9][9];

    private void readIn() {
        Scanner in = new Scanner(System.in);
//        String str;
//        this.values = new char[9][9];//左行右列
//        for (int i = 0; i < 9; i++) {
//            str = in.nextLine();
//            this.values[i][0] = str.charAt(0);
//            this.values[i][1] = str.charAt(2);
//            this.values[i][2] = str.charAt(4);
//            this.values[i][3] = str.charAt(8);
//            this.values[i][4] = str.charAt(10);
//            this.values[i][5] = str.charAt(12);
//            this.values[i][6] = str.charAt(16);
//            this.values[i][7] = str.charAt(18);
//            this.values[i][8] = str.charAt(20);
//        }
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                values[i][j] = in.next();
                if ((j + 1) % 3 == 0) {
                    in.next();
                }
            }
        }

//        for (int i = 0; i < 9; i++) {
//            for (int j = 0; j < 9; j++) {
//                System.out.print(values[i][j]+" ");
//            }
//            System.out.println();
//        }
    }

    private void x_iterator() {//对数据中的x进行迭代求解
        boolean changed;
        do {
            changed = false;
            for (int i = 0; i < 9; i++) {
                for (int j = 0; j < 9; j++) {
                    if (values[i][j].equals("x")) {
                        changed = this.x_solver(i, j, this.isSolvable(i, j));
                    }
                }
            }
        } while (changed);
//        for (int i = 0; i < 9; i++) {
//            for (int j = 0; j < 9; j++) {
//                System.out.print(values[i][j]);
//            }
//            System.out.println();
//        }
    }
    private void output(){
        boolean imp=false;
        StringBuilder Temp= new StringBuilder();
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                if(Objects.equals(values[i][j], "x")){
                    imp=true;
                    break;
                }
            }
        }

        for(int i=0;i<9;i++){
            if(imp) break;
            int j;
            for(j = 0; j<9; j++){
                Temp.append(values[i][j]);
                if(j==2||j==5||j==8) Temp.append(" | ");
                else Temp.append(" ");
            }
            System.out.println(Temp);
            Temp = new StringBuilder();
            if(i==2||i==5) System.out.println();
        }
        if(imp) System.out.println("Impossible");
    }

    private boolean RowSolvable(int coordinate_x) {
        int m = 0;
        for (int i = 0; i < 9; i++) {
            if (values[coordinate_x][i].equals("x")) {
                m++;
            }
        }
        return m == 1;
    }

    private boolean ColSolvable(int coordinate_y) {
        int n = 0;
        for (int i = 0; i < 9; i++) {
            if (values[i][coordinate_y].equals("x")) {
                n++;
            }
        }
        return n == 1;
    }

    private boolean BlockSolvable(int coordinate_x, int coordinate_y) {
        int blockX = coordinate_x / 3;
        int blockY = coordinate_y / 3;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (values[i + blockX * 3][j + blockY * 3].equals("x")) {
                    return false;
                }
            }
        }
        return true;
    }

    private int isSolvable(int coordinate_x, int coordinate_y) {
        if (RowSolvable(coordinate_x)) {
            return 1;
        } else if (ColSolvable(coordinate_y)) {
            return 2;
        } else if (BlockSolvable(coordinate_x, coordinate_y)) {
            return 3;
        } else {
            return 0;
        }
    }

    private String RowSolver(int coordinate_x, int coordinate_y) {
        int sum = 45;
        for (int i = 0; i < 9; i++) {
            if (i != coordinate_y) {
//                sum -= (Integer.parseInt(values[coordinate_x][i]) - 48);
                sum=sum-Integer.parseInt(values[coordinate_x][i]);
            }
        }
//        sum += 48;
        return Integer.toString(sum);
    }

    public String ColSolver(int coordinate_x,int coordinate_y) {
        int sum = 45;
        for (int i = 0; i < 9; i++) {
            if (i != coordinate_x) {
//                sum -= (Integer.parseInt(values[i][coordinate_x]) - 48);
                sum=sum-Integer.parseInt(values[i][coordinate_y]);
            }
        }
//        sum += 48;
        return Integer.toString(sum);
    }

    public String BlockSolver(int coordinate_x, int coordinate_y) {
        int sum = 45;
        int blockX = coordinate_x / 3;
        int blockY = coordinate_y / 3;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if ((i + blockX * 3) != coordinate_x || (j + blockY * 3) != coordinate_y) {
//                    sum -= (Integer.parseInt(values[i + blockX * 3][j + blockY * 3]) - 48);
                    sum=sum-Integer.parseInt(values[i+blockX*3][j+blockY*3]);
                }
            }
        }
//        sum += 48;
        return Integer.toString(sum);
    }

    public boolean x_solver(int coordinate_x, int coordinate_y, int solvable) {
        boolean solved=false;
        String result = "x";
        switch (solvable) {
            case 0:
                break;
            case 1:
                result = RowSolver(coordinate_x, coordinate_y);
                solved=true;
                break;
            case 2:
                result = ColSolver(coordinate_x, coordinate_y);
                solved=true;
                break;
            case 3:
                result = BlockSolver(coordinate_x, coordinate_y);
                solved=true;
                break;
            default:
                break;
        }
        values[coordinate_x][coordinate_y] = result;
        return solved;
    }

    public static void main(String[] args) {
        Main M = new Main();
        M.readIn();
        M.x_iterator();
        M.output();
    }
}