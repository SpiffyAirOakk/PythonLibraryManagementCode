import database


def searchfunc(search):
    '''Just search books'''
    out=database.searchfunc(search)
    return out



def searchNABooks():
    ''' USED TO RETURN NA BOOKS '''
    out=database.NAsearchfunc()
    return out

def searchABooks():
    ''' USED TO RETURN Available BOOKS '''
    out=database.Asearchfunc()
    return out


def test_searchfunc():
    assert searchfunc('H') != ''

def test_searchNABooks():
    assert searchNABooks() != ''

def test_searchABooks():
    assert searchABooks() != ''


if __name__ == "__main__":
    test_searchfunc()
    test_searchNABooks()
    test_searchABooks()
    print("Everything passed")