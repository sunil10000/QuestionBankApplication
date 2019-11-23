import java.io.*;
import java.util.*;
import java.net.*;

public class TestClient{
    Socket client;
    BufferedReader in;
    PrintWriter out;
    int deltaSum=0;
    Map<Integer, Integer> db;

    void start(String ip_str,int port) {
        try
        {
            client = new Socket(ip_str,port);
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            out = new PrintWriter(client.getOutputStream(), true);
            System.out.println("OK");
            db = new HashMap<Integer, Integer>();
        }
        catch(Exception e){
            System.out.println("No Server");
            System.exit(1);
        }

    }

    public void close() throws IOException{
        client.close();
        out.close();
        in.close();
    }

    public void add(int key,int value){
        db.put(key,value);
    }

    public int read(int key){
        if(db.containsKey(key)){
            return db.get(key);
        }
        else {
            return 0;
        }
    }

    public void send(String s){
        out.println(s);
        out.flush();
    }

    public void processCommand(String cmd) throws IOException,InterruptedException{
            String[] cmds = cmd.split("\\s+");

            if(cmds[0].equals("disconnect")){
                this.send("disconnect");
                this.close();
                System.out.println("OK");
            }
            else if(cmds[0].equals("add")){
                this.send("add "+ cmds[1]);
                int x = Integer.parseInt(in.readLine());
                this.add(Integer.parseInt(cmds[1]),x);
            }
            else if(cmds[0].equals("read")){
                this.send("read "+cmds[1]);
                int old_w = this.read(Integer.parseInt(cmds[1]));
                int new_w = new_w = Integer.parseInt(in.readLine());
                this.deltaSum+=(new_w-old_w);
                System.out.println((Integer.toString(new_w))+" "+(Integer.toString(new_w-old_w)));
            }
            else if(cmds[0].equals("connect")){
                this.start(cmds[1],(Integer.parseInt(cmds[2])));
            }
            else if(cmds[0].equals("sleep")){
                Thread.sleep(Integer.parseInt(cmds[1]));
            }
            else if(cmds[0].equals("print")){
                System.out.println(this.deltaSum);
            }
            else{// unknown command don't do anything
            }
    }

    public static void main(String[] args) throws IOException,InterruptedException{
        TestClient basicCleint = new TestClient();
        Scanner scanner = new Scanner(System.in);
        while(true){
            String line = scanner.nextLine();
            basicCleint.processCommand(line);
        }
        // BufferedReader reader = new BufferedReader(new FileReader(file_path));
        // String line = reader.readLine();
        // while(line!=null){
        //     // System.out.println(line);
        //     basicCleint.processCommand(line);
        //     line = reader.readLine();
        // }
        // reader.close();
        // System.out.println(basicCleint.deltaSum);

    }


}
