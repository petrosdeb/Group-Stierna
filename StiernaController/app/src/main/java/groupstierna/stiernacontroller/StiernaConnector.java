package groupstierna.stiernacontroller;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class StiernaConnector {
    private static String hostName;
    private static int portNumber;
    private static PrintWriter out;

    public StiernaConnector() {
        updateConnection();
    }

    public static void updateConnection() {
        try {
            Socket echoSocket = new Socket(hostName, portNumber);
            out = new PrintWriter(echoSocket.getOutputStream(), true);
        } catch (UnknownHostException e) {
            System.err.println("Don't know about host " + hostName);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to " +
                    hostName);
            System.exit(1);
        }
    }

    public static void main(String[] args) throws IOException {

        if (args.length != 2) {
            System.err.println(
                    "Usage: java TestConnector <host name> <port number>");
            System.exit(1);
        }

        hostName = args[0];
        portNumber = Integer.parseInt(args[1]);
    }

    public static void send(String message) {
        out.println(message);
    }

    public static void setHostName(String hostName) {
        StiernaConnector.hostName = hostName;
    }

    public static void setPortNumber(int portNumber) {
        StiernaConnector.portNumber = portNumber;
    }
}
