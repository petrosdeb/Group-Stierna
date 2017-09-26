package platooning;

import sics.plugin.PlugInComponent;
import sics.port.PluginPPort;
import sics.port.PluginRPort;

public class ACCController extends PlugInComponent {
	
	public PluginPPort writeSpeed;
	public PluginPPort writeSteer;
	public PluginPPort writeLED;
	public PluginRPort readFrontSpeed;
	public PluginRPort readRearSpeed;
	public PluginRPort readPosition;
	
	
	public ACCController(String[] args) {
		super(args);
	}

	public static void main(String[] args) {
		
		ACCController controller = new ACCController(args);
		controller.run();
		
	}

	@Override
	public void run() {
		
	}

	@Override
	public void init() {
		writeSpeed = new PluginPPort(this, "writeSpeed");
		writeSteer = new PluginPPort(this, "writeSteer");
		writeLED = new PluginPPort(this, "writeLED");
		
		readFrontSpeed = new PluginRPort(this, "readFrontSpeed", 0);
		readRearSpeed = new PluginRPort(this, "readRearSpeed", 0);
		readPosition = new PluginRPort(this, "readPosition", 0);
		
		
	}
	
	public void sendToSCU(int data) {
		
	}

}

class SCUData extends Thread {
	private PluginRPort scuPort;
	private Integer data;
	
	public SCUData(PluginRPort scuPort) {
		this.scuPort = scuPort;
	}
	
	public void run() {
		data = (Integer) scuPort.read(); //might return a string
	}
	
	public Integer getData() {
		return data;
	}
	
}