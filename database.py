import sqlite3
import pandas as pd
conn = sqlite3.connect(r"Library.db")
c = conn.cursor()
cur = conn.cursor()


def initial():
### Puts all the data into the DB and normalises it ###
        c.execute('''CREATE TABLE Book_info (ID int, Genre text, Title text, Author text, Purchase_Price text, Purchase_Date text)''')
        data = pd.read_csv(r'Book_data.txt', encoding = 'unicode_escape',delimiter = "\t")
        # write the data to a sqlite table
        data.to_sql('Book_info', conn, if_exists='append', index = False)
        c.execute('''SELECT * FROM Book_info''').fetchall()

        c.execute('''CREATE TABLE Book_info_Purchase (ID int, Title text, Purchase_Price text, Purchase_date text)''')
        c.execute('''INSERT INTO Book_info_Purchase (ID, Title ,Purchase_Price, Purchase_Date) SELECT ID, Title, Purchase_Price, Purchase_Date from Book_info;''') 
        c.execute('''COMMIT;''')
        c.execute('''SELECT * FROM Book_info_Purchase''').fetchall()

        c.execute('''CREATE TABLE Book_info_Title (ID int, Title text, Genre text, Author text)''')
        c.execute('''INSERT INTO Book_info_Title (ID , Title , Genre , Author ) SELECT ID , Title , Genre , Author from Book_info;''') 
        c.execute('''COMMIT;''')
        c.execute('''SELECT * FROM Book_info_Title''').fetchall()

        c.execute('''DROP TABLE Book_info''')

        c.execute('''CREATE TABLE Reserve_table (Book_ID int, Reservation_Date text, Checkout_Date text, Return_Date text, Member_ID int)''')
        data = pd.read_csv(r'Reserve_table.txt', encoding = 'unicode_escape',delimiter = "\t")
        # write the data to a sqlite table
        data.to_sql('Reserve_table', conn, if_exists='append', index = False)
        c.execute('''UPDATE Reserve_table set Reservation_Date = NULL where Reservation_Date = '---' ''')
        c.execute('''COMMIT;''')
        c.execute('''UPDATE Reserve_table set Checkout_Date = NULL where Checkout_Date = '---' ''')
        c.execute('''COMMIT;''')
        c.execute('''UPDATE Reserve_table set Return_Date = NULL where Return_Date = '---' ''')
        c.execute('''COMMIT;''')

def initialOnCommand():
### Used to reset the DB ###
        c.execute('''DROP TABLE Book_info_Title''')
        c.execute('''DROP TABLE Book_info_Purchase''')
        c.execute('''DROP TABLE Reserve_table''')

        c.execute('''CREATE TABLE Book_info (ID int , Genre text, Title text, Author text, Purchase_Price text, Purchase_Date text)''')
        data = pd.read_csv(r'Book_data.txt', encoding = 'unicode_escape',delimiter = "\t")
        # write the data to a sqlite table
        data.to_sql('Book_info', conn, if_exists='append', index = False)
        c.execute('''SELECT * FROM Book_info''').fetchall()

        c.execute('''CREATE TABLE Book_info_Purchase (ID int PRIMARY KEY, Title text, Purchase_Price text, Purchase_date text) ''')
        c.execute('''INSERT INTO Book_info_Purchase (ID, Title ,Purchase_Price, Purchase_Date) SELECT ID, Title, Purchase_Price, Purchase_Date from Book_info;''') 
        c.execute('''COMMIT;''')
        c.execute('''SELECT * FROM Book_info_Purchase''').fetchall()

        c.execute('''CREATE TABLE Book_info_Title (ID int PRIMARY KEY , Title text, Genre text, Author text) ''')
        c.execute('''INSERT INTO Book_info_Title (ID , Title , Genre , Author ) SELECT ID , Title , Genre , Author from Book_info;''') 
        c.execute('''COMMIT;''')
        c.execute('''SELECT * FROM Book_info_Title''').fetchall()

        c.execute('''DROP TABLE Book_info''')

        c.execute('''CREATE TABLE Reserve_table (Book_ID int , Reservation_Date text, Checkout_Date text, Return_Date text, Member_ID int  )''')
        data = pd.read_csv(r'Reserve_table.txt', encoding = 'unicode_escape',delimiter = "\t")
        # write the data to a sqlite table
        data.to_sql('Reserve_table', conn, if_exists='append', index = False)
        c.execute('''UPDATE Reserve_table set Reservation_Date = NULL where Reservation_Date = '---' ''')
        c.execute('''COMMIT;''')
        c.execute('''UPDATE Reserve_table set Checkout_Date = NULL where Checkout_Date = '---' ''')
        c.execute('''COMMIT;''')
        c.execute('''UPDATE Reserve_table set Return_Date = NULL where Return_Date = '---' ''')
        c.execute('''COMMIT;''')





### BOOKSEARCH.PY STARTS ###

def searchfunc(title):
### Searches for the Title in the DB ###
    cur.execute("SELECT Book_info_Title.ID, Book_info_Title.Genre, Book_info_Title.Title, Book_info_Title.Author, Book_info_Purchase.Purchase_Price, Book_info_Purchase.Purchase_Date FROM Book_info_Title join Book_info_Purchase on Book_info_Title.ID=Book_info_Purchase.ID   where Book_info_Title.Title LIKE '%"+title+"%' OR Book_info_Title.Author LIKE '%"+title+"%' OR Book_info_Title.Genre LIKE '%"+title+"%' ")
    rows = cur.fetchall()
    return rows 

def NAsearchfunc():
    ### Searches for the Not Available Title in the DB ###
    cur.execute("select distinct Book_ID, Book_info_Title.Title, Book_info_Title.Author, Book_info_Title.Genre from Reserve_Table join Book_info_Title on Book_info_Title.ID=Reserve_Table.Book_ID where Return_Date is NULL and Checkout_Date is NOT NULL and Reservation_Date is NULL  group by Book_ID")
    rows = cur.fetchall()
    return rows

def Asearchfunc():
    ### Searches for the Available Title in the DB ###
    cur.execute("select  ID, Title, Author, Genre from Book_info_Title  except Select distinct Book_ID, Book_info_Title.Title, Book_info_Title.Author, Book_info_Title.Genre from Reserve_Table join Book_info_Title on Book_info_Title.ID=Reserve_Table.Book_ID group by Book_ID UNION select ID, Title, Author, Genre from Book_info_Title join Reserve_table on Book_info_Title.ID=Reserve_Table.Book_ID except SELECT distinct Book_ID, Book_info_Title.Title, Book_info_Title.Author, Book_info_Title.Genre from Reserve_Table join Book_info_Title on Book_info_Title.ID=Reserve_Table.Book_ID where Return_Date is NULL and Checkout_Date is NOT NULL and Reservation_Date is NULL  group by Book_ID")
    rows = cur.fetchall()
    return rows

### BOOKSEARCH.PY ENDS ###


### BOOKCHECKOUT.PY STARTS ###

def checkout(ID):
### Checks if book is available or not ###
### If its available then it returns NULL ###
    cur.execute("SELECT * FROM Reserve_table where Book_ID ="+ID+" AND Checkout_Date is NOT NULL AND Return_Date IS NULL")
    rows = cur.fetchall()
    return rows 

def Userhascheckout(ID,MID):
### Checks if book is available or not ###
### If its available then it returns NULL ###
    cur.execute("SELECT * FROM Reserve_table where Book_ID ="+ID+" AND Checkout_Date is NOT NULL AND Return_Date IS NULL AND Member_ID="+MID)
    rows = cur.fetchall()
    return rows 


def checkres(ID):
    ### Checks if someone made a reservation on it ###
    cur.execute("SELECT * FROM Reserve_table where Book_ID ="+ID+" AND Reservation_Date is NOT NULL AND Return_Date IS NULL AND Checkout_Date IS NULL")
    rows = cur.fetchall()
    return rows 

def didyoureserve(ID,User):
    ### Checks if the Member being served made an reservation ###
    cur.execute("SELECT * FROM Reserve_Table where Book_ID ="+ID+" AND  Reservation_Date is NOT NULL AND Return_Date IS NULL AND Checkout_Date IS NULL AND Member_ID="+User)
    rows = cur.fetchall()
    return rows 

def confirmres(ID,User,date):
    ### If book is available then checkout book ###
    cur.execute("INSERT INTO Reserve_table (Book_ID,Checkout_Date,Member_ID) Values("+ID+", '"+date+"', "+User+")")
    c.execute('''COMMIT;''')
    rows = cur.fetchall()

def changerestocheckout(ID,User,date):
    ### If you reserved it and now book is available then change reservation to checkout ###
    cur.execute("UPDATE Reserve_table SET Checkout_Date = '"+date+"', Reservation_Date= NULL WHERE Book_ID="+ID+" AND Member_ID="+User+" AND Return_Date IS NULL AND Checkout_date is NULL")
    c.execute('''COMMIT;''')

def reservbook(ID,User,date):
    ### If book is unavailable and no one reserved it then you can reserve ###
    cur.execute("INSERT INTO Reserve_table (Book_ID, Reservation_Date, Member_ID) Values("+ID+", '"+date+"', "+User+")")
    c.execute('''COMMIT;''')


### BOOKCHECKOUT.PY ENDS ###    



### BOOKRETURN.PY STARTS ###    

def returnbook(ID,date):
### If you checked out a book then you can return ###
    cur.execute("UPDATE Reserve_table SET Return_Date = '"+date+"' WHERE Book_ID="+ID+" AND Return_Date IS NULL AND Reservation_Date IS NULL")
    c.execute('''COMMIT;''')


### BOOKRETURN.PY ENDS ###  



### BOOKRSELECT.PY STARTS ###  


def mostFamGenre():
### Selects the most famous genre for the Librarian ###
    cur.execute("Select Count(Book_info_Title.Genre) , Book_info_Title.Genre from Book_info_Title join Reserve_table where Book_info_title.ID = Reserve_table.Book_ID GROUP BY Book_info_Title.Genre ORDER BY COUNT(Book_info_Title.Genre) DESC LIMIT 3")
    rows = cur.fetchall()
    return rows 

def mostFamBook():
### Selects the most famous Book for the Librarian ###
    cur.execute("select COUNT(Reserve_table.Book_ID), Book_info_Title.Title AS MOST_FREQUENT from Reserve_table join Book_info_Title WHERE Reserve_table.Book_ID=Book_info_Title.ID GROUP BY Book_info_Title.Title ORDER BY COUNT(Book_ID) DESC LIMIT 3 ")
    rows = cur.fetchall()
    return rows 

def buyBook(ID,Title,date):
### Responsible for buying new books and putting in DB ###
    cur.execute("INSERT INTO Book_info_Title (ID, Genre, Title, Author) VALUES ("+ID+", (Select genre from Book_info_Title where Title='"+Title+"' group by genre),'"+Title+"', ((Select Author from Book_info_Title where Title='"+Title+"' group by genre)))")
    c.execute('''COMMIT;''')
    cur.execute("INSERT INTO Book_info_Purchase (ID, Title, Purchase_Price, Purchase_Date) VALUES ("+ID+",'"+Title+"', (Select Purchase_Price from Book_info_Purchase where Title='"+Title+"' group by Title),'"+date+"')")
    c.execute('''COMMIT;''')

def bookbyGenre(Genre):
### Responsible for buying new books and putting in DB ###
    cur.execute("select Book_info_Title.Title from Book_info_Title where Book_info_Title.Genre= '"+Genre+"' group by Title")
    rows=cur.fetchall()
    return rows

### BOOKRSELECT.PY ENDS ###  


def didyoujustcheckedout(ID,User):
    cur.execute("SELECT * FROM Reserve_table WHERE Book_ID ="+ID+" AND Member_ID ="+User+" AND Checkout_Date is NOT NULL AND Return_date is NULL")
    rows = cur.fetchall()
    return rows 

### Shared Functions ###
########################
def ListOfBookIDs():
    cur.execute("SELECT ID from Book_info_Title")
    rows=cur.fetchall()
    return rows

def countOfBookIDs():
    cur.execute("SELECT Count(ID) from Book_info_Title")
    rows=cur.fetchall()
    return rows[0][0]



def test_countOfBookIDs():
    assert countOfBookIDs()!=''

def test_ListOfBookIDs():
    assert ListOfBookIDs()!=''

def test_didyoujustcheckedout():
    assert didyoujustcheckedout('8','1234')!=''

def test_bookbyGenre():
    assert bookbyGenre('Horror')!=''

def test_mostFamBook():
    assert mostFamBook()!=''

def test_confirmres():
    assert confirmres('8','6655','13/11/2022')!=''

def test_Userhascheckout():
    assert Userhascheckout('8','1022')!=''


if __name__ == "__main__":
    test_countOfBookIDs()
    test_ListOfBookIDs()
    test_didyoujustcheckedout()
    test_bookbyGenre()
    test_mostFamBook()
    test_confirmres()
    test_Userhascheckout()
    print("Everything passed")
