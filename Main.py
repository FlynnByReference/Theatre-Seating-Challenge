import fileinput

# Define rows
SEATROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# Three seat buffer
BUFFER = 'SSS'
# Create 2D array of seats to represent 
rows, cols = (10, 20)
theater = []
for i in range(rows):
    col = ""
    for j in range(cols):
        col += 'S'
    theater.append(col)

# Determine whether a row is empty
def isEmpty(row):
    if ('T' in row):
        return False
    else:
        return True

# Checks the end of a row for available seating and a 3 seat buffer
def isAvailable(row, seats):
    # Creates a string to represent available seating at the end of a row
    occupy = BUFFER
    for i in range(seats):
        occupy += 'S'
    # If the given row has enough open seats to accomodate the party return true
    if (occupy in row):
        return True
    return False

# Determines which side of the aisle has the most available seats
def mostRoom(row):
    left = row.find('T')
    right = row.rfind('T')

    if (left > len(row) - right):
        return 'left'
    else:
        return 'right'
    
# Find a row to seat a party
def findRow(seats):
    # Rough ranking of ideal theater rows
    ideal = [6, 7, 5, 8, 4, 9, 3, 2, 1, 0]
    # List of occupied but still available rows
    available = []
    # Variable to determine whether any rows are available
    closed = []
    # Check if the first 7 rows in ideal ranking are empty
    # Most movie watchers don't like sitting up front
    for i in ideal[:7]:
        if isEmpty(theater[i]):
            return i
        elif isAvailable(theater[i], seats):
            available.append(i)
        else:
            closed.append(i)
    # Return one of the more desirable aisles if available
    if len(available) > 0:
        return available[0]

    # Now check least desirable front 3 rows
    for i in ideal[6:]:
        if isEmpty(theater[i]):
            return i
        elif isAvailable(theater[i], seats):
            available.append(i)
        else:
            closed.append(i)

    # Return None if no seating is available
    if closed == ideal:
        return None

    # Return the first available row if every row is occupied with at least one party
    return available[0]

def seat(seats):
    seatRow = findRow(seats)
    occupy = ''
    reserved = [seatRow]
    for i in range(seats):
        occupy += 'T'
    # theater is full :(
    if seatRow == None:
        print('theater is full :(')
        return reserved
    chosen = theater[seatRow]

    # Seats first party of the row in the middle
    if 'T' not in chosen:
        chosen = chosen.replace('S', '', len(occupy))
        midPoint = len(chosen)//2
        theater[seatRow] = chosen[:midPoint] + occupy + chosen[midPoint:]
        for i in range(len(theater[seatRow])):
            if theater[seatRow][i] == 'T':
                reserved.append(i + 1)
        return reserved

    # Seats the party on the left side of the aisle if it has the most available seats
    elif mostRoom(chosen) == 'left':
        taken = chosen.find('T')
        buffer = chosen[:taken]
        buffer = buffer[:len(buffer) - len(occupy + BUFFER)] + occupy + BUFFER
        theater[seatRow] = buffer + chosen[taken:]
        for i in range(len(occupy)):
            reserved.append(taken + i)
        return reserved

    # Seats the party on the right side of the aisle if it has the most available seats
    elif mostRoom(chosen) == 'right':
        taken = chosen.rfind('T')
        buffer = chosen[taken + 1:]
        buffer = BUFFER + occupy + buffer[len(BUFFER) + len(occupy):]
        theater[seatRow] = chosen[:taken + 1] + buffer
        for i in range(len(occupy)):
            reserved.append(taken - (i + 1))
        return reserved

def main():
    # Create an output file if one does not already exist or overwrite the existing output file
    outfile = open('output.txt', 'w')

    # Reads each line of the input file and assigns theater seats to the reservation party based on the preference algorithm
    for line in fileinput.input(files='input.txt'):
        reserve = int(line[5:])
        reservation = seat(reserve)
        row = reservation[0]
        output = line[:5]
        # If no seat numbers have been returned, there are no available seats for a party of the given size
        if len(reservation) == 1:
            output += 'No available seating'
            break
        # Write the seat numbers to the output file
        for i in range(len(reservation) - 1):
            if i == len(reservation) - 2:
                output += SEATROWS[row] + str(reservation[i+1]) + '\n'
            else:
                output += SEATROWS[row] + str(reservation[i+1]) + ','
        outfile.write(output)
    outfile.close()

main()
        