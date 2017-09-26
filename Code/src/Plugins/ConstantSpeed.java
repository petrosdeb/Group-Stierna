package Plugins;
/**
 * 
 * @author Petros
 * PlugIn can be assembled with many PlugIn ports defined as attributes in Java code. 
 * Two types of PlugIn port can be instanced:  
 * PluginPPort (read data from the port), PluginRPort (write data to the port). 
 * Note that these PlugIn ports always need to be initialized before invoking read or 
 * write methods, and initialization codes must be placed in the public void init() method.
 *
 */
import sics.plugin.PlugInComponent;
import sics.port.PluginPPort;
import sics.port.PluginRPort;

public class ConstantSpeed extends PlugInComponent {
	public PluginPPort pportSpeed;
	public PluginRPort rportFront;
	public PluginRPort rportRear;
	
	public ConstantSpeed() {}

	public ConstantSpeed(String[] args) {
		super(args);
	}
	
	public static void main(String[] args) {
		ConstantSpeed instance = new ConstantSpeed(args);
		instance.run();
	}

	@Override
	public void init() {
		// Initiate PluginPPort
		pportSpeed = new PluginPPort(this, "pportSpeed");
		pportSpeed.write("fs|10");
		rportFront = new PluginRPort(this, "rportFront", 0);
		rportRear = new PluginRPort(this, "rportRear", 0);
	}
	
	
	public void doFunction() throws InterruptedException {
		Integer newSpeed;
		Integer oldSpeed = 0;
		Integer speedValue = 10;
		while(true) {
			
			// read front wheel speed value
			Integer frontWheelData = (Integer)rportFront.read();
			
			// read rear wheel speed value
			Integer rearWheelData = (Integer)rportRear.read(); 
			if (!(frontWheelData == null) && !(rearWheelData == null)) {
				newSpeed = frontWheelData + rearWheelData;
			} else {
				newSpeed = 0;
			}
			
			//Minimum input for speed is -100
			if(newSpeed >= oldSpeed && speedValue != -100) {
				speedValue = speedValue - 1;
			} 
			
			//Maximum input for speed is 100
			else if(newSpeed < oldSpeed && speedValue != 100) {
				speedValue = speedValue + 1;
			}
			
			// Prepare published data, which is packaged in the format “key|value”
			String pubData = "fs|" + String.valueOf(speedValue);
			
			// Publish data
			pportSpeed.write(pubData);
			
			oldSpeed = newSpeed;
   			Thread.sleep(100);
   		}
	}
	
	
	public void run() {
		init();
		// do functions, for example, read front wheel speed value from sensor and then publish through MQTT
		try {
			doFunction();
			
   		} catch (InterruptedException e) {
   			
   		}
	}
}