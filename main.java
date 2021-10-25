import java.util.*;
class employee
{
     private String employeid;
     private String empname;
     private int basicsalary,advance,netsalary;
     public void read()
     {
        Scanner scan= new Scanner(System.in);
        System.out.println("Enter the employee id");
        employeid=scan.next();
        System.out.println("Enter the employee name");
        empname=scan.next();
        System.out.println("Enter the basic salary of an employee");
        basicsalary=scan.nextInt();
        System.out.println("Enter the amount employee take advance");
        advance=scan.nextInt();
        calculate();
     }
     public void calculate()  
     {
        
        netsalary=basicsalary-advance;
     }
     public void display()  
     {
        System.out.println("Employeeid:"+employeid);
        System.out.println("Employeename:"+empname);
        System.out.println("Basicsalary:"+basicsalary);
        System.out.println("Advance:"+advance);
        System.out.println("NetSalary:"+netsalary);
             

     }
 
}
class main 
{
     public static void main(String args[])
     {
         employee employeobj=new employee();
         employeobj.read(); 
         employeobj.display();
     }
}