import psutil
import time
import os
import datetime

def get_network_usage(interface='eth0', duration=1):
    net_io_start = psutil.net_io_counters(pernic=True)[interface]
    start_bytes = net_io_start.bytes_recv
    
    time.sleep(duration)  # Wait for the specified duration
    
    net_io_end = psutil.net_io_counters(pernic=True)[interface]
    end_bytes = net_io_end.bytes_recv
    
    download_speed = (end_bytes - start_bytes) / duration  # Bytes per second
    download_speed_mbps = download_speed / 1_000_000  # Convert to Megabytes
    
    return download_speed_mbps

def shutdown():
    os.system("shutdown /s /t 0")

def log():
    now = datetime.datetime.now()
    with open('log.txt', 'a') as f:
        f.write(f"SHUTDOWN AT: {now.strftime('%H:%M:%S %d/%m/%Y')}\n")

if __name__ == "__main__": 
    print("MONITORING TRAFFIC...")
    
    SHUTDOWN_TIMER = 60 # seconds
    WRITE_TO_LOG = True
    STEP = 1 # seconds
    
    shutdown_initiated = False
    shutdown_in = SHUTDOWN_TIMER
    interface = "Ethernet"  # Replace with your network interface name

    while True:
        time.sleep(STEP)
        speed = get_network_usage(interface=interface, duration=1)
        
        if speed < 1:
            shutdown_initiated = True
            shutdown_in -= STEP+1

            if shutdown_in/(STEP+1) <= 10:
                print("Shutdown in:", shutdown_in, 'seconds\007')
            else:
                print("Shutdown in:", shutdown_in, 'seconds')

            if shutdown_in <= 0:
                if WRITE_TO_LOG:
                    log()
                shutdown()
        else:
            if shutdown_initiated:
                shutdown_initiated = False
                print("Shutdown postponed!")
            shutdown_in = SHUTDOWN_TIMER



