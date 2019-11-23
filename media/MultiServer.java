import java.io.*;
import java.util.*;
import java.net.*;
import java.lang.*;

public class MultiServer extends BasicServer implements Runnable{
    boolean isOpen;

    public MultiServer(Socket myClient) throws IOException{
        super(myClient);
        isOpen = true;
    }

    @Override
    public void run(){
        try
        {
            while(isOpen){
                String cmd = this.recieveLine();
                if(cmd!=null){
                    //System.out.println(cmd);
                    String[] cmds = cmd.split("\\s+");
                    if(cmds[0].equals("disconnect")){
                        this.close();
                        System.out.println("DIS");
                        isOpen = false;
                    }
                    else if(cmds[0].equals("add")){
                        this.add(Integer.parseInt(cmds[1]));
                        System.out.println("ADD "+cmds[1]);
                        this.send(Integer.toString(this.read(Integer.parseInt(cmds[1]))));
                    }
                    else if(cmds[0].equals("read")){
                        int w = this.read(Integer.parseInt(cmds[1]));
                        System.out.println("READ "+cmds[1]+" "+(Integer.toString(w)));
                        this.send(Integer.toString(w));
                    }
                    else{// unknown command don't do anything
                    }
                }
            }
        } catch(Exception e){}
    }

    public static void main(String[] args) throws IOException{
        ServerSocket server = new ServerSocket(5000);
        System.out.println("Listening on 5000");
        Socket client;
        List<Thread> threads = new ArrayList<Thread>();
        while(true){
            client = server.accept();
            Thread t = new Thread(new MultiServer(client));
            t.start();
            threads.add(t);
        }

    }
}
// public static void main(String[] args) throws IOException{
//         ServerSocket server = new ServerSocket(5000);
//         System.out.println("Listening on 5000");
//         Socket client;
//         //List<Thread> threads = new ArrayList<Thread>();
//         ExecutorService pool = Executors.newFixedThreadPool(MAX_C);
//         while(true){
//             client = server.accept();
//             // Thread t = new Thread(new MultiServer(client));
//             // t.start();
//             // threads.add(t);
//             Runnable r = new MultiServer(client);
//             pool.execute(r);
//         }

//     }
