from datetime import datetime
import os
import time

class Logger:
    def __init__(self):
        self.currentDate = datetime.now()
        self.date_time = self.currentDate.strftime("%d_%m_%Y_%H_%M_%S")

        if not os.path.exists("Logs"):
            os.mkdir("Logs")
            
        self.file = open(f"Logs/logs_{self.date_time}.log","w")

        self.log(f"Logger initialized at {self.currentDate.strftime('%d/%m/%Y at %H:%M:%S')}", logtype = "INFO")
        self.freeline()

    def log(self, message, logtype = "INFO"):
        if "\r" in message:
            for line in message.split("\r"):
                if line != "\n" and line != "\r":
                    self.file.write(f"[{logtype}] "+line.replace("\r","").replace("\n","")+"\n")
        
        else:
            for line in message.split("\n"):
                if line != "\n" and line != "\r":
                    self.file.write(f"[{logtype}] "+line.replace("\r","").replace("\n","")+"\n")

        # Make content of log readable before closing it
        self.file.flush()

    def freeline(self):
        self.file.write("\n")
    
    def close(self):
        self.file.close()
        