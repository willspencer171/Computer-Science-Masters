public class Employee {
    Project assignedProject;
    String employeeId;
    String firstName;
    String lastName;
    String department;
    String role;

    // Constructor
    public Employee(String employeeId, String firstName, String lastName, String department, String role) {
        this.employeeId = employeeId;
        this.firstName = firstName;
        this.lastName = lastName;
        this.department = department;
        this.role = role;
        this.assignedProject = null;
    }

    public String display() {
        return this.employeeId + ", " + this.firstName.charAt(0) + ". " + this.lastName + ", " + this.role;
    }
}
