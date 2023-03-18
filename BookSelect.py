import database
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

def mostFamGenre():
    '''
    This Function returns the Graphs
    Gets all the numbers from DB
    '''
    Genre=database.mostFamGenre()
    top1=Genre[0][1]
    top1Val=Genre[0][0]

    top2=Genre[1][1]
    top2Val=Genre[1][0]

    top3=Genre[2][1]
    top3Val=Genre[2][0]

    values = [top1Val,top2Val,top3Val]
    names = [top1,top2,top3]

    figure=Figure(figsize=(20, 20))
    axes = figure.add_subplot(122)
    axes.bar(names, values)
   


    Book=database.mostFamBook()
    top1=Book[0][1]
    top1Val=Book[0][0]

    top2=Book[1][1]
    top2Val=Book[1][0]

    top3=Book[2][1]
    top3Val=Book[2][0]

    values = [top1Val,top2Val,top3Val]
    names = [top1,top2,top3]

    axes = figure.add_subplot(121)
    axes.bar(names, values)
    return figure

    

def listoffambook():
    '''Lists top 3 famous books. Uses DB'''
    Book=database.mostFamBook()
    top1=Book[0][1]
    top1Val=Book[0][0]

    top2=Book[1][1]
    top2Val=Book[1][0]

    top3=Book[2][1]
    top3Val=Book[2][0]
    options=[top1,top2,top3]
    return options


def listoffamgenre():
    '''Lists top 3 famous Genre. Uses DB'''
    genre=database.mostFamGenre()
    top1=genre[0][1]
    top1Val=genre[0][0]

    top2=genre[1][1]
    top2Val=genre[1][0]

    top3=genre[2][1]
    top3Val=genre[2][0]
    options=[top1,top2,top3]
    return options

def buyBook(ID,Title,Date):
    database.buyBook(ID,Title,Date)
    status='Precurement Successful'
    return status


def booksForGenre(Genre):
    '''Lists top 3 famous books by genres. Uses DB'''
    ans=database.bookbyGenre(Genre)
    book1=0
    book2=0
    options=[]
    if len(ans)==1:
        book1=ans[0][0]
        options=[book1]
    elif len(ans)==2:
        book1=ans[0][0]
        book2=ans[1][0]
        options=[book1,book2]
    return options

    

def test_booksForGenre():
    assert booksForGenre('Comedy') != ''

def test_listoffamgenre():
    assert listoffamgenre() != ''

def test_listoffambook():
    assert listoffambook() != ''

def test_mostFamGenre():
    assert mostFamGenre()!=''


if __name__ == "__main__":
    test_booksForGenre()
    test_listoffamgenre()
    test_listoffambook()
    test_mostFamGenre()
    print("Everything passed")