# DaoGenerator

This project's purpose is to serve as a polyglottal-generation of code in different languages to ease the
development of database-querying web-applications.

*History*

In the early 2000's, the de facto mechanisms to perform CRUD-type functionality against a database in the Java "universe" was either through GOF ("Gang-of-Four") design patterns or Enterprise Java Beans. EJBs added a lot of maintenance overhead to projects I've been on and many preferred a lighter-weight approach; hence why design pattern-based objects like DAOs (Data Access Objects), DAOImpls (DAOs are Java interfaces and thereby require an implementation class, hence the suffix 'Impl') and so forth were used.

In 2012, I was on a project wherein I needed to autogenerate as much code as possible and decided to write a very simplified series of Python modules that accomplished this task. The DaoGenerator project itself is an evolution of the these ideas and since I come from a largely Java-centric background, I chose to use Java and T-SQL conventions in the code that this project generates.

The project itself utilizes a series of JSON-based configuration files under the `config` directory. The mechanisms that are used to format the SQL and Java code are in the `config\templates` directory. These are written in the Jinja2 templating 'dialect'. Jinja2 is the only dependency that this project has..

The project uses POSIX-like flags to determine which files will be generated. The following table explains the meaning of these flags:

| Flag                        | Meaning                                                        |
|-----------------------------|----------------------------------------------------------------|
| `generate-table-sql`        | Generate the SQL script that create the tables in the database.|
| `generate-view-sql`         | Generate the SQL script that create the views in the database. |
| `generate-stored-procedures`| Generate the SQL script that create the stored-procedures.     |
| `generate-alter-table-sql`  | Generate the SQL script that alter the underlying tables so as to add foreign-key constraints.                                                                                   |
| `generate-delete-table-sql` | Generate the SQL script that deletes all data in the database's tables (for cleansing, rebuilding and refactoring processes).                                                         |
| `generate-drop-table-sql`   | Generate the SQL script that drops all of the tables in the database. |
| `generate-value-objects`    | Generate the Value Object java classes.                         |
| `generate-dao`              | Generate the DAO interfaces.                                   |
| `generate-dao-impls`        | Generate the DAOImpl Java classes.                              |
| `all`                       | Generate all of the above.                                      |

*Installation steps*

1. Ensure that `pip` is installed correctly. Issue the following command:
`pip install -r requirements.txt`
2. After the installation completes, modify the JSON configuration files to fit the database structure and underlying requirements.
3. Run the project by issuing the following command: `python main.py -m <flag defined above>`
