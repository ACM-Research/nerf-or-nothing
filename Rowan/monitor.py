import psutil
import time

# Update the process_id variable with the PID of the process to monitor
process_id = 2958687

while True:
    try:
        # Get process information using psutil by specifying the process ID
        process = psutil.Process(process_id)
        memory_info = process.memory_info()

        # Extract the memory usage and storage usage
        rss = memory_info.rss
        vms = memory_info.vms
        storage_usage = psutil.disk_usage('/').used

        # Extract GPU usage (if applicable)
        # Note: This depends on the GPU and the library you are using
        # Please adjust accordingly based on your specific setup
        gpu_usage = "N/A"

        # Output the information
        print(f"Process ID: {process_id}")
        print(f"Memory Usage (RSS): {rss} bytes")
        print(f"Memory Usage (VMS): {vms} bytes")
        print(f"Storage Usage: {storage_usage} bytes")
        print(f"GPU Usage: {gpu_usage}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.TimeoutExpired):
        # Handle exceptions that may occur when accessing process information
        print(f"Failed to retrieve process information for PID: {process_id}")

    # Sleep for 1 second
    time.sleep(1)
