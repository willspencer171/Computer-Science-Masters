import java.time.LocalDate;
import java.util.ArrayList;

public class Project {
    String projectId;
    String projectName;
    String projectDescription;
    float projectCost;
    LocalDate start;
    LocalDate end;
    ArrayList<Employee> assignedEmployees;

    // Constructor
    public Project(String projectId, String projectName, String projectDescription, float projectCost, LocalDate start, LocalDate end) {
        this.projectId = projectId;
        this.projectName = projectName;
        this.projectDescription = projectDescription;
        this.projectCost = projectCost;
        this.start = start;
        this.end = end;
        this.assignedEmployees = new ArrayList<>();
    }

    public String display(){
        return this.projectId + ", " + this.projectName + ", £" + this.projectCost;
    }
}
