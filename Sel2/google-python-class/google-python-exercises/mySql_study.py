import sqlite3

createDb = sqlite3.connect(':memory:')
queryCurs = createDb.cursor()

def createTable():
    queryCurs.execute('''CREATE TABLE customers
    (id INTEGER PRIMARY KEY, name TEXT, street TEXT, city TEXT, state TEXT, balance REAL)''')

def addCust(name,street, city, state, balance):
    queryCurs.execute('''INSERT INTO customers (name,street,city,state,balance)
    VALUES(?,?,?,?,?)''',(name,street,city,state,balance))
    
    
    
    
    
def main():
    createTable()
    
    addCust('Maciek','mydlana street','wrocla','DOL',160)
    addCust('BARTEK','ulica_1','swidnica','GOR',190)
    
    createDb.commit()
    queryCurs.execute('SELECT * FROM customers ORDER BY balance')
    
    listTitle = ['Id Num', 'Name', 'Street', 'City', 'State', 'Balance']
    k = 0 
    
    
    for i in queryCurs:
        print "\n"
        for j in i:
            print listTitle[k],
            print j
            if k <5: k+=1
            else: k = 0
            
    queryCurs.close()

if __name__ == '__main__':
    main()