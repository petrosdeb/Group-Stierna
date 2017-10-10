package groupstierna.stiernacontroller;

import android.os.AsyncTask;
import android.widget.TextView;

import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;

public class StiernaAsyncClient extends AsyncTask<Void, Void, TextView> {
    private Boolean successful;
    private String hostName;
    private int portNumber;
    private String message;
    private TextView connectionStatus;

    public StiernaAsyncClient(String hostName, int portNumber, String message, TextView connectionStatus) {
        this.hostName = hostName;
        this.portNumber = portNumber;
        this.message = message;
        this.connectionStatus = connectionStatus;
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
        if (successful) {
            connectionStatus.setText(R.string.connected);
        } else {
            connectionStatus.setText(R.string.disconnected);
        }
        MainActivity.connectionStatus = successful;
    }
}
