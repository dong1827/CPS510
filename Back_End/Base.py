from flask import Flask, request, session, json
from flask_cors import CORS
import oracledb
import Configs.Config as Config


app = Flask(__name__)
app.config.from_object(Config.Config)

CORS(app, supports_credentials=True)

#Establishing a database connection
def get_connection():
    username = "rdong"
    password = "05014760"
    dsn = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(Host=oracle12c.scs.ryerson.ca)(Port=1521))(CONNECT_DATA=(SID=orcl12c)))"

    try:
        #Try to connect to the database
        conn = oracledb.connect(user=username, password=password, dsn=dsn)
        return conn
    except oracledb.Error as e:
        print(f"An error has occured while connecting to database: {e}")

#Makes session permanent as long as the user leave their browser open
@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True

@app.route('/register', methods = ['post'])
#Try to register the user into the database and return whether it was success
def register(): 
    res_body = {"register": "fail", "Msg": "An error has occured"}
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    sql = "INSERT INTO Users (username, password) VALUES (:1, :2)"
    conn = get_connection()
    cursor = conn.cursor()

    #Trying to insert username and password into database
    try:
        cursor.execute(sql, (username, password))
        conn.commit()
        res_body["register"] = "success"
        res_body["Msg"] = "Succuessfully registered"
    #Add in custom message
    except oracledb.IntegrityError:
        res_body["register"] = "fail"
        res_body["Msg"] = "Username already exists"

    except ValueError as ve:
        res_body["register"] = "fail"
        res_body["Msg"] = f"Invalid input: {str(ve)}"

    except Exception as e:
        res_body["register"] = "fail"
        res_body["Msg"] = "An error has occured"

    return res_body
    


@app.route('/login', methods = ['post'])
#Try to log the user in and return whether it was successful or not 
def login():
    res_body = {"login": "fail"}

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    #Grab the user's password
    sql = "SELECT Password FROM Users WHERE Username = :1"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (username,))
    result = cursor.fetchall()

    #Check if the passwords match
    if result:
        if (result[0][0] == password): 
            session["user"] = username
            res_body["login"] = "success"

    return res_body

@app.route('/logout', methods = ['post'])
#Log the user out 
def logout(): 
    res_body = {"result": "None"}
    session.clear()
    res_body["result"] = "success"

    return res_body

@app.route('/session', methods = ['get'])
#Check if there's an active session
def get_session(): 
    res_body = {"session": "None"}

    if ("user" in session):
        res_body["session"] = session["user"]

    return res_body

@app.route('/create', methods = ['post'])
#Creating table
def create_table(): 
    res_body = {"result": "None"}

    #sql statements for each table
    sql_statements = [ 
        """CREATE TABLE Customer (
        Username VARCHAR2(25) PRIMARY KEY,
        Password VARCHAR2(25) NOT NULL,
        FirstName VARCHAR2(25) NOT NULL,
        LastName VARCHAR2(25) NOT NULL,
        Phone VARCHAR2(12),
        Email VARCHAR2(25))""",

        """CREATE TABLE StoreCredit (
        ID NUMBER PRIMARY KEY,
        Username VARCHAR2(25) REFERENCES Customer(Username) NOT NULL, 
        TransactionDate DATE NOT NULL,
        TransactionType VARCHAR2(25) NOT NULL, 
        Balance NUMBER DEFAULT 0)""",

        """CREATE TABLE Product (
        ProductID NUMBER PRIMARY KEY,
        Title VARCHAR2(25) NOT NULL, 
        ReleaseDate DATE NOT NULL, 
        Price NUMBER(15, 2) NOT NULL,
        Type VARCHAR2(5) NOT NULL)""",

        """CREATE TABLE Music (
        MusicID NUMBER PRIMARY KEY, 
        Artist VARCHAR2(25) DEFAULT 'unknown',
        Album VARCHAR2(25),
        FOREIGN KEY (MusicID) REFERENCES Product(ProductID))""",

        """CREATE TABLE Movie (
        MovieID NUMBER PRIMARY KEY,
        Director VARCHAR2(25) DEFAULT 'unknown', 
        Casting VARCHAR2(25),
        FOREIGN KEY (MovieID) REFERENCES Product(ProductID))""",

        """CREATE TABLE Genre (
        ProductID NUMBER REFERENCES Product(ProductID),
        Genre VARCHAR2(25) NOT NULL,
        PRIMARY KEY (ProductID, Genre))""",

        """CREATE TABLE Review (
        Customer VARCHAR2(25) REFERENCES Customer(Username) NOT NULL,
        Product NUMBER REFERENCES Product(ProductID) NOT NULL,
        Comments VARCHAR2(4000),
        Rating NUMBER CHECK (Rating BETWEEN 1 AND 5) NOT NULL,
        ReviewDate DATE NOT NULL,
        PRIMARY KEY(Customer, Product))""",

        """CREATE TABLE Stores (
        StoreID NUMBER PRIMARY KEY,
        Street VARCHAR2(25) NOT NULL,
        SNumber NUMBER NOT NULL, 
        FloorOfBuilding NUMBER)""",

        """CREATE TABLE Employee (
        EmployeeID NUMBER PRIMARY KEY,
        SINNUM VARCHAR2(9) UNIQUE NOT NULL, 
        FirstName VARCHAR2(25) NOT NULL,
        LastName VARCHAR2(25) NOT NULL, 
        Birthdate DATE NOT NULL, 
        StoreID NUMBER REFERENCES Stores(StoreID) NOT NULL)""",

        """CREATE TABLE Stocks (
        ProductID NUMBER REFERENCES Product(ProductID) NOT NULL,
        StoreID NUMBER REFERENCES Stores(StoreID) NOT NULL,
        StockCount NUMBER NOT NULL CHECK (StockCount >= 0),
        PRIMARY KEY (ProductID, StoreID))""",

    
        """CREATE TABLE Records (
        RecordID NUMBER PRIMARY KEY,
        ProductID NUMBER REFERENCES Product(ProductID) NOT NULL,
        Customer VARCHAR2(25) REFERENCES Customer(Username) NOT NULL,
        StoreID NUMBER REFERENCES Stores(StoreID),
        PurchaseDate DATE NOT NULL,
        Amount NUMBER(15, 2) NOT NULL CHECK (Amount >= 0),
        PaymentMethod VARCHAR2(25) NOT NULL)"""
    ]


    try:
        #execute the sql statements
        conn = get_connection()
        cursor = conn.cursor()
        for sql in sql_statements:
            cursor.execute(sql)
        
        conn.commit()
        res_body["result"] = "Successfully created tables"
    except oracledb.DatabaseError as e:
        error_obj, = e.args 
        res_body["result"] = error_obj.message
    

    return res_body
    

@app.route('/drop', methods = ['post'])
#Dropping table
def drop_table(): 
    res_body = {"result": "None"}
    sql_statements = [
    "DROP TABLE Customer CASCADE CONSTRAINTS",
    "DROP TABLE Employee CASCADE CONSTRAINTS",
    "DROP TABLE Genre CASCADE CONSTRAINTS",
    "DROP TABLE Movie CASCADE CONSTRAINTS",
    "DROP TABLE Music CASCADE CONSTRAINTS", 
    "DROP TABLE Product CASCADE CONSTRAINTS", 
    "DROP TABLE Records CASCADE CONSTRAINTS", 
    "DROP TABLE Review CASCADE CONSTRAINTS", 
    "DROP TABLE Stocks CASCADE CONSTRAINTS", 
    "DROP TABLE StoreCredit CASCADE CONSTRAINTS",
    "DROP TABLE Stores CASCADE CONSTRAINTS"
    ]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        for sql in sql_statements:
            cursor.execute(sql)
        conn.commit()
        res_body["result"] = "successfully dropped all tables"
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        res_body["result"] = error_obj.message
    

    return res_body

@app.route('/dummyData', methods = ['post'])
#Inserting dummy data
def dummy_data():
    res_body = {"result": ""}
    sql_statements = [
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('john_doe', 'securePassword123', 'John', 'Doe', '1234567890', 'john@example.com')",
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('jane_smith', 'anotherPassword456', 'Jane', 'Smith', '0987654321', 'jane@example.com')",
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('mark_jones', 'password789', 'Mark', 'Jones', '1122334455', 'mark@example.com')",
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('lucy_adams', 'pass4321', 'Lucy', 'Adams', '6677889900', 'lucy@example.com')",
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('emily_clark', 'pass1234', 'Emily', 'Clark', '5552223333', 'emily@example.com')",
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('david_brown', 'mypassword321', 'David', 'Brown', '4443332222', 'david@example.com')",
    "INSERT INTO Customer (Username, Password, FirstName, LastName, Phone, Email) VALUES ('john_doe2', 'securePassword123', 'John', 'Doe', '1234567890', 'john@example.com')",
    
    "INSERT INTO StoreCredit (ID, Username, TransactionDate, TransactionType, Balance) VALUES (1, 'john_doe', TO_DATE('2023-01-01', 'YYYY-MM-DD'), 'Initial Credit', 100)",
    "INSERT INTO StoreCredit (ID, Username, TransactionDate, TransactionType, Balance) VALUES (2, 'jane_smith', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'Initial Credit', 150)",
    "INSERT INTO StoreCredit (ID, Username, TransactionDate, TransactionType, Balance) VALUES (3, 'mark_jones', TO_DATE('2024-01-03', 'YYYY-MM-DD'), 'Initial Credit', 200)",
    "INSERT INTO StoreCredit (ID, Username, TransactionDate, TransactionType, Balance) VALUES (4, 'lucy_adams', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'Initial Credit', 250)",
    "INSERT INTO StoreCredit (ID, Username, TransactionDate, TransactionType, Balance) VALUES (5, 'emily_clark', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'Initial Credit', 300)",
    "INSERT INTO StoreCredit (ID, Username, TransactionDate, TransactionType, Balance) VALUES (6, 'david_brown', TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'Initial Credit', 175)",

    "INSERT INTO Product (ProductID, Title, ReleaseDate, Price, Type) VALUES (1, 'The Great Album', TO_DATE('2023-01-01', 'YYYY-MM-DD'), 19.99, 'Music')",
    "INSERT INTO Product (ProductID, Title, ReleaseDate, Price, Type) VALUES (2, 'Epic Movie', TO_DATE('2023-02-01', 'YYYY-MM-DD'), 14.99, 'Movie')",
    "INSERT INTO Product (ProductID, Title, ReleaseDate, Price, Type) VALUES (3, 'Greatest Music', TO_DATE('2023-03-02', 'YYYY-MM-DD'), 9.99, 'Music')",
    "INSERT INTO Product (ProductID, Title, ReleaseDate, Price, Type) VALUES (4, 'Jazzy Music', TO_DATE('2023-04-01', 'YYYY-MM-DD'), 19.99, 'Music')",
    "INSERT INTO Product (ProductID, Title, ReleaseDate, Price, Type) VALUES (5, 'Incredible Movie', TO_DATE('2023-05-01', 'YYYY-MM-DD'), 12.99, 'Movie')",
    "INSERT INTO Product (ProductID, Title, ReleaseDate, Price, Type) VALUES (6, 'Action Movie', TO_DATE('2023-06-01', 'YYYY-MM-DD'), 18.99, 'Movie')",

    "INSERT INTO Music (MusicID, Artist, Album) VALUES (1, 'Artist Name', 'The Great Album')",
    "INSERT INTO Music (MusicID, Artist, Album) VALUES (3, 'Band Name', 'Amazing Album')",
    "INSERT INTO Music (MusicID, Artist, Album) VALUES (4, 'Unknown Artist', 'Random Jazz Album')",

    "INSERT INTO Movie (MovieID, Director, Casting) VALUES (2, 'Another Director', 'Lead Actress')",
    "INSERT INTO Movie (MovieID, Director, Casting) VALUES (5, 'Famous Director', 'Famous Actor')",
    "INSERT INTO Movie (MovieID, Director, Casting) VALUES (6, 'Famous Director', 'Lead Hero')",

    "INSERT INTO Genre (ProductID, Genre) VALUES (1, 'Rock')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (3, 'Pop')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (4, 'Jazz')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (2, 'Action')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (2, 'Horror')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (5, 'Drama')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (6, 'Comedy')",
    "INSERT INTO Genre (ProductID, Genre) VALUES (6, 'Action')",

    "INSERT INTO Review (Customer, Product, Comments, Rating, ReviewDate) VALUES ('john_doe', 1, 'Great product!', 5, SYSDATE)",
    "INSERT INTO Review (Customer, Product, Comments, Rating, ReviewDate) VALUES ('jane_smith', 2, 'Loved it!', 4, SYSDATE)",
    "INSERT INTO Review (Customer, Product, Comments, Rating, ReviewDate) VALUES ('mark_jones', 3, 'This is fantastic!', 5, SYSDATE)",
    "INSERT INTO Review (Customer, Product, Comments, Rating, ReviewDate) VALUES ('lucy_adams', 4, 'We need more of this.', 4, SYSDATE)",
    "INSERT INTO Review (Customer, Product, Comments, Rating, ReviewDate) VALUES ('emily_clark', 5, 'Engaging story!', 5, SYSDATE)",
    "INSERT INTO Review (Customer, Product, Comments, Rating, ReviewDate) VALUES ('david_brown', 6, '', 4, SYSDATE)",

    "INSERT INTO Stores (StoreID, Street, SNumber, FloorOfBuilding) VALUES (1, 'Main St', 123, 1)",
    "INSERT INTO Stores (StoreID, Street, SNumber, FloorOfBuilding) VALUES (2, 'Second St', 456, null)",
    "INSERT INTO Stores (StoreID, Street, SNumber, FloorOfBuilding) VALUES (3, 'Third St', 789, 2)",
    "INSERT INTO Stores (StoreID, Street, SNumber, FloorOfBuilding) VALUES (4, 'Fourth St', 101, 1)",

    "INSERT INTO Employee (EmployeeID, SINNUM, FirstName, LastName, Birthdate, StoreID) VALUES (1, '123456789', 'Jane', 'Smith', TO_DATE('1990-05-15', 'YYYY-MM-DD'), 1)",
    "INSERT INTO Employee (EmployeeID, SINNUM, FirstName, LastName, Birthdate, StoreID) VALUES (2, '987654321', 'John', 'Doe', TO_DATE('1985-08-20', 'YYYY-MM-DD'), 2)",
    "INSERT INTO Employee (EmployeeID, SINNUM, FirstName, LastName, Birthdate, StoreID) VALUES (3, '564738291', 'Alice', 'Brown', TO_DATE('1995-07-10', 'YYYY-MM-DD'), 3)",
    "INSERT INTO Employee (EmployeeID, SINNUM, FirstName, LastName, Birthdate, StoreID) VALUES (4, '837291564', 'Bob', 'Williams', TO_DATE('1988-09-20', 'YYYY-MM-DD'), 4)",
    "INSERT INTO Employee (EmployeeID, SINNUM, FirstName, LastName, Birthdate, StoreID) VALUES (5, '135791113', 'Charlie', 'Green', TO_DATE('1992-03-11', 'YYYY-MM-DD'), 4)",
    "INSERT INTO Employee (EmployeeID, SINNUM, FirstName, LastName, Birthdate, StoreID) VALUES (6, '246810121', 'Sophia', 'White', TO_DATE('1987-11-05', 'YYYY-MM-DD'), 4)",

    "INSERT INTO Stocks (ProductID, StoreID, StockCount) VALUES (1, 1, 50)",
    "INSERT INTO Stocks (ProductID, StoreID, StockCount) VALUES (2, 2, 30)",
    "INSERT INTO Stocks (ProductID, StoreID, StockCount) VALUES (3, 3, 40)",
    "INSERT INTO Stocks (ProductID, StoreID, StockCount) VALUES (4, 4, 25)",
    "INSERT INTO Stocks (ProductID, StoreID, StockCount) VALUES (5, 4, 60)",
    "INSERT INTO Stocks (ProductID, StoreID, StockCount) VALUES (6, 4, 35)",

    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (1, 1, 'john_doe', 1, SYSDATE, 19.99, 'Credit Card')",
    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (2, 2, 'jane_smith', 2, SYSDATE, 14.99, 'Debit Card')",
    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (3, 3, 'mark_jones', 3, TO_DATE('2023-06-01', 'YYYY-MM-DD'), 9.99, 'Cash')",
    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (4, 5, 'lucy_adams', 4, TO_DATE('2023-06-01', 'YYYY-MM-DD'), 12.99, 'Credit Card')",
    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (5, 5, 'emily_clark', 4, TO_DATE('2024-06-01', 'YYYY-MM-DD'), 12.99, 'Credit Card')",
    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (6, 5, 'david_brown', 4, TO_DATE('2023-06-01', 'YYYY-MM-DD'), 12.99, 'Debit Card')",
    "INSERT INTO Records (RecordID, ProductID, Customer, StoreID, PurchaseDate, Amount, PaymentMethod) VALUES (7, 2, 'john_doe', 1, SYSDATE, 14.99, 'Credit Card')"
    ]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        for sql in sql_statements:
            cursor.execute(sql)
        conn.commit()
        res_body["result"] = "successfully inserted dummy data"
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        res_body["result"] = error_obj.message

    return res_body

@app.route('/query', methods = ['post'])
#Return the query result
def query(): 
    res_body = {"result": "Success"}

    data = request.get_json()
    query = data.get("query")

    try:
        sql = f"SELECT * FROM {query}"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description] 
        rows = cursor.fetchall()

        # Step 5: Format the response
        res_body["columns"] = columns
        res_body["rows"] = rows

        return res_body
    
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        res_body["result"] = error_obj.message
        res_body["rows"] = ""
        res_body["columns"] = ""

        return res_body
 
    finally:
        if conn:
            conn.close()

@app.route('/advQuery', methods = ['post'])
#Return an advanced query result
def adv_query(): 
    res_body = {"result": "Success"}

    data = request.get_json()
    query = int(data.get("query"))

    sql_statements = [
        """SELECT DISTINCT C.Username AS "Customer"
        FROM Customer C
        WHERE EXISTS (
            SELECT 1 
            FROM Records R 
            JOIN Product P ON R.ProductID = P.ProductID
            WHERE C.Username = R.Customer 
            AND P.Type = 'Music'
        )
        AND EXISTS (
            SELECT 1 
            FROM Records R 
            JOIN Product P ON R.ProductID = P.ProductID
            WHERE C.Username = R.Customer 
            AND P.Type = 'Movie'
        )""",

        """SELECT DISTINCT C.Username AS "Customer"
        FROM Customer C
        JOIN Review R ON C.Username = R.Customer
        UNION
        SELECT DISTINCT C.Username AS "Customer"
        FROM Customer C
        JOIN Records RD ON C.Username = RD.Customer""",

        """SELECT S.StoreID AS "Store ID", COUNT(R.ProductID) AS "Total Products Sold"
        FROM Records R
        JOIN Stores S ON R.StoreID = S.StoreID
        GROUP BY S.StoreID
        HAVING COUNT(R.ProductID) > 2""",

        """SELECT P.ProductID AS "Product ID", P.Title AS "Product Title"
        FROM Product P
        JOIN Review R ON P.ProductID = R.Product
        MINUS
        SELECT P.ProductID AS "Product ID", P.Title AS "Product Title"
        FROM Product P
        JOIN Records R ON P.ProductID = R.ProductID
        WHERE R.Customer = 'john_doe'""",

        """SELECT S.StoreID AS "Store ID", P.Type AS "Product Type", AVG(P.Price) AS "Average Price"
        FROM Product P
        JOIN Records R ON P.ProductID = R.ProductID
        JOIN Stores S ON R.StoreID = S.StoreID
        WHERE P.Type IN ('Music', 'Movie')
        GROUP BY S.StoreID, P.Type"""
    ]

    try:
        sql = sql_statements[query]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description] 
        rows = cursor.fetchall()

        # Step 5: Format the response
        res_body["columns"] = columns
        res_body["rows"] = rows

        return res_body
    
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        res_body["result"] = error_obj.message
        res_body["rows"] = ""
        res_body["columns"] = ""

        return res_body
 
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
