import database

def retbook(ID,date):
    '''Just Returns the book and updates DB'''
    check1=database.checkout(ID)
    if check1:
        database.returnbook(ID,date)
        status='Book Returned Successfully'
    else:
        status='No Book Checked Out under this ID'
    return status

def test_retbook():
    assert retbook('5', '2211') != ''

if __name__ == "__main__":
    test_retbook()
    print("Everything passed")