import os
import time


def login():
    while True:
        username=raw_input("enter the username:")
        password=raw_input("enter the password:")
        if(username=="swag"and password=="swag123"):
            time.sleep(1)
            print "login successful"
            logged()
            break
        else:
            print"password did not match"

def logged():
    time.sleep(1)
    print("Welcome to the GAMING STATION")

def login1():
    while True:
        username=raw_input("Enter Username:")
        password=raw_input("Enter Password:")
        if(username=="lmois"and password=="123"):
            time.sleep(1)
            #print "login successful"
            #logged()
            break
        else:
            print"password did not match"

def logged():
    time.sleep(1)
    print("welcome to the ----")

class gaming:
    

    def __init__(self):
        self.gno = 0
        self.gname   = ""
        self.gdet    = ""
        self.app     = ""
        self.dt = time.strftime('%Y-%m-%d')
        
    def create(self):
        
        self.gno =   int(input('Enter game number   : '))
        self.gname = raw_input('Enter game name  : ')
        self.gdet =  raw_input('Enter game details   : ')
        self.app =   raw_input("enter the application name:")
        wFile = open('GAME.CSV','a')
        
        wFile.write(str(self.gno)+','+self.gname+','+self.gdet+','+self.app+','+self.dt+'\n')
        wFile.close()
        print('Record added to the file successfully.')

    def search(self):
        
        found = False
        try:
            rFile = open('GAME.CSV')   

            mgno = int(input('What game number you want to search ? '))
            for record in rFile:
                L = record.split(',')
                if (mgno == int(L[0])):
                    found = True
                    name = L[1]
                    det  = L[2]
                    app  = L[3]
                    print(" Game No: {} \n Game Name: {} \n Details:{} \n App: {}").format(mgno,name,det,app)

            rFile.close()

            if (found):
                #print('Game#: ',mgno,' found')
                pass
            else:
                print "Game#: {} not found".format(mgno)
        except IOError:
            print("File 'GAME.CSV' not found")

    def update(self):
        
        if not os.path.exists('GAME.CSV'):
            print("File 'GAME.CSV' not found")
            return
        
        rFile = open('GAME.CSV', 'r')
        L = rFile.readlines()
        rFile.close()
     
        mgno = raw_input('What game number you want to modify ? ')
        found = False

        for index,record in enumerate(L):
            elements = record.rstrip('\n').split(',')
            if elements[0]==mgno:
                found = True
                locn = index
                break
        if not found:
            print "game#",mgno,"not found"
        else:
            curr_rec_L = L[locn].split(',')
            
            newname = raw_input("Enter new name : ")
           
            curr_rec_L[1] = newname

            newgdet = raw_input("Enter new details : ")
            
            curr_rec_L[2] = str(newgdet)

            newapp = raw_input("Enter new application : ")
            
            curr_rec_L[3] = str(newapp)

            curr_rec_L[4] = self.dt

            newlist = curr_rec_L[0]+','+curr_rec_L[1]+','+curr_rec_L[2]+','+curr_rec_L[3]+','+curr_rec_L[4]+'\n'

            L[locn] = newlist

            wFile = open('GAME.CSV','w')
            wFile.writelines(L)
            wFile.close()



    def delete(self):
        
        if not os.path.exists('GAME.CSV'):
            print("File 'GAME.CSV' not found")
            return
        
        rFile = open('GAME.CSV', 'r')
        L = rFile.readlines()
        rFile.close()
     
        mgno = raw_input('What game number you want to delete ? ')
        found = False

        for index,record in enumerate(L):
            elements = record.rstrip('\n').split(',')
            if elements[0]==mgno:
                found = True
                locn = index
                break
        if not found:
            print "mgno#",mgno,"not found"
        else:
           
            del L[locn]
            print "Record with roll#:",mgno,"deleted successfully"

           
            wFile = open('GAME.CSV','w')
            wFile.writelines(L)
            wFile.close()

    def report(self):
        

        if not os.path.exists('GAME.CSV'):
            print("File 'GAME.CSV' not found")
            return
        else:
            rFile = open('GAME.CSV','r')

        for record in rFile:
            L = record.split(',')
            gno = int(L[0])
            gname = L[1]
            gdet = L[2]
            app= L[3]
            print "GAME NO:",gno
            print "GAME NAME:",gname
            print "GAME DETAILS:",gdet
            print "APPLICATION:",app
                
class subscriber:
    def __init__(self):
        self.subno=0
        self.subname=""
        self.emailid=""
        self.status= True
        self.news= True

    def create(self):
        
        self.subno = int(input('Enter subscriber number   : '))
        self.subname = raw_input('Enter subsciber name  : ')
        self.emailid = raw_input('Enter subscriber email id   : ')
        self.status =raw_input("Enter the Subscriber status NA-not active/A-active):")
        self.news =raw_input("Enter the Newsletter status(S-sent/R-returned):")
        wFile = open('SUBS.CSV','a')
        
        wFile.write(str(self.subno)+','+self.subname+','+self.emailid+','+self.status+','+self.news+'\n')
        wFile.close()
        print('Record added to the file successfully')


    def search(self):
        
        found = False
        try:
            rFile = open('SUBS.CSV')   
            msubno = int(input('What subscriber number you want to search ? '))
            for record in rFile:
                L = record.split(',')
                if msubno == int(L[0]):
                    found = True
                    name = L[1]
                    emailid = L[2]
                    status  = L[3]
                    news= L[4]
                    print(msubno,name,emailid,status,news)
            rFile.close()
            if not found:
                print('subscriber#: ',msubno,' not found')
        except IOError:
            print("File 'SUBS.CSV' not found")

    def update(self):
        if not os.path.exists('SUBS.CSV'):
            print("File 'SUBS.CSV' not found")
            return
        
        rFile = open('SUBS.CSV', 'r')
        L = rFile.readlines()
        rFile.close()
     
        msubno = raw_input('What subscriber number you want to modify ? ')
        found = False

        for index,record in enumerate(L):
            elements = record.rstrip('\n').split(',')
            if elements[0]==msubno:
                found = True
                locn = index
                break
        if not found:
            print "subscriber#",msubno,"not found"
        else:
            curr_rec_L = L[locn].split(',')
            
            newname = raw_input("Enter new name : ")
           
            curr_rec_L[1] = newname

            newemail = raw_input("Enter new emailid : ")
            
            curr_rec_L[2] = newemail

            newstatus = raw_input("Enter new status(NA/A): ")
            curr_rec_L[3] = newstatus

            newnews = raw_input("Enter new newsletter status(S/R): ")
            
            curr_rec_L[4] = newnews
            

            newlist = curr_rec_L[0]+','+curr_rec_L[1]+','+curr_rec_L[2]+','+curr_rec_L[3]+','+curr_rec_L[4]+'\n'
            L[locn] = newlist

            wFile = open('SUBS.CSV','w')
            wFile.writelines(L)
            wFile.close()



    def report(self):
        

        if not os.path.exists('SUBS.CSV'):
            print("File 'SUBS.CSV' not found")
            return
        else:
            rFile = open('SUBS.CSV','r')

        for record in rFile:
            L = record.split(',')
            subno = int(L[0])
            subname = L[1]
            emailid = L[2]
            status= L[3]
            news=L[4]
            print "SUBSCRIBER NO:",subno
            print "SUBSCRIBER NAME NAME:",subname
            print "SUBSCRIBER EMAIL ID:",emailid
            print "SUBSCRIBER STATUS:",status
            print "SUBSCRIBER NEWSLETTER STATUS:",news
                
login1()
s = gaming()
p = subscriber()
print "---------------------------------------------------------------------"
print "                              Welcome Administrator                                "
print "---------------------------------------------------------------------"
print "As an administrator which module do you wish to work on?"
print "Gaming or Subscriber"
mod=raw_input("Enter either Gaming or Subscriber:")

if mod.upper() =="GAMING":

    while True:
         print('\n\tGAMING STATION \n')
         print(' 1. CREATE')
         print(' 2. SEARCH')
         print(' 3. UPDATE')
         print(' 4. DELETE')
         print(' 5. REPORT')
         print(' 6. EXIT')

         choice = int(input('Enter your choice (1-6) : '))
         if choice == 1:
             s.create()
         elif choice == 2:
             s.search()
         elif choice == 3:
             s.update()
         elif choice == 4:
             s.delete()
         elif choice == 5:
             s.report()
         elif choice == 6:
             break;
         else:
             print('Error in choice.. Retry!')

elif mod.upper() =="SUBSCRIBER":
    while True:
        print('\n\n\tSUBSCRIBER\n')
        print('1. CREATE')
        print('2. SEARCH')
        print('3. UPDATE')
        print('4. DELETE')
        print('5. REPORT')
        print('6. EXIT')
        choice = int(input('Enter your choice (1-6) : '))
        if choice == 1:
            p.create()
        elif choice == 2:
            p.search()
        elif choice == 3:
            p.update()
        elif choice == 4:
            p.delete()
        elif choice == 5:
            p.report()
        elif choice == 6:
            break;
        else:
            print('Error in choice. Please retry')

else:
    print('Error in choice. Please retry')

        










       

