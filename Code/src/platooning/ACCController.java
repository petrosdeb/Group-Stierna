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
		// TODO Auto-generated method stub
		
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