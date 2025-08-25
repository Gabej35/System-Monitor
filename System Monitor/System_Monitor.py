import psutil
import time
from datetime import datetime
import csv

# global Var
cpu = None
memory = None
disk = None
cpu_avg = None
memory_avg = None
disk_avg = None

# list
cpu_list = []
memory_list = []
disk_list = []
time_list = []

# Main monitor function that will be called to check usage
def monitor(duration, intervals):
    global cpu, memory, disk
    while intervals != 0:
        # This is getting the values
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # Get current time
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        time_list.append(formatted_time)

        print(f"[{formatted_time}] CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")

        # Append to lists and update averages
        average(cpu, memory, disk)

        time.sleep(duration)  # Time in seconds
        intervals -= 1  # decrement the counter

# Get duration and intervals
while True:
    try:
        duration_input = float(input("How many seconds apart for each check?: "))
        intervals_input = int(input("How many times do you want this check?: "))
        if duration_input > 0 and intervals_input > 0:
            break  # Both inputs are valid, exit loop
        else:
            print("Both inputs must be greater than 0. Try again.")
    except ValueError:
        print("Invalid format, only numbers are allowed. Please try again.")

# Getting and appending a list of the average usage
def average(cpu, memory, disk):
    global cpu_avg, memory_avg, disk_avg

    cpu_list.append(cpu)
    memory_list.append(memory)
    disk_list.append(disk)

    cpu_avg = sum(cpu_list) / len(cpu_list)
    memory_avg = sum(memory_list) / len(memory_list)
    disk_avg = sum(disk_list) / len(disk_list)

# Run the monitor
monitor(duration_input, intervals_input)

# Display final averages
print("\nAverage Usage:")
print(f"CPU: {cpu_avg:.2f}% | Memory: {memory_avg:.2f}% | Disk: {disk_avg:.2f}%")

# Display max usage and corresponding time
max_cpu = max(cpu_list)
max_memory = max(memory_list)
max_disk = max(disk_list)

time_max_cpu = time_list[cpu_list.index(max_cpu)]
time_max_memory = time_list[memory_list.index(max_memory)]
time_max_disk = time_list[disk_list.index(max_disk)]

print("\nMaximum Usage:")
print(f"Max CPU: {max_cpu:.2f}% at {time_max_cpu}")
print(f"Max Memory: {max_memory:.2f}% at {time_max_memory}")
print(f"Max Disk: {max_disk:.2f}% at {time_max_disk}")

# Export to CSV
with open("monitor_log.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "CPU (%)", "Memory (%)", "Disk (%)"])
    for t, c, m, d in zip(time_list, cpu_list, memory_list, disk_list):
        writer.writerow([t, c, m, d])

print("\nAll readings have been saved to 'monitor_log.csv'.")
