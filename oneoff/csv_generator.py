import csv
import time

def write_to_csv(data, filename):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Example usage
while True:
    # Generate or retrieve the data to be written to the CSV file
    data = [1, 2, 3, 4, 5]

    # Specify the filename of the CSV file
    filename = 'data.csv'

    # Write data to CSV
    write_to_csv(data, filename)

    # Wait for a specific interval before writing again
    time.sleep(1)
