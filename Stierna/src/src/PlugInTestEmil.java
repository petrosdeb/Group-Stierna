import sics.plugin.PlugInComponent;
import sics.port.PluginPPort;
import sics.port.PluginRPort;

public class PlugInTestEmil extends PlugInComponent {
    public PluginPPort pport;
    public PluginRPort rport;

    public PlugInTestEmil() {}

    public PlugInTestEmil(String[] args) {
        super(args);
    }

    public static void main(String[] args) {
        PlugInTestEmil instance = new PlugInTestEmil(args);
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
            // Write speed to Drive Motor port
            this.pport.setId(3);

            // Send speed 2 to Drive Motor for 5 seconds
            long start = System.currentTimeMillis();
            long end = start + 5*1000; // 60 seconds * 1000 ms/sec
            while (System.currentTimeMillis() < end)
            {
                this.pport.write(2);
            }

            // Brake after 5 seconds
            this.pport.write(0);

            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                ;
            }
        }
    }
}

