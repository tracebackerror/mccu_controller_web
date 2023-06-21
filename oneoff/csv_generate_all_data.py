import csv
import datetime
import random
import time


# Define the column headers
headers = [
    "Date", "Time", "Latitude", "Longitude", "Roll", "Pitch", "Yaw", "Temperature", "Current",
    "Azimuth", "Elevation", "Cross-EL", "Polarization",
    "Target Azimuth", "Target Elevation", "Target Polarization",
    "Satellite", "Channel",
    "Motor Azimuth", "Motor Elevation", "Motor Cross EL", "Motor Polarization"
]

# Define the CSV file path
csv_file_path = "data.csv"
while True:
# Generate and write infinite loop CSV data
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        #writer.writerow(headers)  # Write the column headers


        # Generate a random datetime
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")

        # Generate random values for other columns
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        roll = round(random.uniform(-180, 180), 2)
        pitch = round(random.uniform(-90, 90), 2)
        yaw = round(random.uniform(0, 360), 2)
        temperature = round(random.uniform(-40, 40), 2)
        current = round(random.uniform(0, 10), 2)
        azimuth = round(random.uniform(0, 360), 2)
        elevation = round(random.uniform(0, 90), 2)
        cross_el = round(random.uniform(-90, 90), 2)
        polarization = random.choice(["H", "V"])
        satellite = "Satellite Name"
        channel = "Channel Name"
        motor_azimuth = round(random.uniform(0, 360), 2)
        motor_elevation = round(random.uniform(0, 90), 2)
        motor_cross_el = round(random.uniform(-90, 90), 2)
        motor_polarization = random.choice(["H", "V"])

        # Write the row to the CSV file
        row = [
            current_datetime, latitude, longitude, roll, pitch, yaw, temperature, current,
            azimuth, elevation, cross_el, polarization,
            azimuth, elevation, polarization,
            satellite, channel,
            motor_azimuth, motor_elevation, motor_cross_el, motor_polarization
        ]
        writer.writerow(row)

    time.sleep(3)
