class Driver1 {
    public static void main(String args[]) {
	Person p = new Person();
	p.setForename("Fred");
	p.setSurname("Bloggs");
	p.setAge(23);
	PDemoSwing pfr = new PDemoSwing("Person GUI",p);
	pfr.setLocation(200,200);
	pfr.setVisible(true);
	System.out.println("Slight delay - then change the age");
	for(int i=0; i< 500000000; i++);
	p.setAge(32);
	System.out.println("Slight delay - then change the forename");
	for(int i=0; i< 500000000; i++);
	p.setForename("Freda");
	System.out.println("Slight delay - then change the surname");
	for(int i=0; i< 500000000; i++);
	p.setSurname("Bloggetta");
    }
}

