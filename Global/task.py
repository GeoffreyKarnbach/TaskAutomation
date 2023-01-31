import importlib
import time
import configparser
from datetime import datetime
import Global.utils as Utils
import traceback

class Task:
    def __init__(self, taskname, logger):
        self.name = taskname
        self.logger = logger
        self.lastExecuted = 0
        self.module = None

        self.config = configparser.ConfigParser()
        self.config.read(f"Tasks/{self.name}/config.ini")
        self.interval = int(self.config["Frequency"]["EveryXMinutes"])

        if self.config["Global"]["RunOnStartup"] == "True":
            self.firstExecuted = False
        else:
            self.firstExecuted = True

        self.initialize()
    
    def initialize(self):
        self.module = importlib.import_module(f"Tasks.{self.name}.main")
        self.logger.log(f"Load {self.name}.main", logtype = "TASK_HANDLER")

        response = self.module.initialize()
        self.logger.log(response, logtype = self.name)
    
    def run(self):
        self.logger.log(f"Starting thread for {self.name}", logtype = self.name)
        time.sleep(5)
        while True:
            if (self.lastExecuted + self.interval * 60 <= time.time() and Utils.is_in_interval(self.config["Frequency"]["AllowedFrom"], self.config["Frequency"]["AllowedTo"])) or not self.firstExecuted:
                
                if not self.firstExecuted:
                    self.firstExecuted = True
                    
                self.lastExecuted = time.time()

                self.currentDate = datetime.now()
                self.date_time = self.currentDate.strftime("%d_%m_%Y_%H_%M_%S")

                self.logger.log(f"Executing {self.name} at {self.currentDate.strftime('%d/%m/%Y at %H:%M:%S')}", logtype = self.name)

                if self.config["Global"]["Testing"] == "True":
                    self.logger.log(f"Testing mode is enable for task {self.name}, main function will not be run.", logtype = self.name)
                else:
                    error = False
                    start_time = time.time()
                    response = ""
                    
                    try:
                        response = self.module.main()
        
                    except Exception as e:
                        
                        error = True
                        error_message = traceback.format_exc()
                        response = "Failed to execute task"
                        

                    self.logger.log(f"{response} after {(time.time()-start_time):.2f} seconds.", logtype = self.name)

                    if error:
                        self.logger.freeline()
                        
                        if "\n" in str(error_message):
                            for line in str(error_message).split("\n"):
                                if line != "":
                                    self.logger.log(f"{line}", logtype = "ERROR")
                        else:
                            for line in str(error_message).split("\r"):
                                if line != "":
                                    self.logger.log(f"{line}", logtype = "ERROR")
                        
                        self.logger.freeline()
            else:
                time.sleep(5)