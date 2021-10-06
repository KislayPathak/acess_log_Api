# acess_log_Api
extract data through your access.log file from apache webserver


1. copy app.py and templates folder in base directory of your project
        make sure python3 is installed
        install flask using pip 
        use command pip install flask
2. open app.py 
        look for variable named:"filepath"
        pass the variable filepath in next line method to open file
        check if it is set to your access.log      --filepath(default)="/var/log/apache2/access.log"
3.change routes based on your server
