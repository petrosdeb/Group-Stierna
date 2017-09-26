package platooning;

import sics.plugin.PlugInComponent;
import sics.port.PluginRPort;

public class ControllerSCU extends PlugInComponent {
	
	public PluginRPort readDistance;
	public PluginRPort readIMU;
	public PluginRPort rportFront;

	@Override
	public void run() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void init() {
		// TODO Auto-generated method stub
		
	}
	
	public void sendToVCU(int data) {
		
	}

}
