import java.util.Scanner;
public class GeneCheck {
	public static void main(String[] args) {
		System.out.println("请输入基因序列");
		Scanner input=new Scanner(System.in);
		char[] gene_sequence=input.next().toCharArray();
		String [] codon=new String[1000];
		int count=0;
		for(int x=0;x<gene_sequence.length/3;x++){//密码子个数
			if(count==3)//密码子三个一组
				count=1;//数完三个从头计
			for(int y=3*x;y<gene_sequence.length&&count!=2;y++){//y是碱基个数，如果count分别为0、1、2，是2则代表末尾
				if(gene_sequence[y]=='A'||gene_sequence[y]=='T'||gene_sequence[y]=='C'||gene_sequence[y]=='G'){//一个个数过去看是不是ATCG构成的
					if((y+1)>=3&&(y+1)%3==0){
						if(gene_sequence[y-2]=='A'&&gene_sequence[y-1]=='T'&&gene_sequence[y]=='G'&&count==0){
							codon[0]=new String(new char[]{gene_sequence[y-2],gene_sequence[y-1],gene_sequence[y]}); 
							count=1;
							}
						if(count==1&&x!=0){
							if(gene_sequence[y-2]=='G'&&gene_sequence[y-1]=='A'&&gene_sequence[y]=='T'&&count==1){
								count=2;
								}
							if(gene_sequence[y-2]=='A'&&gene_sequence[y-1]=='A'&&gene_sequence[y]=='T'&&count==1){
								count=2;
								}
							if(gene_sequence[y-2]=='A'&&gene_sequence[y-1]=='G'&&gene_sequence[y]=='T'&&count==1){
								count=2;
								}
							else{
								codon[x]=new String(new char[]{gene_sequence[y-2],gene_sequence[y-1],gene_sequence[y]});
								count=3;
								}
							}
						}
					}
				else{System.out.println("这不是基因组");
				break;
				}
				}
			}
		System.out.print("从基因组中读取的基因：");
		for(int z=0;z<codon.length;z++){
			if(z==0){System.out.print("启始密码子：");
			}
			if(codon[z]==null){System.out.print("：终止密码子")
				;break;
				}
			System.out.println(codon[z]);
			}
		}
	}
