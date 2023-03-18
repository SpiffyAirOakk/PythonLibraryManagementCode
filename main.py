#################################
######### MAIN GUI PART #########
#################################
## No direct link to DB except for one count function ##
## Other modules using DB ##
import urllib.request
import json
import tkinter as tk
from tkinter import ttk 
from tkinter import *
import bookSearch
import database
import bookCheckout
import bookReturn
import BookSelect
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')


def clock():
        '''Clock Fucntion'''
        timenow = datetime.now()
        timeTem = timenow.strftime('%H:%M:%S')
        time_label.config(text=timeTem)
        time_label.after(200, clock)

def weatherupdate(Weather_label):
        '''Weather Function'''
        try:
            resp=urllib.request.urlopen(req).read()
            jsonResponse = json.loads(resp.decode('utf-8'))
            Temp=str(int(jsonResponse['main']['temp']-273))
            Sky=str(jsonResponse['weather'][0]['description'].capitalize())
            Weather_label.config(text= city_name+' | '+Temp+chr(176)+'C | '+Sky)
        except:
            Weather_label.config(text='Please Connect the Internet For weather Updates')
    
## FOR WEATHER AND TIME ##
today = datetime.today()   # Just using system date and time 
try:
    api_key = "2c91945b776625fdf1925d32af71ad75"    # Connecting to API and getting a response for weather
    city_name='Loughborough'
    req = urllib.request.Request(url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid='+api_key)
except:
    print('No INTERNET')
#########################

## Welcome Page ##
##################
def page1(root):   # Main page that hosts all the things
    '''
    Main welcome Page
    Links to 4 out of 5 other pages
    '''
    def DBinnit():
        '''DB initialize function'''
        database.initialOnCommand()
        db_label=tk.Label(home_frame,text='DB Initialised',bg='Pink')
        db_label.pack()
        db_label.after(1500, db_label.forget)
    
    home_frame=tk.Frame(root,bg='Pink')
    top_Frame=tk.Frame(home_frame,bg='BLACK')
    Welcome_label=tk.Label(top_Frame, text="WELCOME LIBRARIAN",font=("Arial", 50),foreground="WHITE",bg="BLACK")
    Welcome_label.pack()
    global time_label
    time_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    time_label.pack(anchor=SE)
    Weather_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    weatherupdate(Weather_label)
    Weather_label.pack(anchor=E)
    top_Frame.pack(anchor=N, fill=BOTH)
    clock()
    Desc_lable1=tk.Label(home_frame,text='Welcome to the Library Database Management System',bg='Pink',font=("Arial", 25,'italic'))
    Desc_lable1.pack()
    Desc_lable2=tk.Label(home_frame,text='Press Any of the button to continue',bg='Pink',font=("Arial", 25,'italic'))
    Desc_lable2.pack()
    Nav_button1=tk.Button(home_frame, text = 'Search', command = changepage,font=("Arial", 14))
    Nav_button1.pack(padx=5,pady=5)
    Nav_button2=tk.Button(home_frame, text = 'Checkout Book', command = changepage2,font=("Arial", 14))
    Nav_button2.pack(padx=5,pady=5)
    Nav_button4=tk.Button(home_frame, text = 'Return Book', command = changepage3,font=("Arial", 14))
    Nav_button4.pack(padx=5,pady=5)
    Nav_button5=tk.Button(home_frame, text = 'Popular Books', command = changepage4,font=("Arial", 14))
    Nav_button5.pack(padx=5,pady=5)
    Nav_button5=tk.Button(home_frame, text = 'Initialize Data Base', command = DBinnit,font=("Arial", 14)
    )
    Nav_button5.pack(padx=5,pady=5)
    home_frame.pack(fill=tk.BOTH,expand=TRUE)
#######################
## Welcome Page ENDS ##


## Search Page ##
#################
def page2(root):
    '''
    Second page is for search
    '''
    ## NESTED FUNC ##
    def check_user():
        '''
        This function only checks input and prints content of a query
        '''
        inp=user_entry.get()# getting the user input
        if inp == '':
            warning_lable=tk.Label(text='NO INPUT')
            warning_lable.pack()
            warning_lable.after(1500, warning_lable.forget)
        else: # Using tree View
            
            result=bookSearch.searchfunc(inp)
            
            tree.column("# 1", anchor=CENTER)
            tree.heading("# 1", text="ID")
            tree.column("# 2", anchor=CENTER)
            tree.heading("# 2", text="Genre")
            tree.column("# 3", anchor=CENTER)
            tree.heading("# 3", text="Title")
            tree.column("# 4", anchor=CENTER)
            tree.heading("# 4", text="Author")
            tree.column("# 5", anchor=CENTER)
            tree.heading("# 5", text="Purchase Price £")
            tree.column("# 6", anchor=CENTER)
            tree.heading("# 6", text="Purchase Date")
            i=1
            j=0
            for j in tree.get_children():
                tree.delete(j)
            for book in result: 
                tree.insert('', 'end', text=i, values=(book))
                i=i+1
            tree.pack()
    ##################
    Search_frame=tk.Frame(root,bg='#f4cd58')
    top_Frame=tk.Frame(Search_frame,bg='BLACK')
    Welcome_label=tk.Label(top_Frame, text="Search Books",font=("Arial", 50),foreground="WHITE",bg="BLACK")
    Welcome_label.pack()
    global time_label
    time_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    time_label.pack(anchor=SE)
    
    Weather_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    weatherupdate(Weather_label)
    Weather_label.pack(anchor=E)
    clock()
    top_Frame.pack(anchor=N, fill=BOTH)
    Search_lable2=tk.Label(Search_frame,bg='#f4cd58',text='Book Title or Genre or Author',font=("Arial", 14))
    Search_lable2.pack()
    user_entry = Entry(Search_frame) 
    user_entry.pack(padx=5,pady=5)
    check_button = Button(Search_frame, text="Search Book",command=check_user,font=("Arial", 14))
    check_button.pack(padx=5,pady=5)
    tree_Frame=tk.Frame(Search_frame,bg='#f4cd58',width=900,height=400)
    tree = ttk.Treeview(tree_Frame, column=("ID", "Genre", "Title", "Author", "Purchase Price £", "Purchase Date"), show='headings', height=15)
    tree_Frame.pack()
    Nav_button=tk.Button(Search_frame, text = 'Return to Home', command = changepage,font=("Arial", 14))
    Nav_button.pack(padx=5,pady=5)
    Search_frame.pack(fill=tk.BOTH,expand=TRUE)
######################
## Search Page ENDS ##    

## Checkout Page ##
###################
def page3(root):
    '''
    Page 3 is the Checkout tab
    Contains a table showing all the available books 
    One can checkout books and reserve them
    '''
    #################################################################################
    def viewTree():
        '''To show all the available Books'''
        result=bookSearch.searchABooks()
            
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Genre")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Title")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="Author")
        i=1
        j=0
        for j in tree.get_children():
            tree.delete(j)
        for book in result: 
            tree.insert('', 'end', text=i, values=(book))
            i=i+1
        tree.pack()
    def makeres():
            '''
            if book is reserved then this function is called.
            Used to make reservations 
            '''
            UID=UID_entry.get()
            BID=BID_entry.get()
            Date=today.strftime("%d/%m/%Y")
            reserve_button.forget()
            res_label.forget()
            result= bookCheckout.reserve(BID,UID,Date)
            result_label=tk.Label(lab_frame,text=result,bg='#f4cd58')
            result_label.pack(padx=5,pady=5)
            result_label.after(1500, result_label.forget)

    def chout():
        '''
        Gets the user ID and Book ID
        If book is there then it checks out and if reservation is available then it reserves
        '''
        UID=UID_entry.get()
        BID=BID_entry.get()
        Date=today.strftime("%d/%m/%Y")
        if UID == '' or BID == '':
            warning_lable=tk.Label(lab_frame,text='NO INPUT',bg='#f4cd58')
            warning_lable.pack()
            warning_lable.after(1500, warning_lable.forget)
        else:
            if not BID.isnumeric() or not UID.isnumeric():
                warning_lable=tk.Label(lab_frame,text='Invalid Book ID or User ID',bg='#f4cd58')
                warning_lable.pack()
                warning_lable.after(1500, warning_lable.forget)
            elif int(BID) > BookIDcount or len(UID)>4 or len(UID)<4:
                warning_lable=tk.Label(lab_frame,text='Invalid Book ID or User ID',bg='#f4cd58')
                warning_lable.pack()
                warning_lable.after(1500, warning_lable.forget)

            else:
                result=bookCheckout.checkout(BID,UID,Date)
                if result == 'Reservation Available':
                    res_label.forget()
                    res_label.pack()
                    reserve_button.forget()
                    reserve_button.pack()
                    reserve_button.pack(padx=5,pady=5)
                    
                else:
                    result_label=tk.Label(lab_frame,text=result,bg='#f4cd58')
                    result_label.pack()
                    result_label.after(1500, result_label.forget)


    #################################################################################
    BookIDcount=database.countOfBookIDs()
    Checkout_frame=tk.Frame(root,bg='#f4cd58')
    top_Frame=tk.Frame(Checkout_frame,bg='BLACK')
    Welcome_label=tk.Label(top_Frame, text="Checkout Books",font=("Arial", 50),foreground="WHITE",bg="BLACK")
    Welcome_label.pack()
    global time_label
    time_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    time_label.pack(anchor=SE)
    Weather_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    weatherupdate(Weather_label)
    Weather_label.pack(anchor=E)
    clock()
    top_Frame.pack(anchor=N, fill=BOTH)
    lab_frame=tk.Frame(Checkout_frame,bg='#f4cd58')
    res_label=tk.Label(lab_frame,text='Book Not Avalable but you can Reserve',bg='#f4cd58')
    reserve_button=tk.Button(lab_frame,text='Make Reservation',command=makeres,font=("Arial", 14))
    Checkout_lable2=tk.Label(Checkout_frame,bg='#f4cd58',text='Book ID')
    Checkout_lable2.pack()
    BID_entry = Entry(Checkout_frame) 
    BID_entry.pack()
    Checkout_lable3=tk.Label(Checkout_frame,bg='#f4cd58',text='Member ID')
    Checkout_lable3.pack()
    UID_entry = Entry(Checkout_frame) 
    UID_entry.pack()
    check_button=tk.Button(Checkout_frame, text = 'Checkout',command=lambda:[chout(),viewTree()],font=("Arial", 14))
    check_button.pack(padx=5,pady=5)
    placeholder_label=tk.Label(lab_frame,text='.',foreground='#f4cd58',bg='#f4cd58')
    placeholder_label.pack()
    placeholder_label.after(100,placeholder_label.forget)
    lab_frame.pack()
    tree_Frame=tk.Frame(Checkout_frame,bg='#f4cd58',width=900,height=300)
    Heading_lab=tk.Label(tree_Frame,text='List of Available Books',font=("Arial", 15),bg='#f4cd58')
    Heading_lab.pack()
    tree = ttk.Treeview(tree_Frame, column=("ID", "Genre", "Title", "Author"), show='headings', height=15)
    viewTree()
    tree_Frame.pack()
    back_Frame=tk.Frame(Checkout_frame,bg='#f4cd58')
    Nav_button=tk.Button(back_Frame, text = 'Return Home', command = changepage2,font=("Arial", 14))
    Nav_button.pack(padx=15,pady=15)
    back_Frame.pack(side=BOTTOM)
    Checkout_frame.pack(fill=tk.BOTH,expand=TRUE)
#######################    
## Checkout Page ENDS ##

## Return Page ##
#################
def page4(root):
    '''
    This page is responsibe for returning the books
    Contains a table showing all books that were checked out
    '''
    ############################################################################################
    def viewTree():
        '''Tree Function'''
        result=bookSearch.searchNABooks()
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Genre")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Title")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="Author")
        i=1
        j=0
        for j in tree.get_children():
            tree.delete(j)
        for book in result: 
            tree.insert('', 'end', text=i, values=(book))
            i=i+1
        tree.pack()


    def Book_ret():
        '''This is responsible for returning the books
        Checks the Book ID for invalid IDs'''
        #UID=UID_entry.get()
        BID=BID_entry.get()
        if BID == '':
            warning_lable=tk.Label(lab_frame,text='NO INPUT',bg='#f4cd58')
            warning_lable.pack()
            warning_lable.after(1500, warning_lable.forget)
        else:
            if not BID.isnumeric():
                warning_lable=tk.Label(lab_frame,text='Invalid Book ID ',bg='#f4cd58')
                warning_lable.pack()
                warning_lable.after(1500, warning_lable.forget)
            elif int(BID) > BookIDcount or int(BID) == 0:
                warning_lable=tk.Label(lab_frame,text='Invalid Book ID ',bg='#f4cd58')
                warning_lable.pack()
                warning_lable.after(1500, warning_lable.forget)
            else:
                Date=today.strftime("%d/%m/%Y")
                result=bookReturn.retbook(BID,Date)
                status_label=tk.Label(lab_frame,text=result,bg='#f4cd58')
                status_label.pack()
                status_label.after(1500, status_label.forget)  
    #############################################################################################
    BookIDcount=database.countOfBookIDs()
    Return_frame=tk.Frame(root,bg='#f4cd58')
    top_Frame=tk.Frame(Return_frame,bg='BLACK')
    Welcome_label=tk.Label(top_Frame, text="Return Books",font=("Arial", 50),foreground="WHITE",bg="BLACK")
    Welcome_label.pack()
    global time_label
    time_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    time_label.pack(anchor=SE)
    Weather_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    weatherupdate(Weather_label)
    Weather_label.pack(anchor=E)
    clock()
    top_Frame.pack(anchor=N, fill=BOTH)
    Return_lable2=tk.Label(Return_frame,bg='#f4cd58',text='Book ID')
    Return_lable2.pack()
    BID_entry = Entry(Return_frame) 
    BID_entry.pack()
    #Return_lable3=tk.Label(Return_frame,bg='#f4cd58',text='Member ID')
    #Return_lable3.pack()
    #UID_entry = Entry(Return_frame) 
    #UID_entry.pack()
    Ret_button=tk.Button(Return_frame, text = 'Return Book',command=lambda:[Book_ret(),viewTree()],font=("Arial", 14))
    Ret_button.pack(padx=5,pady=5)
    
    lab_frame=tk.Frame(Return_frame,bg='#f4cd58')
    placeholder_label=tk.Label(lab_frame,text='.',foreground='#f4cd58',bg='#f4cd58')
    placeholder_label.pack()
    placeholder_label.after(100,placeholder_label.forget)
    lab_frame.pack()
    tree_Frame=tk.Frame(Return_frame,bg='#f4cd58',width=900,height=400)
    Heading_lab=tk.Label(tree_Frame,text='List of Checkedout Books',font=("Arial", 15),bg='#f4cd58')
    Heading_lab.pack()
    
    tree = ttk.Treeview(tree_Frame, column=("ID", "Genre", "Title", "Author"), show='headings', height=15)
    viewTree()
    tree_Frame.pack()
    back_Frame=tk.Frame(Return_frame,bg='#f4cd58')
    Nav_button=tk.Button(back_Frame, text = 'Return Home', command = changepage3,font=("Arial", 14))
    Nav_button.pack(padx=30,pady=30)
    back_Frame.pack(side=BOTTOM)
    Return_frame.pack(fill=tk.BOTH,expand=TRUE)
#######################    
## Return Page ENDS ##

## Select Page ##
#################
def page5(root):
    '''
    This page has a nested page
    This is responsible for recomendations and buying new books
    '''
    ########################################################################################
    def selectbook():
        '''Just printing the graphs'''
        figure2=BookSelect.mostFamGenre()
        canvas = FigureCanvasTkAgg(figure2, Select_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    ########################################################################################
    Select_frame=tk.Frame(root,bg='#f4cd58')
    top_Frame=tk.Frame(Select_frame,bg='BLACK')
    Welcome_label=tk.Label(top_Frame, text="Recommendation",font=("Arial", 50),foreground="WHITE",bg="BLACK")
    Welcome_label.pack()
    global time_label
    time_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    time_label.pack(anchor=SE)
    
    Weather_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    weatherupdate(Weather_label)
    Weather_label.pack(anchor=E)
    clock()
    top_Frame.pack(anchor=N, fill=BOTH)
    Nav_button=tk.Button(Select_frame, text = 'Purchase Books', command = changepage5,font=("Arial", 14))
    Nav_button.pack(padx=5,pady=5)
    back_Frame=tk.Frame(Select_frame,bg='#f4cd58')
    Nav_button=tk.Button(back_Frame, text = 'Return Home', command = changepage4,font=("Arial", 14))
    Nav_button.pack(padx=30,pady=30)
    back_Frame.pack(side= BOTTOM)
    selectbook()
    Select_frame.pack(fill=tk.BOTH,expand=TRUE)
#######################    
## Select Page ENDS ##

## Purchase Page Starts ##
##########################
def page6(root):
    '''
    Sits inside Page 5
    Is responsible for Buying books accordion to popularity and genre
    '''
################################################################################################
    def Decision(event):
        '''Decide between Books or genre'''
        opt=clicked.get()
        if opt=='Books':
            drop2.forget()
            drop1.pack()
            book_spinbox.forget()
            purchase_button.forget()#
            purchase_button2.forget()
            drop4.forget()
            drop5.forget()
            drop3.forget()
            drop2.forget()
            bb_label2.forget()
            bb_label3.forget()
            bb_label1.forget()
            
        if opt=='Genre':
            drop1.forget()
            drop2.pack()
            book_spinbox.forget()
            purchase_button.forget()
            bb_label2.forget()
            bb_label3.forget()
            bb_label1.forget()
    
    def BuyBook(event):
        '''
        If user chooses books then show famous books
        Dont mind all the forget() functions
        They are just ther to make this look good
        '''
        opt=clicked1.get()
        book_spinbox.forget()
        purchase_button.forget()
        drop4.forget()
        drop5.forget()
        drop4.forget()
        drop3.forget()
        drop2.forget()
        bb_label3.forget()
        bb_label1.forget()
        bb_label2.forget()
        if opt == options1[0]:
            book_spinbox.forget()
            bb_label1.pack()
            bb_label2.forget()
            bb_label3.forget()
            book_spinbox.pack()
        elif opt == options1[1]:
            book_spinbox.forget()
            bb_label2.pack()
            bb_label1.forget()
            bb_label3.forget()
            book_spinbox.pack()
        elif opt == options1[2]:
            book_spinbox.forget()
            bb_label3.pack()
            bb_label1.forget()
            bb_label2.forget()
            book_spinbox.pack()
        
        purchase_button.pack(padx=5,pady=5)
    

    def genbuy(event):
        '''
        Same as above but with genre
        '''
        opt=clicked2.get()
        book_spinbox.forget()
        purchase_button.forget()
        bb_label2.forget()
        bb_label3.forget()
        bb_label1.forget()
        print(opt)
        if opt==options2[0]:
            drop3.pack(padx=5,pady=5)
            purchase_button2.forget()
            drop4.forget()
            drop5.forget()
        elif opt==options2[1]:
            drop4.pack(padx=5,pady=5)
            purchase_button2.forget()
            drop5.forget()
            drop3.forget()
        elif opt==options2[2]:
            drop5.pack(padx=5,pady=5)
            purchase_button2.forget()
            drop4.forget()
            drop3.forget()

    def BuyBook1(event):
        '''
        So each genre have more than one book 
        So to make a choice for that
        '''
        opt=clicked3.get()
        book_spinbox.forget()
        purchase_button.forget()
        if opt == options3[0]:
            purchase_button2.forget()
            bb_label2.forget()
            bb_label3.forget()
            bb_label1.pack()
            book_spinbox.pack()
        elif opt == options3[1]:
            purchase_button2.forget()
            bb_label1.forget()
            bb_label3.forget()
            bb_label2.pack()
            book_spinbox.pack()
        elif opt == options4[0]:
            purchase_button2.forget()
            bb_label1.forget()
            bb_label3.forget()
            bb_label2.pack()
            book_spinbox.pack()
        elif opt == options5[0]:
            purchase_button2.forget()
            bb_label1.forget()
            bb_label2.forget()
            bb_label3.pack()
            book_spinbox.pack()
        
        purchase_button2.pack(padx=5,pady=5)



            
    def completeTran2():
        '''
        To complete genre based transactions
        Buying books after according to genre
        '''
        Title=clicked3.get()
        if Title=='':
            Title=clicked4.get()
        elif Title=='':
            Title=clicked5.get()
        elif Title=='':
            Title=clicked3.get()
        amount=book_spinbox.get()
        Date=today.strftime("%d/%m/%Y")
        i=1
        for i in range (int(amount)):
            ID=database.countOfBookIDs()
            ID= str(ID+1)
            BookSelect.buyBook(ID,Title,Date)



    def completeTran():
        '''
        To complete genre based transactions
        Buying books according to popular books
        '''
        Title=clicked1.get()
        amount=book_spinbox.get()
        Date=today.strftime("%d/%m/%Y")
        i=1
        for i in range (int(amount)):
            ID=database.countOfBookIDs()
            ID= str(ID+1)
            BookSelect.buyBook(ID,Title,Date)


#####################################################################################
    purchase_frame=tk.Frame(root,bg='#f4cd58')
    top_Frame=tk.Frame(purchase_frame,bg='BLACK')
    Welcome_label=tk.Label(top_Frame, text="Purchase Books",font=("Arial", 50),foreground="WHITE",bg="BLACK")
    Welcome_label.pack()
    global time_label
    time_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    time_label.pack(anchor=SE)
    Weather_label=tk.Label(top_Frame,foreground='White',bg='BLACK',font=("Arial", 15))
    weatherupdate(Weather_label)
    Weather_label.pack(anchor=E)
    clock()
    top_Frame.pack(anchor=N, fill=BOTH)
    Purchase_lable2=tk.Label(purchase_frame,text='Select on basis of what you want to buy the books',bg='#f4cd58',font=("Arial", 14))
    Purchase_lable2.pack()
    clicked = StringVar()
    clicked1 = StringVar()
    clicked2 = StringVar()
    clicked3 = StringVar()
    clicked4 = StringVar()
    clicked5 = StringVar()
    options1=BookSelect.listoffambook()
    options2=BookSelect.listoffamgenre()
    options3=BookSelect.booksForGenre(options2[0])
    options4=BookSelect.booksForGenre(options2[1])
    options5=BookSelect.booksForGenre(options2[2])    # MIND ALL THE VARIABLES
    clicked1.set( options1[0] )                       # ALL THIS WAS DONE IS HEAT OF THE MOMENT
    clicked2.set( options2[0] )
    clicked3.set( options3[0] )
    clicked4.set( options4[0] ) 
    clicked5.set( options5[0] )
    drop1 = OptionMenu(purchase_frame , clicked1 , *options1,command=BuyBook)
    drop2 = OptionMenu(purchase_frame , clicked2 , *options2,command=genbuy)
    drop3 = OptionMenu(purchase_frame , clicked3 , *options3,command=BuyBook1)
    drop4 = OptionMenu(purchase_frame , clicked4 , *options4,command=BuyBook1)
    drop5 = OptionMenu(purchase_frame , clicked5 , *options5,command=BuyBook1)
    options=['Books','Genre']
    clicked.set( options[0] )
    main_drop = OptionMenu( purchase_frame , clicked , *options, command=Decision)
    main_drop.pack(padx=5,pady=5)

    bb_label1=tk.Label(purchase_frame,text='Recomended ammount is 5 Books',bg='#f4cd58')
    bb_label2=tk.Label(purchase_frame,text='Recomended ammount is 3 Books',bg='#f4cd58')
    bb_label3=tk.Label(purchase_frame,text='Recomended ammount is 2 Books',bg='#f4cd58')

    book_spinbox=tk.Spinbox(purchase_frame,from_=0, to=10)

    purchase_button=tk.Button(purchase_frame,text='Buy Books',command=completeTran,font=("Arial", 14))
    purchase_button2=tk.Button(purchase_frame,text='Buy Books',command=completeTran2,font=("Arial", 14))
    back_Frame=tk.Frame(purchase_frame,bg='#f4cd58')
    Nav_button=tk.Button(back_Frame, text = 'Go Back', command = changepage5,font=("Arial", 14))
    Nav_button.pack(padx=30,pady=30)
    back_Frame.pack(side= BOTTOM)
    purchase_frame.pack(fill=tk.BOTH,expand=TRUE)
########################
## Purchase Page Ends ##

## PAGE CONTROLLERS ##
######################
def changepage():#
    ''' Controls the page change between page 1 (Home) and 2 (Search)'''
    global pagenum, root
    for widget in root.winfo_children():
        widget.forget()
    if pagenum == 1:
        page2(root)
        pagenum = 2
    else:
        page1(root)
        pagenum = 1


def changepage2():
    ''' Controls the page change between page 1 (Home) and 3 (Checkout)'''
    global pagenumcheckout, root
    for widget in root.winfo_children():
        widget.forget()
    if pagenumcheckout == 1:
        page3(root)
        pagenumcheckout = 3
    else:
        page1(root)
        pagenumcheckout = 1

def changepage3():
    ''' Controls the page change between page 1 (Home) and 3 (Return)'''
    global pagenumreturn, root
    for widget in root.winfo_children():
        widget.forget()
    if pagenumreturn == 1:
        page4(root)
        pagenumreturn = 4
    else:
        page1(root)
        pagenumreturn = 1    

def changepage4():
    ''' Controls the page change between page 1 (Home) and 4 (Recomendation Tab)'''
    global pagenumselect, root
    for widget in root.winfo_children():
        widget.forget()
    if pagenumselect == 1:
        page5(root)
        pagenumselect = 5
    else:
        page1(root)
        pagenumselect = 1     

def changepage5():
    ''' Controls the page change between page 4 (Recomendation Tab) and 5 (Purchase)'''
    global pagenumpurchase, root
    for widget in root.winfo_children():
        widget.forget()
    if pagenumpurchase == 1:
        page6(root)
        pagenumpurchase = 6
    else:
        page5(root)
        pagenumpurchase = 1

'''Variables to control page selection'''
pagenum = 1
pagenumcheckout=1
pagenumreturn=1
pagenumselect=1
pagenumpurchase=1
root = tk.Tk()
root.title('Library Database Management System')
root.geometry('1200x700')
page1(root)   # MAIN PAGE WINDOW
root.mainloop()

## Page change help taken from ##
##https://stackoverflow.com/questions/58292617/how-to-have-multiple-pages-in-tkinter-gui-without-opening-new-windows-using-fu##
## Time program Help Taken from ##
##https://bytes.com/topic/python/answers/629499-dynamically-displaying-time-using-tkinter-label##