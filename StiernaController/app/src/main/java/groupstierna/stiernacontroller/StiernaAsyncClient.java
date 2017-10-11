package groupstierna.stiernacontroller;

import android.os.AsyncTask;
import android.os.Handler;
import android.os.Message;
import android.widget.TextView;

import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;

public class StiernaAsyncClient extends AsyncTask<Void, Void, TextView> {
    private Boolean successful;
    private String hostName;
    private int portNumber;
    private String message;
    private Handler connectionStatusHandler;

    public StiernaAsyncClient(String hostName, int portNumber, String message, Handler connectionStatusHandler) {
        this.hostName = hostName;
        this.portNumber = portNumber;
        this.message = message;
        this.connectionStatusHandler = connectionStatusHandler;
    }

    @Override
    protected TextView doInBackground(Void... voids) {
        Socket socket;
        PrintWriter out;

        InetSocketAddress address = new InetSocketAddress(hostName, portNumber);

        try {
            socket = new Socket();
            socket.connect(address);
            out = new PrintWriter(socket.getOutputStream(), true);
        } catch (Throwable e) {
            e.printStackTrace();
            successful = false;
            return null;
        }

        if (!message.isEmpty()) {
            out.println(message);
        }

        successful = true;
        return null;
    }

    @Override
    protected void onPostExecute(TextView result) {
        Message resultMessage = new Message();
        if (successful) {
            resultMessage.arg1 = R.string.connected;
        } else {
            resultMessage.arg1 = R.string.disconnected;
        }
        resultMessage.obj = successful;
        connectionStatusHandler.sendMessage(resultMessage);
    }
}
