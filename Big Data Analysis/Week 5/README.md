# Week 5: Databases, Schemas and Normalisation

## Weekly Learning Outcomes

1. Describe the relational database model (MLO 2)
2. Explain the problems caused by data that is too large for RAM (MLO 2)
3. Explain how Big Data causes problems for analytics (MLO 2)

## Reading for this Week

### Lesson 1

Chapter 1 of Lemahieu's Principles of Data Management

Chapter 4 of Lemahieu's Principles of Data Management

### Lesson 2

Sections 3.3, 3.4 and 6.1 from Lemahieu's Principles of Data Management

### Lesson 3

Chapter 6, pp. 111-121 of Lemahieu's Principles of Data Management

## Table of Contents

1. [Why Databases?](#why-databases)
    1. [Files vs DBMS](#files-vs-dbms)
    2. [Elements of a DBMS](#elements-of-a-dbms)
2. [Modelling Data and the Relational Database Model](#modelling-data-and-the-relational-database-model)
    1. [The Entity Relationship Diagram](#the-entity-relationship-diagram-erd)
    2. [The Enhanced ERD](#the-enhanced-erd-eer)
    3. [UML Class Diagram](#the-uml-class-diagram)
    4. [The Relational Model](#relational-model)
3. [Database Normalisation](#database-normalisation)
    1. [Why We Need Normalisation](#why-we-need-normalisation)
    2. [Normal Forms](#normal-forms)

## Why Databases?

It sounds kind of obvious doesn't it? Why databases? Well, it's not really that simple depending on how you're defining things.

Data come in various forms, naturally. And storing these data can be a complex problem of its own. When you have a bunch of data about a particular collection of things, they can become interconnected and *related* to one another. Let's say we have an Experiment. An Experiment could be run at 25°C for 25 minutes. All well and good so far because these are fundamental units. Think primitive types in a coding language. As soon as you introduce something else like, for example, the Person running the experiment, you have data about those Persons. Now there's a relationship between the entities being described by some data.

### Files vs DBMS

When you're starting out in data, you're probably going to use a CSV to store all your data about something. And that's fine. You can write to it, read from it and do just about anything you need with it, as long as the data you're storing can be represented by strings. If they can't - e.g. your data are represented by another set of data - then you need something different - enter the DataBase Management System (DBMS). This is a software package that is used to manage the relationships between your data. Now, you've got a type of object called an Experiment, and one called Scientist. You have data about both, and they can each be linked to the other via what's known as a foreign key - a unique identifier that points to the ID of an instance of another object.

What this means is that, technically, you can still have your data stored in CSVs. There's nothing wrong with that. Each file will represent a type of object and a collection of these files will be your database, which can be managed by a DBMS.

The problem arose when applications were using the same information about the same things, but weren't using them from the same source.

![File System](/Images/file_system.png)

This lead to duplicated data! Redundant data is bad for a number of reasons. Firstly, storage is not free or infinite. Second, changing data about a person in one file doesn't change it in another file - now your data about the same person is different!

Let's say you have Will Spencer, a customer of this company. They've bought something from online checkout and given their name as Will Spencer. Next, they sign up to the GIS system using the same login details as before, automatically filling their name as Will Spencer. Great! But what if Will Spencer wants to go by a cooler name like Ross Spectre? He goes to change it using his login for the GIS system and does so. Now, we have a Will Spencer and a Ross Spectre using the same Customer ID? You'd expect data about an entity to change universally if those data are used in another application, right?

A DBMS can be used to keep this in line. Separate the User object out and keep ID and Name as attributes. Now, whenever the Invoice, CRM or GIS systems need to change or access Will Spencer, they do so with the same person. Now, Will Spencer becomes Ross Spectre and is known for his cool-sounding spy name, wherever the GIS tracks him to.

![DBMS](/Images/dbms.png)

One of the main advantages that a DBMS provides is data querying and data retrieval. In a file-based system, we'd have to write logic in each application for CRUDing its related file. To do this, we open the file, read the whole file, do a check to see if a row's attributes match the search criteria and move on. The same sort of thing continues, but the code itself is laborious, especially if you have to repeat it a lot (think DRY - don't repeat yourself).

Enter SQL - Structured Query Language. This is the language of many many DBMSs (see chapter 7 of Lemahieu for more of it). In principle, however, it just simplifies the syntax for making selections, updating entries, deleting entries and managing the entire database. We see the database as a collection of tables, where each table represents an entity and its instances. If we want to search for an Experiment called "Double Slit Experiment", we can use the code

```sql
SELECT *
FROM Experiments
WHERE name = 'Double Slit Experiment'
```

Which, it has to be said, is really simple and easy to read.

### Elements of a DBMS

A database is a structure. We can provide a high-level structure of what we expect the data in the database to look like. This description of the data is known as the **database model**, or **schema**. The **database state** or **set of instances** represents the actual data in the database. In terms of just DBMS, this is less important than the model or schema. Earlier I mentioned CRUD - Create, Read, Update, Delete. These are the 4 main operations that can be completed on data themselves. Anything else is strictly outside the scope of a DBMS.

#### Data Model / Schema

The conceptual data model provides a high-level description of entities, their attributes, and their relationships. These are often represented visually in an Entity Relationship diagram, or as an object-oriented model.

A logical data model translates the conceptual model for a specific implementation of the database. These can still be understood by business users, but are more closely linked to the physical structure/organisation of the data. Logical data models are typically relational, object-oriented, XML-based, NoSQL-based or hierarchical. Special shoutout to CODASYL, whatever that is.

An external data model contains subsets of the data items in the logical model and often acts as an interface between the DBMS and applications using it.

#### The Three Layer Architecture

When it comes to making applications for databases, we typically use a three-layer architecture to separate the external layer and internal layer via a conceptual layer.

The external layer includes the external data model which includes views of the logical data model - subsets of the entire database as mentioned before. This is useful for implementing separation of concerns such that different types of user can only access the bits they need to access.

The internal layer contains the internal data model, which describes how the data are stored physically.

The conceptual layer defines data items, essentially giving meaning to the raw data stored in the internal layer.

Ideally, the three layers should be independent of one another - changes in the physical layer shouldn't change how the logical layer works, and the view layer shouldn't have any bearing on how the physical structure of the data is shaped.

##### The difference between the logical and conceptual layers

While often used interchangeably, there is a distinction to be made between these two.

The conceptual layer represents a higher level view of the database and describes how entities in the database look. It focuses on what data is stored in the database

The logical layer is a similar thing, but more with respect to the logical implementation of the database. Being specific to the logical implementation, this defines how tables, columns and relationships look.

The line is blurred more in some implementations - relational databases only really define the logical layer, while object-oriented ones might define both distinctly.

#### The Catalogue

This is where all the metadata of a database is stored. It's the definitions of the view, logical and internal data models and aims to synchronise these models for consistency

## Modelling Data and the Relational Database Model

### The Entity Relationship Diagram (ERD)

When it comes to modelling our database, it can be really helpful to have a diagram that breaks down how the database will look. This is entirely conceptual and nonspecific to any data definition or manipulation languages (DDL and DML). They break our database down into the following components:

- Entities
  - Weak entities depend on a strong entity to exist
- Attributes
  - Simple attributes
  - Multivalue attributes
  - Derived attributes
  - Key attributes
  - Composite key attributes
- Relationships
  - One-to-one
  - One-to-many
  - Many-to-many
    - Often broken down to two 1-M relationships with an intermediary entity
    - Like shop items with customers. An item may be bought by many customers and many customers may buy an item.
    - Link them with a Transaction object and the many to many disappears
  - The relationship itself may have attributes

The ERD falls short in some places:

- Temporal/sequential logic cannot be represented
  - For example, a student cannot enrol in more than 4 modules per semester
- In fact, pretty much any logic cannot be represented by the ERD
  - What is represented is different types of relationship like contains

### The Enhanced ERD (EER)

This is an extension of the ER model that includes the original three components (entities, relationships and attributes) as well as three more (specialisation/generalisation, categorisation and aggregation).

In fairness, you'll recognise these concepts from the software engineering module in class entity diagrams.

#### The Specialist General

Specialisation refers to the concept of entity subclassing - i.e. the *"is a type of"* relationship.

Consider an Artist. We can specialise an Artist as a Singer or a Painter or Actor. These are all *types of* Artist. Each of these subclasses can be treated as entities, each with their own attributes and relationships to other entities (a Singer is part of a Band, a Painter created a Masterpiece, an Actor starred in a Movie). Each of these subclasses inherits attributes from their superclass.

The antithesis of this concept is generalisation or abstraction. It's just specialisation in the opposite direction. Both are processes that represent the same thing from different perspectives.

![General Spec](/Images/gen_spec.png)

The diamond between Actor and Movie represents the many to many relationship.

There are a few types of specialisation

- Overlap Specialisation
  - One entity may be a member of more than one subclass
  - i.e. an Artist is allowed to specialise as a Singer and an Actor
- Total Specialisation
  - Every entity in the superclass must be a member of some subclass
  - i.e. an entity must be a subclass of the superclass - an Artist must be one of Singer, Painter or Actor
- Partial Specialisation
  - This allows an entity to only belong to the superclass without having to be a member of the subclass
  - i.e. an entity can be an Artist without being a Singer, Painter or Actor

#### Categorisation

A category is a subclass that has several *possible* superclasses. For example, an account holder can inherit from either a Person or Company. That is to say that every Account Holder must be a Person or Company. Total categorisation means that every Person or Company is an Account Holder and partial categorisation means that not every Person or Company is an Account Holder

![Categorisation](/Images/categorisation.png)

#### Aggregation

Here, entity types that are related by a particular relationship can be combined/aggregated into a higher-level aggregate entity type. This is similar in nature to interfaces in Java, I think.

Let's look at an example. A consultant works on 0 to N projects and a project is being worked on by 1 to M consultants. This relationship (many to many) and the entities involved can be aggregated into a group that works like an entity - it has its own attributes. Let's call this Participation. Now this can have its own relationships as well. A Participation acts as a link to a Contract. One Participation has one Contract, while one Contract can be based on 1 to M participations of Consultants - essentially each Consultant has a Contract via Participation.

![Aggregation](/Images/aggregation.png)

Let's put it all together!

![EER Example](/Images/EER_ex.png)

### The UML Class Diagram

We've gone into the Entity Relationship Model here. We can also have a look at the more general UML (Unified Modelling Language) that's used for a whole range of diagrams. In this case, we'll be looking at the Class Diagram.

Here, we're looking at an Object-Oriented approach to database modelling. While each class equates to an entity type and each object equates to an entity, that's where the similarities end. We have variables that belong to a class and we have methods. The methods are the real flexibility of this modelling approach. We can tell people what the classes *do*.

These methods are actually the key point of encapsulation. They protect the variables from being edited or retrieved in a way that is unexpected. For example, a variable may have a getter and a setter method. The getter would retrieve the information (with flexibility for extra calculations, providing information like Age at runtime based on the date and DoB) and a setter would ensure the information being entered is correct for the variable.

A UML class is simple. Just a box subdivided into three. One for the name, one for the variables and one for the methods:

![UML Class](/Images/class.png)

The types of variables that can be modelled (and how) are listed:

- Key variables
  - There are none! Since an OO DBMS creates an object with an immutable Object ID (OID), this OID is taken to be the identifier
  - No more composite keys!
- Unique variables
  - While a variable cannot be declared as a key variable, you can still have unique ones by placing a constraint using OCL
- Composite variables
  - Okay, so no composite keys but a composite variable? Let's go!
  - Option 1 - decompose into their parts
  - Option 2 - create a new *domain* for that variable
- Multivalued variables
  - Can be modelled in two ways
  - Option 1 - Indicate multiplicity (like [0..4])
  - Option 2 - Aggregation
- Derived Variables
  - Indicated using a forward slash /

Ngl to you, the assessment doesn't want us to use UML class diagrams so I'm going to move past this. I'm done.

### Relational Model

This has a trong foundation in mathematical concepts - particularly set theory and first order predicate logic. Not things I know much about.

There's no graphical representation for this, unlike the ER and EER models so it isn't suitable as a conceptual data model. Just logical.

#### The Basics

A database is represented as a collection of relations. A relation is a set of tuples that each represent a real-world entity like a product, customer, supplier etc.

A relation can be looked at like a table of these values. Each tuple represents an instance of an entity and is a row in the table. We give each positional value in the tuple a name to represent the column names in the table. It sounds confusing but it's literally just a table as you know it.

So to map this to the EER model:

- Relation = Entity type
- Tuple = Entity
- Column = Attribute type
- Cell = Attribute value

#### Formal Definitions

Before we move on, let's define a domain. This specifies the range of permitted values for an attribute type. This is essentially all the values allowed. For an integer, this could be a value between 1 and 10. For sex it's the set containing male and female (plus others). For countries it's the set of all countries in the world. Do you see where I'm going here? Sets!

Each attribute type is defined using a domain. Dates are a year, followed by a month, then a day, each with their own set of values dependent on each other.

A relation is a set of m tuples, where each tuple contains n values. We have an m x n matrix! Each value is an element of the corresponding domain or is a NULL value

$$R(A_1, A_2, \dots, A_n) = \{t_1, t_2, \dots, t_m\}\\\text{where}\ t=<v_1, v_2, \dots, v_n>$$

$$v_i\isin \text{dom}(A_i)$$

So, mathematically speaking, a relation (table) is a subset of the cartesian product of the domains that comprise it.

#### Keys

There are lots of different types of key in the relational model. The simplest types are superkeys and keys.

A superkey is a set of values in the tuple that make it uniquely identifiable. The maximal superkey is just the whole tuple being used as a key. In the opposite direction, we have the minimal key. This is the smallest subset of the tuple that can be used to uniquely identify the tuple. It's easiest to use a unique ID value for this, but a superkey can be a useful composite key replacement.

A candidate key is an identifiably unique attribute of a tuple. For example, the ID could be unique, but so could the name of a product. In which case, they are both candidate keys. One is chosen to be the primary key of that relation. This key is used to establish connections to other relations. It can be used to define indexes in the storage model which is interesting. These should always be a NOT NULL value. Every candidate key that is not the primary key is an alternative key.

Foreign keys are those that are used to identify tuples in other relations. For example, each Card belongs to a Set, and each Set contains many cards. This is a one to many relationship. The primary key of a Set can be used in the Card as a foreign key to identify the Set that it belongs to. The Set relation does not contain multiple values for the Cards that are contained within as multivalued attributes are not permitted in the relational model.

If we have a many to many relationship, this can't be modelled by using foreign keys since each relation would need multivalued attributes to relate the two. Instead, what we do is create an intermediary relation which includes the two foreign keys and the attributes that pertain to each specific pairing of those foreign keys:

![N:M relationships](/Images/many_to_many_rel.png)

What's important to recognise in this is that a table (relation) can be used to describe an entity type OR a relationship type. In the case of the above, the new relation is a relationship between the Supplier and Product using the *verb* Supplies. Read like "These suppliers supply these products"

## Database Normalisation

The goal of this lesson will be to learn how to progress a database from First Normal Form to Third Normal Form. This is a method that reduces data redundancy.

### Why We Need Normalisation

It's actually kind of the whole point of using a DBMS really. To reduce redundancy and anomalies.

#### Types of Anomaly

We have 3 main types of anomaly that occur in non-normalised databases:

- Insertion
- Deletion
- Update

Let's have a look at an example.

![Non-normalised data](/Images/non_norm.png)

Let's say we change the room in the first row from H221 to B007. Seemingly innocuous. However, we haven't also updated the third row. Now the same class is occurring in two different places :/

Next, a deletion anomaly. Remove the second row and you'll find that you no longer have any information about the class HCI101b. That's it, that course doesn't exist now!

Finally an insertion anomaly. Let's say we want to create a new course but nobody has signed on yet. You can fill in all the relevant information for the course, yet it still wouldn't be valid since no student has signed on to it, thus failing to create a composite key.

### Normal Forms

#### First Normal Form

1NF (normal form) is simple and relatively obvious. Atomic data cells. Whaaaaaat no way! What does that mean?

It means no lists. No saving lists in your cells. It also means you can't have a series of columns that hold the same type of data - you can't just expand a list into columns. If you have a student and they're enrolled onto many courses, you can expand it into its own relation such that each row is just a tuple of the student's ID and the course ID. This is a composite key that can be used to identify the course-student pairing.

> Functional Dependencies occur in a relation when you can determine the value of one attribute from another. For example, you can determine the name of a student from their student ID (if you know how they're mapped, of course).
>
> This is helpful to know when looking into 2NF

#### Second Normal Form

For something to be in second normal form, it must already be in first normal form.

2NF is the removal of partial functional dependencies. When I explained an example of a functional dependency (name from student ID), it's clear to see that the name of a student is not dependent on the class ID. It seems obvious to point it out, really.

Second normal form is about removing functional dependencies that are not fully dependent on all components of the relation's key. In the table pictured way above, the composite key is not suitable.

We should identify the partial dependencies and the total dependencies. Total dependencies can stay, but partial dependencies should be removed with the key component they are dependent on and placed in a separate relation

![Second Normal Form](/Images/2NF.png)

#### Third Normal Form

3NF is about removing transitive dependencies. In 2NF, we removed partial dependencies. A transitive dependency is a functional dependency where the dependent relies on a determinant that is not part of the key. For example, if class is in a room with a Room ID, and the class also has an attribute called Room Name, then that room name is dependent on the room ID, not the class ID. It should then be removed and the Room ID be used as a foreign key pointing to the Room relation.

#### So, to conclude

- First Normal Form
  - This is about atomicity
  - All attributes should be singular
  - Remove duplicate attributes and place them in a long form relation
- Second Normal Form
  - Removal of Partial dependencies
  - If an attribute is not fully dependent on the key, get rid
- Third Normal Form
  - Removal of transitive dependencies
  - If an attribute is dependent on another attribute, get rid.
