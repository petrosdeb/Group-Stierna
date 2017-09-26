package platooning;

import sics.port.PluginPPort;
import sics.port.PluginRPort;

/**
 * 
 * @author Petros Debesay
 * 
 * The model
 *
 */
public final class ACCSystem {
	/**
	 * All ports for read and write. In controller instead? Where we have one for
	 * each ECU? Or at least VCU and SCU.
	 */
	
	private static ACCSystem instance = null;
	
	private int speed;
	private int distance;
	private int led;
	private int steer;
	
	private ACCSystem() {
		
	}
	
	public static ACCSystem getInstance() {
        if (instance == null) {
            synchronized(ACCSystem.class) {
                if (instance == null) {
                    instance = new ACCSystem();
                }
            }
        }
        return instance;
    }
}