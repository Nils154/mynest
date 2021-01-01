# mynest.py
Very simple python module to interface with google nest.
Finally Google provides access to Nest thermostats in their new API. 
I wrote this simple module to access and control my thermostat. 
You need to edit the code and add your own IDs to get it to work. Just follow the comments.

# mysql_controller_module.py
Very simple insert statement so that it is straighforward to log data from mynest.
You need to edit to code to get it to work for your situation

# mynest_logging_example.py
This example runs a loop,
It pulls information from mynest.
If the observed temperature range is more than 2 degrees it turns on the fan (if in AC mode and not already cooling)
then it logs the data into mysql and sleeps for 20 minutes each time.

# grafana
If you have mysql installed and your python code logging data, you can install grafana: https://grafana.com/tutorials/install-grafana-on-raspberry-pi/#3

Create a new mysql user in mysql: https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql

Grant it only 'SELECT' access to your mynestdb table.
Create a datasource to your local mysql database in grafana from its webinterface.
You can import the two json example panels.
