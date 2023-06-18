import csv
import time
import random

def write_to_csv(data, filename):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Example usage
while True:
    # Generate or retrieve the data to be written to the CSV file
    data = [random.random(), random.random(), random.random(), random.random(), random.random()]

    # Specify the filename of the CSV file
    filename = 'data.csv'

    # Write data to CSV
    write_to_csv(data, filename)

    # Wait for a specific interval before writing again
    time.sleep(1)
