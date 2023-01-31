def main():
    import speedtest
    import time
    from datetime import datetime
    import os
    

    if not os.path.exists("Tasks/Speedtester/Output"):
        os.mkdir("Tasks/Speedtester/Output")
        
    start_time = time.time()

    currentDate = datetime.now()
    date_time = currentDate.strftime("Speedtest_%d_%m_%Y_%H_%M_%S")

    test = speedtest.Speedtest(secure=True)
    best = test.get_best_server()

    results = f"Speedtest Results using the server '{best['host']}':\n"

    download = test.download()
    upload = test.upload()
    ping = test.results.ping

    results += f"Download Speed: {download/1024/1024:.2f} Mbps\n"
    results += f"Upload Speed: {upload/1024/1024:.2f} Mbps\n"
    results += f"Ping: {int(ping)} ms\n"

    results += f"\n\nTime taken: {time.time() - start_time:.2f} seconds"


    with open(f"Tasks/Speedtester/Output/{date_time}.log", "w+") as f:
        f.write(results)
    
    return "Speedtest task completed successfully"

def initialize():
    return "Speedtester initialized"

if __name__ == "__main__":
    main()