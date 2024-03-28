
import javax.swing.*;
class Driver3 {
  public static void main(String args[]) {
      Person p = new Person();
      p.setForename("Fred");
      p.setSurname("Bloggs");
      p.setAge(23);
      PDemoSwing pfr = new PDemoSwing("Person GUI",p);
      pfr.setLocation(200,200);
      pfr.setVisible(true);
      AgeSlider asl = new AgeSlider("Person Age",p);
      asl.setLocation(400,400);
      asl.setVisible(true);
      
      //Input control
     while (true)
     {
     
      String forename = JOptionPane.showInputDialog("Please enter your forename");
      p.setForename(forename);
      
      String surname = JOptionPane.showInputDialog("Please enter your surname");
      p.setSurname(surname);
      
      String inputValue = JOptionPane.showInputDialog("Please enter your age");
      int age =Integer.parseInt(inputValue);
      p.setAge(age);
      
      }
      //end of input control
      /*
      System.out.println("Slight delay - then change the age");
      for(int i=0; i< 500000000; i++);
      p.setAge(32);
      System.out.println("Slight delay - then change the forename");
      for(int i=0; i< 500000000; i++);
      p.setForename("Freda");
      System.out.println("Slight delay - then change the surname");
      for(int i=0; i< 500000000; i++);
      p.setSurname("Bloggetta");*/
  }
}

