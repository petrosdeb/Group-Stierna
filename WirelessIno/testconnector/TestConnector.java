import java.io.IOException;
import java.io.*;
import java.net.*;

import static java.lang.System.in;
import static java.lang.System.out;

public class TestConnector {
    public static void main(String[] args) throws IOException {
        new TestConnector(args);
    }

    TestConnector(String... args) {
        if (args.length != 2) {
            System.err.println(
                    "Usage: java TestConnector <host name> <port number>");
            System.exit(1);
        }

        String hostName = args[0];
        int portNumber = Integer.parseInt(args[1]);

        try (
                Socket echoSocket = new Socket(hostName, portNumber);
                PrintWriter out =
                        new PrintWriter(echoSocket.getOutputStream(), true);
                BufferedReader in =
                        new BufferedReader(
                                new InputStreamReader(echoSocket.getInputStream()));
                BufferedReader stdIn =
                        new BufferedReader(
                                new InputStreamReader(System.in))
        ) {
            String userInput;
//            new ReadThread(in).run();
            while ((userInput = stdIn.readLine()) != null) {
                out.println(userInput);
            }
        } catch (UnknownHostException e) {
            System.err.println("Don't know about host " + hostName);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to " +
                    hostName);
            System.exit(1);
        }
    }

    /*
    Thread that reads a stream and outputs it
     */
    class ReadThread implements Runnable {

        ReadThread(BufferedReader inputStream) {
            in = new BufferedReader(inputStream);
        }

        BufferedReader in;

        @Override
        public void run() {
            while (true) {
                try {
                    String v;
                    out.println(v = in.readLine());

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /*
    Thread that reads the standard input stream and outputs it to a stream
//     */
//    class WriteThread implements Runnable {
//
//        WriteThread(OutputStream stream) {
//            out = new PrintWriter(stream);
//        }
//
//        PrintWriter out;
//
//        BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
//
//        @Override
//        public void run() {
//        }
//    }
}



