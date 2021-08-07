import os
import sys
import wget

iexec_out = os.environ['IEXEC_OUT']
iexec_in = os.environ['IEXEC_IN']

def read_file(filepath):
    with open(filepath, "r") as f:
        f.seek(0)
        return f.read()

def write_file(path, data):
    with open(path, "w+") as f:
        f.write(data)


def bubbleSort(arr, asc):
    n = len(arr)
 
    # Traverse through all array elements
    for i in range(n):
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if asc:
                if arr[j] > arr[j+1] :
                    arr[j], arr[j+1] = arr[j+1], arr[j]
            else:
                if arr[j] < arr[j+1] :
                    arr[j], arr[j+1] = arr[j+1], arr[j]

def main():
    print("------------------------")
    print("STARTING private code execution")

    # treat the args
    # /app/app.py https://inputfile_download_link.com <asc/desc> 
    args = sys.argv

    if len(args) <= 1:
        print("Error: Missing input arguments.\nUsage:")
        print("  iexec app run ... --args \"https://inputfile_download_link.com <asc/desc> \"")
        sys.exit(1)
    
    url = args[1]
    print(" - Using input file from URL: "+ url)

    direction_asc = True
    if len(args) > 2 and args[2] == "desc":
        direction_asc = False
        print(" - Descending sort")
    else:
        print(" - Ascending sort")


    # Download the input file
    print("DOWNLOADING input file")
    wget.download(url, iexec_in + '/inputs.csv')


    # Check the input file is here
    print("CHECKING Input file")
    if os.path.exists(iexec_in + '/inputs.csv'):
        data = read_file(iexec_in + '/inputs.csv').split(",")
        print("Input file content:   ", read_file(iexec_in + '/inputs.csv'))
    else:
        print("Cannot find input file, check that the dowload URL is correct")
        sys.exit(1)
    

    # Work on data
    # print(data, "data------")
    print("SORTING")
    sort = [float(i) for i in data]
 
    bubbleSort(sort, direction_asc)
    
    #write result
    print("WRITING result")
    result = str(sort)
    write_file(iexec_out + '/my-result.txt', result)

    print("END of the private code execution")
