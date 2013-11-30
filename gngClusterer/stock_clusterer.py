import glob
import gng
import stock_functions

if __name__ == '__main__':
    files = glob.glob("../data/*.csv")
    print files
    print open(files[0]).read()
    
#    graph = gng.gng()



