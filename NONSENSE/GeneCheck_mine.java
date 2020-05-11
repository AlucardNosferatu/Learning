import java.util.Scanner;
public class GeneCheck_mine {
	Scanner input;
	char[] gene_sequence;
	String valid_gene_sequence;
	int start_index;
	int end_index;
	public GeneCheck_mine(){
		this.input=new Scanner(System.in);
		this.start_index=0;
		this.end_index=0;
		}
	public static void main(String[]args){
		GeneCheck_mine GCM=new GeneCheck_mine();
		GCM.gene_sequence=GCM.input.next().toCharArray();//得到基因序列
		if(GCM.distinguish()){
			GCM.process();
			}
		}
	public Boolean distinguish(){
		Boolean judge=true;
		for(int i=0;i<=this.gene_sequence.length-2;i++){
			if(this.gene_sequence[i]!='A'&&this.gene_sequence[i]!='T'&&this.gene_sequence[i]!='C'&&this.gene_sequence[i]!='G'){
				judge=false;
				i=this.gene_sequence.length+1;
				}
			else{
				judge=true;
				}
			}
		return judge;
		}
	public void process(){
		this.start();
		this.end();
		this.record();
		this.print();
		}
	public void start(){
		for(int i=0;i<=this.gene_sequence.length;i++){
			if(this.gene_sequence[i]=='A'){
				if(this.gene_sequence[i+1]=='T'){
					if(this.gene_sequence[i+2]=='G'){
						this.start_index=i;//第一个ATG的第一位
						i=this.gene_sequence.length+1;
						}
					}
				}
			}
		}
	public void end(){
		for(int i=this.start_index+3;i<=this.gene_sequence.length;i+=3){
			if(this.gene_sequence[i]=='T'){
				if(this.gene_sequence[i+1]=='A'){
					if(this.gene_sequence[i+2]=='G'||this.gene_sequence[i+2]=='A'){
						this.end_index=i;//第一个的TAG的第一位
						i=this.gene_sequence.length+1;
						}
					}
				else if(this.gene_sequence[i+1]=='G'){
					if(this.gene_sequence[i+2]=='A'){
						this.end_index=i;//第一个的TGA的第一位
						i=this.gene_sequence.length+1;
						}
					}
				}
			}
		}
	public void record(){
		this.valid_gene_sequence=""+this.gene_sequence[this.start_index+3];
		for(int i=this.start_index+4;i<this.end_index;i++){
			this.valid_gene_sequence+=this.gene_sequence[i];
			}
		}
	public void print(){
		System.out.println(this.valid_gene_sequence);
		}
	}
