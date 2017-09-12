import sics.*;
import sics.plugin.PlugInComponent;
import sics.port.PluginPPort;
import sics.port.PluginRPort;

public class PlugInTest extends PlugInComponent {
    public PluginPPort pport;
    public PluginRPort rport;

    public PlugInTest() {}

    public PlugInTest(String[] args) {
        super(args);
    }

    public static void main(String[] args) {
        PlugInTest instance = new PlugInTest(args);
        instance.run();
    }

    @Override
    public void init() {
        // Initiate PluginPPort
        pport = new PluginPPort(this, "pport");
        rport = new PluginRPort(this, "rport", 0);
    }

    public void run() {
        init();
        // do functions, for example, read front wheel speed value from sensor and then publish through MQTT
        while(true) {
            // read front wheel speed value
            Integer frontWheelData = (Integer)rport.read();
            // Prepare published data, which is packaged in the format “key|value”
            String pubData = "fs|" + String.valueOf(frontWheelData);
            // Publish data
            pport.write(pubData);
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                ;
            }
        }
    }
}
