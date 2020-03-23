import os

f=open('log_date.txt','r')
b=f.readline()
while b:
        b=400
        cmd='grep %d abc.txt'%b    #my2 is the file in which we are looking for b
            os.system(cmd)
                b=f.readline()
                f.close()

                #a='500'
                #cmd='grep %d my2.txt'%a
                #os.system(cmd)
