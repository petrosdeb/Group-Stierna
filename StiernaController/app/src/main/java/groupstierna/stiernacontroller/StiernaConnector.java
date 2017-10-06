package groupstierna.stiernacontroller;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;

public class StiernaConnector {
    private String hostName;
    private int portNumber;
    private PrintWriter out;
    private Socket socket;

    public boolean tryConnect() {
        if (socket != null) {
            if (socket.isConnected()) {
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                    return false;
                }
            }
        }
        new Thread(new ClientThread()).start();
        return socket.isConnected();
    }

    public void main(String[] args) throws IOException {

        if (args.length != 2) {
            System.err.println(
                    "Usage: java TestConnector <host name> <port number>");
            System.exit(1);
        }

        hostName = args[0];
        portNumber = Integer.parseInt(args[1]);
    }

    public boolean send(String message) {
        if (socket != null) {
            out.println(message);
            return true;
        }
        return false;
    }

    public void setHostName(String hostName) {
        this.hostName = hostName;
    }

    public void setPortNumber(int portNumber) {
        this.portNumber = portNumber;
    }

    class ClientThread implements Runnable {

        @Override
        public void run() {
            try {
                InetAddress serverAddress = InetAddress.getByName(hostName);
                socket = new Socket(serverAddress, portNumber);
                out = new PrintWriter(socket.getOutputStream(), true);
            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (SocketException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (Exception e) {
                e.printStackTrace();
            } catch (Throwable t) {
                t.printStackTrace();
            }
        }
    }
}