import database

def checkout(ID, user_ID,date):
    ###  This function will tell either the book can be checked out or not and If it can be then it allows the book to be checked out ###
    ### Calls the database using 5 different fuctions ###
    out=database.checkout(ID)
    out2=database.checkres(ID)
    out3=database.didyoureserve(ID,user_ID)
    
    
   
    if out:
            
        if out3:
            status='You are on reservation List'
        else:
            if out2:
                status='No reservation Available'
            else:
                status='Reservation Available'
                #database.reservbook(ID,user_ID,date)  ## Check and make a button if reservation is available
                        
        
        
        
    elif out3:
        print('test stop')
        #print('Available')
        #choice=input('Are you sure? Y|N ')
        #if choice=='Y':
        database.changerestocheckout(ID,user_ID,date)
        status='Book Checkedout'

    elif out2:
        status='Sorry Book available but Reserved'
        
    else:
        #print('Available')
        #choice=input('Are you sure? Y|N ')
        #if choice=='Y':
        database.confirmres(ID,user_ID,date)
        status='Book Checkedout'
    return status
    


def reserve(ID, user_ID,date):
    '''Make Reservations '''
    out4=database.didyoujustcheckedout(ID,user_ID)
    if out4:
        status='Mate you just checked out'
    else:
        database.reservbook(ID,user_ID,date)
        status='Reservation Made'
    return status


def test_checkout():
    assert checkout('5', '2211','13/11/2022') != ''

def test_reserve():
    assert reserve('5', '2212','13/11/2022') != ''

if __name__ == "__main__":
    test_checkout()
    test_reserve()
    print("Everything passed")
