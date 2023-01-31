# <u>Task Automation Tool</u>

## <u> Usage of the tool</u>

Often, it is very usefull to be able to execute a same task every day/hour, in a repeated way, in order to backup data for instance or mesure values. The "Task Automation Tool" is meant to be run on a computer, that is powered on 24/7. <br><br>
Each task, that the server should execute on a regular basis, is defined by a single folder in the "Tasks" directory:

### How to create a new Task:

To create a new task, you will need to create a subdirectory in "Tasks" with following structure: <br><br>

```
Tasks
↳ TASKNAME
  ↳ main.py
  ↳ config.ini
  ↳ requirements.txt
  ↳ Output
    ↳ ...
```

Each file has a specific role:

- main.py: This file will contain the code to be run by the program. It has to contain at least two predefined functions, used by the scheduler:

  - <strong>main()</strong>: This function is run everytime the task is triggered.<br>
  - <strong>initialize()</strong>: This function returns a string and can be used to initialize values. The returned string is written to the logs and makes sure that this task has been sucessfully loaded.

- config.ini: This file will contain two main sections, each containing different important fields for the scheduler to be able to configure the task execution:
  - "EveryXMinutes" (in "Frequency" section): This field takes a positive integer, representing the amount of minutes, that have to pass between two executions of the task.
  - "AllowedFrom" (in "Frequency" section): This field takes a time of format HH:MM, and it indicates the beginning of the period, where the task is allowed to be run.
  - "AllowedTo" (in "Frequency" section): This field takes a time of format HH:MM, and it indicates the end of the period, where the task is allowed to be run.
    <br><br>
  - "Enabled" (in "Global" section): This field takes a value ("True"/"False") and indicates, wether a task should be loaded by the scheduler at program start.
  - "Testing" (in "Global" section): This field takes a value ("True"/"False") and indicates, wether a task should be run normally or in test mode (=only logging a run confirmation but no "main" function execution).
  - "RunOnStartup" (in "Global" section): This field takes a value ("True"/"False") and indicates, wether a task should be auto run once at scheduler launch/startup.

<br>

- requirements.txt: This file will contain a list of all python modules, that pip need to install, in order to be able to run this specific task. The file should be compatible with the command <u><strong>pip install -r requirements.txt</strong></u>.

- Ouput: This is a folder, that the main.py file should automatically generate, if it needs to output some files (for instance results of a backup / test).

<br>

It is possible for the user to use several files/modules, for instance a file called "module1.py" can be added in the subdirectory. In order to be able to import it, following import statement has to be used in the main.py file:

> import Tasks.TASKNAME.module1 as module1

### How to terminate the program (for maintenance for instance)

> python3 terminate.py

### How to start the program using SSH on a remote machine

> tmux
> <br>
> python3 main.py
> <br>
> tmux detach
> <br>
> exit
