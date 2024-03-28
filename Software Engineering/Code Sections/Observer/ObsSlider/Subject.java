
/**
 * Abstract Subject Class
 */

public abstract class Subject {
    
    // Arrays of observers
    private Observer observers[] = new Observer[5];
    int numObs = 0;
    
    // method to attach observers
    public void attach(Observer o) {
	observers[numObs] = o;
	numObs++;
    }
    
    // method to notify observers of state change
    // can't call notify as this is defined in Object
    public void notifyObs() {
	for(int i=0; i<numObs; i++) {
	    observers[i].update();
	}
    }
}


