# mynest
Very simple python module to interface with google nest.
Finally Google provides access to Nest thermostats in their new API. 
I wrote this simple module to access and control my thermostat. 
You need to edit the code and add your own IDs to get it to work. Just follow the comments.

# mysql_controller_module
Very simple insert statement so that it is straighforward to log data from mynest.
You need to edit to code to get it to work for your situation

# mynest_logging_example.py
This example runs a loop,
It pulls information from mynest.
If the observed temperature range is more than 2 degrees it turns on the fan (if in AC mode and not already cooling)
then it logs the data into mysqll
and sleeps for 20 minutes each time.
