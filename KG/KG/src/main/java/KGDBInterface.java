import org.neo4j.driver.v1.*;

public class KGDBInterface {
    public static void main(String[] args) {
        System.out.println("Hello World");
        Driver D= GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j","20160712"));
        try(Session S=D.session()){
            try(Transaction T=S.beginTransaction()){
                StatementResult SR=T.run("MATCH (n:Person)-[:LOVES]->(o:Person) RETURN n,o limit 2");
                while(SR.hasNext()){
                    Record R=SR.next();
                    System.out.print(String.format("%s loves ",R.get("n").get("name")));
                    System.out.println(String.format("%s",R.get("o").get("name")));
                }
            }
        }
        D.close();
    }
}
