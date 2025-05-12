import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Scanner;

public class Driver {
    static ArrayList<Employee> employees = new ArrayList<Employee>();
    static ArrayList<Project> projects = new ArrayList<Project>();

    public static void main(String[] args) throws Exception {
        // Hard-coded database :')
        employees.add(new Employee("E401", "Michael", "Johnson", "Civil Engineering", "Structural Engineer"));
        employees.add(new Employee("E402", "Anna", "Rodriguez", "Architecture", "Architect"));
        employees.add(new Employee("E403", "James", "Thompson", "Project Management", "Project Manager"));
        employees.add(new Employee("E404", "Sophia", "Martinez", "Safety & Compliance", "Safety Officer"));
        employees.add(new Employee("E405", "David", "Wilson", "Electrical Engineering", "Electrical Engineer"));
        employees.add(new Employee("E406", "Olivia", "Brown", "Site Operations", "Construction Site Supervisor"));

        projects.add(new Project("C101", "Residential Tower", "Construction of a 25-story residential building", 2000000, LocalDate.parse("2023-07-10"), LocalDate.parse("2024-12-15")));
        projects.add(new Project("C102", "Highway Expansion", "Expanding a major highway to improve traffic flow", 2400000, LocalDate.parse("2023-08-01"), LocalDate.parse("2025-06-30")));
        projects.add(new Project("C103", "Commercial Plaza", "Developing a shopping and office complex", 1400000, LocalDate.parse("2023-09-15"), LocalDate.parse("2024-05-20")));
        projects.add(new Project("C104", "Bridge Construction", "Building a new suspension bridge over the river", 4400000, LocalDate.parse("2023-10-05"), LocalDate.parse("2025-08-10")));
        projects.add(new Project("C105", "Industrial Warehouse", "Constructing a warehouse for storage and distribution", 2100000, LocalDate.parse("2023-11-20"), LocalDate.parse("2024-09-30")));
        projects.add(new Project("C106", "Airport Terminal Upgrade", "Renovation and expansion of the airport terminal", 3900000, LocalDate.parse("2023-12-10"), LocalDate.parse("2025-07-31")));
        System.out.println("Welcome to the Project/Employee database!");

        loop: while (true) {
            System.out.println("""
Choose from the following options using the numbers:
----------------------------------------------------
1. Add a new project record
2. Add a new employee record
3. Get total cost of projects
4. Find highest cost project
5. Find lowest cost project
6. Sort employees alphabetically by surname
7. Sort projects by cost (largest to smallest)
8. Assign an employee to a project
-1. Quit
""");
            System.out.print("Enter your choice: ");
            Scanner scan = new Scanner(System.in);
            int user_input;
            try {
                user_input = scan.nextInt();
            } catch (InputMismatchException e) {
                System.out.println("Error! Please enter an integer for the option!");
                continue;
            }

            switch (user_input) {
                case 1: {
                    InputProjectData(projects);
                    break;
                }
                case 2: {
                    InputEmployeeData(employees);
                    break;
                }
                case 3: {
                    ProjectSumCost(projects);
                    break;
                }
                case 4: {
                    HighestCostProject(projects);
                    break;
                }
                case 5: {
                    LowestCostProject(projects);
                    break;
                }
                case 6: {
                    SortEmployeesByLastName(employees);
                    break;
                }
                case 7: {
                    SortProjectsByCost(projects);
                    break;
                }
                case 8: {
                    AssignEmployeeToProject(employees, projects);
                    break;
                }
                case -1: {
                    System.out.println("Exiting menu...");
                    break loop;
                }
                default: {
                    int result1 = 12/2;

                    long result2 = 12L/2;

                    float result3 = result1+result2;

                    System.out.println(result1); // 1st result:




                    System.out.println(result2); // 2nd result:



                    System.out.println(result3); // 3rd result:

                    }
                    break;
                }
            }
        }


    private static void InputProjectData(ArrayList<Project> project_data) {
        Scanner scan = new Scanner(System.in);
        String name;
        String desc;
        float cost;
        LocalDate start_date;
        LocalDate end_date;

        while (true) {
            System.out.print("Project Name: ");
            name = scan.nextLine().strip();
            if (name.isBlank()) {
                System.out.println("Please enter a project name");
                continue;
            }

            System.out.print("Project Description: ");
            desc = scan.nextLine().strip();
            if (desc.isBlank()) {
                System.out.println("Please enter a project description");
                continue;
            }

            System.out.print("Project Cost (£): ");
            try {
                cost = scan.nextFloat();
                scan.nextLine();
            } catch (InputMismatchException e) {
                System.out.println("Please enter a floating point value for cost");
                continue;
            }

            System.out.print("Start Date (YYYY-MM-DD): ");
            String start_date_string = scan.nextLine();
            try {
                start_date = LocalDate.parse(start_date_string);
            } catch (DateTimeParseException e) {
                System.out.println("Please enter a date of the format DD-MM-YYYY");
                continue;
            }

            System.out.print("End Date (YYYY-MM-DD): ");
            String end_date_string = scan.nextLine();
            try {
                end_date = LocalDate.parse(end_date_string);
                break;
            } catch (DateTimeParseException e) {
                System.out.println("Please enter a date of the format DD-MM-YYYY");
            }
        }

        String project_id = project_data.getLast().projectId;
        String pid = "C" + (Integer.parseInt(project_id.substring(1)) + 1);

        project_data.add(new Project(pid, name, desc, cost, start_date, end_date));
        for (Project project: project_data) {
            System.out.println(project.display());
        }
    }

    private static void InputEmployeeData(ArrayList<Employee> employee_data) {
        // Because of the blocking action, this is O(infinity), but in practical terms
        // infinity is a constant so it's O(1)
        Scanner scan = new Scanner(System.in);
        String eid;
        String forename;
        String surname;
        String department;
        String role;

        while (true) {
            System.out.print("Enter forename: ");
            forename = scan.nextLine().strip();
            if (forename.isBlank()) {
                System.out.println("Please enter a name");
                continue;
            }

            System.out.print("Enter surname: ");
            surname = scan.nextLine().strip();
            if (surname.isBlank()) {
                System.out.println("Please enter a surname");
                continue;
            }

            System.out.print("Enter department: ");
            department = scan.nextLine().strip();
            if (department.isBlank()) {
                System.out.println("Please enter a department name");
                continue;
            }

            System.out.print("Enter role: ");
            role = scan.nextLine().strip();
            if (role.isBlank()) {
                System.out.println("Please enter a role");
                continue;
            }
            break;
        }

        String employee_id = employee_data.getLast().employeeId;
        eid = "E" + (Integer.parseInt(employee_id.substring(1)) + 1);

        employee_data.add(new Employee(eid, forename, surname, department, role));

        for (Employee employee: employee_data) {
            System.out.println(employee.display());
        }
    }

    private static void ProjectSumCost(ArrayList<Project> projects) {
        // Complexity O(n)
        int numberOfProjects = projects.size();

        float cost = 0;
        for (Project project: projects) {
            cost = cost + project.projectCost;
        }

        System.out.println("Number of projects: " + numberOfProjects);
        System.out.println("Total cost of projects: " + cost);
    }

    private static void HighestCostProject(ArrayList<Project> projects) {
        // Complexity O(n)
        double highest = Double.NEGATIVE_INFINITY;
        Project best_project = projects.getFirst();

        for (Project project: projects) {
            if (project.projectCost > highest) {
                highest = project.projectCost;
                best_project = project;
            }
        }

        System.out.println("Highest cost project:");
        System.out.println(best_project.display());
    }

    private static void LowestCostProject(ArrayList<Project> projects) {
        // Complexity O(n)
        double lowest = Double.POSITIVE_INFINITY;
        Project cheapestProject = projects.getFirst();

        for (Project project: projects) {
            if (project.projectCost < lowest) {
                lowest = project.projectCost;
                cheapestProject = project;
            }
        }

        System.out.println("Lowest cost project:");
        System.out.println(cheapestProject.display());
    }

    private static void SortEmployeesByLastName(ArrayList<Employee> employees) {
        for (int i = 0; i < employees.size(); i++) {
            Employee emp = employees.get(i);
            String target = emp.lastName;
            int j;
            for (j = i; j > 0 && employees.get(j - 1).lastName.compareTo(target) > 0; j--) {
                employees.set(j, employees.get(j - 1));
            }
            employees.set(j, emp);
        }

        for (Employee employee: employees) {
            System.out.println(employee.display());
        }
    }

    private static void SortProjectsByCost(ArrayList<Project> projects) throws Exception {
        // Insertion Sort O(n^2)
        for (int i = 0; i < projects.size(); i++) {
            Project project = projects.get(i);
            float target = project.projectCost;

            int j;
            for (j = i; (j > 0 && (projects.get(j - 1).projectCost < target)); j--){
                projects.set(j, projects.get(j-1));
            }
            projects.set(j, project);
        }

        for (Project project: projects) {
            System.out.println(project.display());
        }

        for (int i=1; i < projects.size(); i++) {
            if (projects.get(i).projectCost > projects.get(i-1).projectCost) {
                throw new Exception("Uh oh! not sorted!");
            }
        }
    }

    private static void AssignEmployeeToProject(ArrayList<Employee> employees, ArrayList<Project> projects) {
        // take two inputs from user to get employee and project. Add employee to list of assigned employees, add project to employee
        ArrayList<String> employeeIDs = new ArrayList<>();
        ArrayList<String> projectIDs = new ArrayList<>();
        String chosenEmployeeID;
        int chosenEmployeeIndex;
        String chosenProjectID;
        int chosenProjectIndex;

        while (true) {
            System.out.println("Choose the ID of an employee to assign");
            for (Employee employee: employees) {
                employeeIDs.add(employee.employeeId);
                System.out.println(employee.display());
            }
            Scanner scan = new Scanner(System.in);
            chosenEmployeeID = scan.nextLine().strip();
            if (!employeeIDs.contains(chosenEmployeeID)) {
                System.out.println("Please choose from the list of employees!");
                continue;
            }
            chosenEmployeeIndex = employeeIDs.indexOf(chosenEmployeeID);
            break;
        }

        while (true) {
            System.out.println("Choose the ID of the project that " + chosenEmployeeID + " will be added to:");

            for (Project project: projects) {
                projectIDs.add(project.projectId);
                System.out.println(project.display());
            }
            Scanner scan = new Scanner(System.in);
            chosenProjectID = scan.nextLine().strip();
            if (!projectIDs.contains(chosenProjectID)) {
                System.out.println("Please choose from the list of projects!");
                continue;
            }
            chosenProjectIndex = projectIDs.indexOf(chosenProjectID);
            break;
        }

        // Need to actually update the input arrays
        employees.get(chosenEmployeeIndex).assignedProject = projects.get(chosenProjectIndex);
        projects.get(chosenProjectIndex).assignedEmployees.add(employees.get(chosenEmployeeIndex));

        System.out.println("The following update has been made:");
        System.out.println("Employee " + chosenEmployeeID + " assigned to project " + employees.get(chosenEmployeeIndex).assignedProject.display());
        System.out.println("Project " + chosenProjectID + " assigned employees: ");
        for (Employee employee: projects.get(chosenProjectIndex).assignedEmployees) {
            System.out.println("\t" + employee.display());
        }

    }

}
