
/**
 * Simplified version of Roger Garside's person class
 * @author Roger Garside - updated by Marc Roper
 * @version Last Rewritten: 17th March 1997 - updates October 2002
 */

public class Person extends Subject {
    
    private String forename ;
    private String surname ;
    private int age ;
    
    public Person() {
        forename = "NONE" ;
        surname = "NONE" ;
        age = 0 ;
    } 

    public String getForename() {
        return forename ;
    } 

    public String getSurname(){
        return surname ;
    } 
    
    public int getAge() {
        return age ;
    } 
    

    // call notifyObs() at end of each mutator
    public void setForename(String f) {
        forename = f ;
        notifyObs();
    } 
    
    public void setSurname(String s) {
        surname = s ;
        notifyObs();
    } 
    
    public void setAge(int a) {
        age = a ;
        notifyObs();
    } 

    public void increaseAge(int n) {
        age += n ;
        notifyObs();
    }     
}




