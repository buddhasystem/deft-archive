### Generic utility functions:
def out_name(n1,n2):
    return 'o_'+n1+'_'+n2
###
def inp_name(n1,n2):
    return 'i_'+n1+'_'+n2

###
def uni_name(n1,n2): # just a shortcut to both functions above, to simplify code
    return ('i_'+n1+'_'+n2, 'o_'+n1+'_'+n2)


### A mock-up function for cases when we want to have serial numbers generated,
### without using the real database sequence:
def getSerial():
    f = open('serial.txt',"r")
    n = int(f.read()) + 1
    f.close()

    f = open('serial.txt',"w")
    f.write(str(n))
    f.close()
    return n
