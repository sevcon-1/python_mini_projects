import sys
import logging

logging.basicConfig(level=sys.argv[1])

logging.debug('DEBUG')
logging.info('INFO')

def write_output(output):
    with open('3xplus1.csv', 'w') as file:
        for line in output:
            logging.debug("line value is: ")
            logging.debug(line)
            ''' Write every item in the list out delimited by , '''
            file.write(','.join(str(item) for item in line))
            file.write("\n")
            
def bounce_it(n):
    bounce = True
    result = []

    '''
    n/2 if 0 = mod(n,2)
    3n+1 if 1 = mod(n,2)
    '''

    while bounce:
        logging.debug(f"value of n is: {n}")
        result.append(int(n))
        logging.debug(result)
        #print(f"{result},", end="")
        m = n % 2
        if m:
            n = 3*n+1
        else:
            n = n/2 

        if n == 1:
            result.append(1)
            bounce = False

    return result

if __name__ == '__main__':
    output = []
    #print(sys.argv)
    n = int(input("Enter staring number: "))
    if sys.argv[2] == 'all':
        while n:
            output.append(bounce_it(n))
            n = n-1
    else:
        output.append(bounce_it(n))

    logging.debug("Returned list for writing is: ")
    logging.debug(output)

    write_output(output)

