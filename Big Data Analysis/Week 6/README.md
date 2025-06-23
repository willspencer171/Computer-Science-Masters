# Weel 6: SQL, Distributed Data and Hadoop

## Weekly Learning Outcomes

1. Explain the models of databases for Big Data (MLO 4)
2. Explain how Big Data causes problems for analytics (MLO 4)
3. Explain how SQL databases can help represent a wide variety of data (MLO 4)
4. Explain how distributed computation approaches such as Hadoop can allow computation on huge volumes of data (MLO 4)

## Reading for this Week

### Lesson 1

None!

### Lesson 2

Chapter 4 of Harrison's *Next Generation Databases*

Chapter 5 of Harrison's *Next Generation Databases*

### Lesson 3

[What Is Big Data?](https://www.oracle.com/uk/big-data/guide/what-is-big-data.html)

[Defining architecture components of the Big Data Ecosystem](https://doi.org/10.1109/CTS.2014.6867550)

Seciont 12.3 of Ricardo and Urban's *Databases Illuminated*

## Table of Contents

1. [Constructing and Querying a Database](#constructing-and-querying-a-database)
    1. [CRUDding it](#crudding-it)
2. [Next Generation Databases](#next-gen-databases)
    1. [Document Databases](#document-databases-json)
    2. [Graph Databases](#graph-databases)
3. [Big Data, Hadoop and Distributed Computation](#big-data-hadoop-and-distributed-computing)
    1. [Hadoop](#hadoop)
    2. [Pros and Cons of Hadoop](#pros-and-cons-of-hadoop)

## Constructing and Querying a Database

So this is a lot about Structured Query Language (SQL) - the industry standard DDL/DML combo language. I firmly believe [W3 Schools](https://www.w3schools.com/sql/) is one of the best places to learn about it purely because it's such a simple language and W3 covers it all

### CRUDding it

Create, read, update and delete are the 4 most important operations of a database management system. Let's look at how it can be done in SQL

#### CREATE - Genesis

First, we need to define our database (hence database definition language DDL). A new table is made using CREATE:

```sql
CREATE TABLE Student (
    'studentID' INT NOT NULL,
    'firstname' TEXT,
    'surname' TEXT,
    'gender' VARCHAR(1),
    'DOB' VARCHAR(8),
    PRIMARY KEY 'studentID'
);
```

This creates a table in our database called Student. Excellent. Now we know what data fields and the types of those data fields are. Text is a variable length field type, while varchar is a fixed length. These field types are their domains, which can be defined by the user themselves if needs be. A good use case for this is with dates.

We can now insert data using INSERT:

```sql
INSERT INTO Student VALUES (
    1, 'Ross', 'Spectre', 'm', '2000/10/19'
)
```

There are a whole bunch of modifiers that are useful for these such as `OR IGNORE` which just ignores the operation if it causes an error, like if the value has already been added.

#### SELECT - Query

When it comes to reading data, we use a single, very powerful keyword called `SELECT`. We can use other keywords with this to create more powerful searches, but the main operation is SELECT:

```sql
SELECT attributes
FROM tablename
[WHERE conditions]
[GROUP BY columns]
[HAVING conditions] -- For aggregates based on group by operations
[ORDER BY columns];
```

Note here that all SQL statements end with a semicolon

When it comes to complex queries, you may need to join data from different tables. There are a few ways of doing this, the simplest being to retrieve your data `FROM` multiple tables and filter based on a condition. For example, joining on a key like the ID of a student is easy like this. The problem that comes with this is the computational cost - listing tables in the `FROM` clause does a cartesian product of your tables - expensive.

A better solution is to use [`JOIN`s](https://www.w3schools.com/sql/sql_join.asp) - there are 4 types of join. The first is the cartesian product as above, called the `FULL JOIN`. A common one is the `INNER JOIN`. A nice easy way of looking at the INNER, LEFT, RIGHT and OUTER (full) joins is using a venn diagram:

![JOINs](joins.png)

##### Aggregate Functions

Now, I'm sure by now you're used to using aggregate functions with Pandas. It also pays to know how to use them when actually selecting your data. These are used in the `SELECT` clause to return a function of whatever attribute is used. For example:

```sql
SELECT count(*), studentName
FROM STUDENTS
WHERE studentName = 'Ross'
```

would count all the instances of people called Ross. This may or may not be a lot.

Other aggregate functions include (but are not limited to):

- MIN()
- MAX()
- SUM()
- AVERAGE()

Aggregate functions (except count) ignore NULL values

#### UPDATE - Modification

This one works syntactically similar to the `SELECT` query builder. In fact, it partially uses a query to operate!

```sql
UPDATE tablename
SET attr1 = val1, attr2 = val2
[WHERE conditions]
```

Very simple! While it is optional, if you omit the `WHERE` clause you will update every record in the table, which can be good but often not what you want.

#### DELETE - Removal

This is a pretty simple one like update. Select the data you want to delete, and this will delete the record that matches the `WHERE` clause conditions.

```sql
DELETE FROM tablename
[WHERE conditions]
```

Again, omitting the `WHERE` clause will delete all records in the table, but not the table itself. This is similar to the `TRUNCATE` keyword

If you want to delete a table from your database, you can use the `DROP TABLE` keyword. This removes it from the database. You can also drop a database from the schema which is interesting (`DROP DATABASE`)

## Next-Gen Databases

SQL databases (RDBMSs) are great and all. However, they are rigid in their use cases. RDBMSs store your data based on an ideal *model* in such a way that you can query the database in a flexible way to get whatever data you'd like out of it. Because of the arbitrarily many ways to access your data (particularly after doing large numbers of joins across 3NF databases), this can become intensive, and no amount of vertical scaling (more computational power in one workstation) can beat it.

NoSQL is the next generation. It's technically more of a generalisation of the standard models of data storage - you can store things however you like and get them out however you like. But once you've decided how you're going to retrieve your data, that's the only way to go about it.

There's a few differences at play here. RDBMSs don't necessarily plan the storage of data around the data itself - it has a rigid structure of $N\times M$ tables that we access using SQL. In NoSQL, you plan the physical structure of the data around the data you're collecting. Some types of NoSQL are:

- Key/Value pairs
  - Yeah, just a big ol dictionary
  - The key references an arbitrary blob of data
- Document databases
  - Same as above, but the data are stored in a least semi-structured documents
  - XML document stores are good for the MS365 suite for Word, Excel, Powerpoint etc.
  - Relational databases actually make use of these by allowing for a long/BLOB attribute type and most RBDMS systems support XML querying by extension
- Graph databases
  - In this representation, graph nodes are made up of individual records. Between nodes are edges to represent connections between them all
  - This can be useful for representing hierarchical or network data that aren't as readily represented in a table form

### Document Databases (JSON)

These are a relatively simple object-oriented document database that uses JavaScript Object Notation (JSON) files to store the data. In document databases, a document is equivalent to a record. In that sense, it's quite easy to see that a document is actually just a single object in a JSON file. Each file can be used to group documents into distinct categories or for related purposes

Document databases look like this in their hierarchy of user-logical-physical layers:

![DocDB](/Images/DocDB.png)

JSON databases can be used in 3NF the same way that a relational database can. In fact, I'm not entirely sure what the difference is?

![Document Linking](/Images/doc_link.png)

Okay, so there are some other differences between relational databases and JSON (and other document types) databases.

#### Data Structure and Flexibility

So, relational DBs have schemas that describe how every row of data should look. They define the attributes and data types for each record and they are the same for each. In an object oriented database, each record is more flexible - there's no schema describing what each object should look like. A Person object could have attributes like age, name, shoe size, while another one could have hair colour, height and VO2 max (idk). They would both be valid as Person objects since there's no restrictive schema.

#### Data Normalisation vs Denormalisation

Normalising your data is really useful for keeping things consistent and structured. However, when your goal isn't necessarily consistency, but speed, embedding objects inside other objects to violate 1st Normal Form is desirable. In JSONs this is done by using a list of objects as an attribute of another object.

```JSON
{
  "name": "Alice",
  "orders": [
    { "item": "Book", "price": 10 },
    { "item": "Pen", "price": 2 }
  ]
}
```

#### Transaction Support

Relational DBs are built around ACID transactions

ACID? Atomic, Consistent, Isolated, Durable. Each transaction (an indivisible action that must either totally succeed or totally fail) must follow this strict rule.

In JSON and other document databases, transactions either aren't supported, or don't adhere so strictly to the ACID principle. Instead, there is BASE (Basic Availability, Soft-state - could be inconsistent for some time, Eventual consistency - will eventually return to consistent state)

Super lax.

### Graph Databases

Sometimes, the information in the database is less important than the relationships between the objects in the database. Think of Facebook - each individual is pretty much insignificant. The friends you make, the ones you tag in posts, the ones you follow, whose posts you like, share, comment on. These factors make up the web of social media, you just happen to be one of the *types* of nodes in it. The relationships are the likes, tags, comments and shares.

Graphs treat relationships (or edges or arcs) as objects with properties themselves. For example, the properties of a relationship between a person and a company could be the nature of their connection (employee), the duration of that connection, or any other information attached to it like wages or hierarchical position.

A node can also have multiple edges connected to another node. Let's say you have a person who worked at a company but got promoted at a certain point. Now, they have a new relationship with that company (would be represented in an RDBMS as a Contract) and the old contract still exists, it just has an end date equal to the start date of the new one.

The reason why we implement this as a graph in a *NoSQL* database system is because there isn't an easy way to perform a graph traversal in SQL. Sure, you can do it, but the comptational and space complexity quickly becomes unmanageable in a large enough network (think 6 degrees of separation). If the first traversal joins together 3 tables on a key, this is an $O(n^2)$ operation. Next traversal is $O(n^3)$ and so on. There often isn't enough memory space to find how many connections there are between you and Kevin Bacon.

What we use is the property graph. This is the technical term for the type of graph whose edges also have properties.

Neo4j is a tool that's particularly useful for managing these types of databases. It implements a database definition / manipulation language similar to SQL called Cypher. This allows the user to traverse the graph optimally to find nodes at the ends of connections.

This is all well and good, but sometimes we want a more procedural language for this purpose, since traversing a graph is inherently a procedural operation. Gremlin is an alternative that fulfils this requirement. It can also be used with Neo4j instead of Cypher.

When it comes to distributed computing, the overhead associated with communicating between different machines proves too inefficient to make the improvement in efficiency from adjacency graphs worthwhile. Typically, pure-graph databases are used on single-machine data, but if you want to distribute it, graphs can be integrated with Hadoop or Spark using Giraph and GraphX, respectively.

## Big Data, Hadoop and Distributed Computing

> *Big data is data that contains greater variety arriving in increasing volumes and with ever-higher velocity*. - Gartner, 2001

### The 5 Vs of Big Data

When it comes to defining Big Data, it's more or less about what typical systems are unable to compute - i.e. you can't process it on your laptop because it's just too much too fast. Big Datasets have 5 properties:

- Volume
  - The amount of data in the dataset
  - In big data, this can be huge numbers - petabytes and terabytes of data are normal in this domain
- Velocity
  - The speed with which data is received or acted on
  - There are millions of posts on Twitter and Instagram every day
- Variety
  - The types of data available
  - (Semi)-unstructured and structured data
- Veracity
  - The truthfulness of a dataset
  - These are linked to data quality and integrity
- Value
  - Data has intrinsic value but it is of no use if it remains undiscovered.

Big Data comes loaded with a few extra definitions. With the main three Vs above (Volume, Velocity and Variety) come new data models, new methods of analysing streamed data and new infrastructure for storage and processing. Much of this means that big data is difficult to actually deal with as an individual - it moves beyond the capabilities of a single workhorse and requires dedicated infrastructure for storage and distribution of processing power.

At the end of the day, Big Data is the gas that fuels the infrastructure used to refine, analyse, store, visualise and process it.

### Hadoop

Apache Hadoop is a big data processing framework, written in Java. In short, it excels in batch processing and large-scale data storage by using the HDFS (Hadoop Distributed File System) to distribute storage over a cluster of machines.

![Hadoop Architecture](/Images/hadoop.png)

#### HDFS - Storage

When you have large volumes of data, you need to consider where it'll all go. Data storage is relatively inexpensive compared with computing power, but a single machine won't handle petabytes of data.

Storage is therefore distributed across multiple machines and stored in the Hadoop Distributed File System.

HDFS splits your file into blocks of equal size. Each block is stored on a separate node (machine) in the cluster. Each block is replicated across all the nodes. Effectively, your file is stored in chunks, copied onto other machines for fault tolerance - if one node goes down, you have copies elsewhere. The data for your file is managed by a Name Node - a master server. This presents your data to you as a single file, when in reality it represents the copies of the file, split into blocks.

Using blocks to manage your data lays the groundwork for parallel processing - you can perform MapReduce on multiple machines and return the results. If your data is shared across 5 machines, processing effectively takes 20% of the time.

Below is the default behaviour of Hadoop for storing data across nodes, organised into racks:

![HDFS](/Images/HDFS.png)

Your dataset is divided into three blocks. The first replica of each block is placed on a node in a random rack (a rack being a collection of nodes on the same network switch). The second is placed in another rack on a random node, and the third is placed in the same rack as the second, on another node.

If the first node fails, it's assumed that the rack itself failed and the next node is accessed from the next rack. If this fails, it's unlikely that two complete racks have failed, so the third block is fetched from another node in that rack.

#### MapReduce - Processing

Two phases of operation occur here. The Map phase and the Reduce phase. The map phase breaks the data into chunks and the reduce phase is used to aggregate the results using a function.

![MapReduce Example](/Images/mapred.png)

#### YARN - Resource Management

I'm not going to go into detail about how exactly this works, but it just manages the reources that the cluster has available to it. In the case that you have a large team of people, resources are allocated fairly and different apps running on Hadoop like Spark or Hive also get allocated resources.

Hive is a data warehousing system that aims to emulate SQL but for big data - we can use HiveQL to query our big database!

#### Hybrid Approach

![Hybrid](/Images/hybrid_hadoop.png)

### Pros and Cons of Hadoop

Hadoop is really good at what it does:

- High Variety
- High Volume
- Cost effective
- Fault tolerant
- Parallelism

But it is not so good for other things:

- Real-time processing
  - Large datasets running on batch storage
  - Can lead to huge runtimes of hours or days
- Not transactional
- Complex data
  - If you have data that would be best represented as a graph, Hadoop is not necessarily the best way of going about it.
