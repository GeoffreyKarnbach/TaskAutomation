import subprocess
import os
import configparser
import threading
import time
import sys

import Global.logger as logger
import Global.task as Task
import Global.utils as Utils

logs = logger.Logger()

start_time = time.time()

# Make sure termination flag is set to false
with open("Termination/termination", "w") as f:
    f.write("False")

logs.log("Set termination flag to False", logtype = "TERMINATION")

# Array containing all tasks
tasks = []

# Fetch all the individual requirements and put them in a requirements.txt file
task_list = os.listdir("Tasks")
with open("requirements_.txt", "w") as f:
    for task in task_list:
        f.write(open(f"Tasks/{task}/requirements.txt", "r").read()+"\n")
logs.log("Generated requirements_.txt", logtype = "REQUIREMENTS")
logs.freeline()

# First download all the requirements
logs.log("Installing requirements with pip:", logtype = "REQUIREMENTS")
result = subprocess.run(["pip", "install", "-r", "requirements_.txt"], capture_output=True)
logs.log(result.stdout.decode("utf-8"), logtype = "REQUIREMENTS")
logs.log("All requirements have been installed with pip.", logtype = "REQUIREMENTS")
logs.freeline()

# Delete the requirements.txt file
os.remove("requirements_.txt")
logs.log("Deleted requirements_.txt", logtype = "REQUIREMENTS")
logs.freeline()

# Import all the tasks main files
logs.log("Start creating all task handlers:", logtype = "TASK_HANDLER")
for item in task_list:
    if item == "__pycache__":
        continue
    
    # Check if the task is enabled in the config file
    current_config = configparser.ConfigParser()
    current_config.read(f"Tasks/{item}/config.ini")
    enabled = current_config["Global"]["Enabled"]

    if enabled == "False":
        logs.log(f"Task {item} is disabled, skipping...", logtype = item)
        continue

    try:
        tasks.append(Task.Task(item, logs))
    except:
        logs.log("Failed to intialize module", logtype = task)
    
logs.log("Finished creating all the tasks in namespace.", logtype = "TASK_HANDLER")
logs.freeline()

logs.log(f"Initialized a total of {len(tasks)} tasks.", logtype = "TASK_HANDLER")
logs.freeline()

# Start the threads for all the tasks
logs.log("Starting all the threads for the tasks:", logtype = "THREAD HANDLER")

threads = []

for task in tasks:
    threads.append([threading.Thread(target=task.run, daemon=True), task.name])
    threads[-1][0].start()
    logs.log(f"Requested thread start for {task.name}", logtype = "THREAD HANDLER")

logs.log("All threads have been requested to start.", logtype = "THREAD HANDLER")
logs.freeline()

# Keep the main thread alive, terminate if termination is True
while True:
    time.sleep(5)
    with open("Termination/termination","r") as f:
        content = f.read()
    
    if content == "True":

        logs.freeline()
        logs.log(f"Termination has been requested, shutting down all tasks ({Utils.get_readable_time()}).", logtype = "TERMINATION")
        logs.log("Shutting down the logger.", logtype = "TERMINATION")
        logs.log(f"Total scheduler uptime: {Utils.convert_seconds_to_readable_time(time.time() - start_time)}", logtype = "TERMINATION")
        logs.close()

        sys.exit(0)