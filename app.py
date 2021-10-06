
from flask import Flask , render_template

 
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
#a) (host, request-count) tuples for the top-10 frequent hosts


from flask.wrappers import Request


def usercount(reques):
    #reques is a list made from request where each request is split by ' '  
    #this function returns all users and number of times they put in requests
    users={}
    for i in range(len(reques)):
        if(reques[i][0] not in users):
            users[reques[i][0]]=1
        if(reques[i][0] in users):
            users[reques[i][0]]+=1
    return users


def total_requests(users):
    #users is a dictionary with format {ip: occurences}  
    #this function returns the number of total requests in LOG
    sum=0
    for i in users:
        sum=sum+users[i]

    return sum

def top_ten_users(users):
    if(len(users)<=10):
        return users
    #users is a dictionary with format {ip: occurences}  
    #this function returns a list of top 10 users
    final_list=[]
    for i in range(10):
        max1=0
        for j in users:
            if(users[j]>max1):
                max1=j
        del users[max1]
        final_list.append(max1)
    return final_list
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#b) (HTTP-status-code, count)

def status_cc(reques):
    #takes same reques as above and returns dictionary different status codes and 
    # how many times they are called

    status=dict()
    for i in reques:
        if(i[8] not in status):
            status[i[8]]=1
        if(i[8]in status):
            status[i[8]]+=1
    return status

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#c) the hour with the highest request count, along with the count
def busy_hour(reques):
    dates=[]
    for i in reques:
        dates.append(i[3].strip('[').split(':'))
    
    
    hour={}
    for i in dates:
        if(i[0]+' '+i[1] not in hour):
            hour[i[0]+' '+i[1]]=1
        if(i[0]+' '+i[1] in hour):
            hour[i[0]+' '+i[1]]+=1
    max1=0
    for i in hour:
        if hour[i]>max1:
            max1=hour[i]
    for i in hour:
        if hour[i]==max1:
            return i +' : '+ str(hour[i])
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#d) the hour with the highest total number of bytes served, along with the total

def bytes_served(reques):
    hours=[]
    for i in reques:
        hours.append([i[3].strip('[').split(':'),i[9]])
    timee={}
    for i in hours:
        if( i[0][0]+' '+i[0][1] not in timee):
            timee[i[0][0]+' '+i[0][1]]=int(i[1])
        if(i[0][0]+' '+i[0][1] in timee):
            timee[i[0][0]+' '+i[0][1]]+=int(i[1])
    max1=0
    for i in timee:
        if timee[i]>max1:
            max1=timee[i]
    for i in timee:
        if timee[i]==max1:
            return i +' : '+ str(timee[i])
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def resource_req(reques):
    #reques is a list made from request where each request is split by ' '  
    #this function returns top 10 requested resources
    resource={}
    final_list=[]
    for i in range(len(reques)):
        if(reques[i][6] +' '+reques[i][7] not in resource):
            resource[reques[i][6]+' '+reques[i][7]]=1
        if(reques[i][6] +' '+reques[i][7] in resource):
            resource[reques[i][6]+' '+reques[i][7]]+=1
    

    if(len(resource)<=10):
        for i in resource:
            final_list.append(i)
        return final_list
    #resource is a dictionary with format {ip: occurences}  
    #this function returns a list of top 10 resource
    
    for i in range(10):
        max1=0
        for j in resource:
            if(resource[j]>max1):
                max1=j
        del resource[max1]
        final_list.append(max1)
    return final_list
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

filepath="/var/log/apache2/access.log"
data = open('access.log', "r").readlines()
reques=list()
for i in data:
    reques.append(i.split(' '))

#client address stored at [0]
#date time stored at [3]
#request stored at[5]
#status code stored at [8]
#bytes served [9]
#module reqyuested at [6][7]

users=usercount(reques)
usernumber=total_requests(users)
top_user=top_ten_users(users)
status=status_cc(reques)
busy_req=busy_hour(reques)
bytes_s=bytes_served(reques)
freq_resources=resource_req(reques)

print("top_10_users with counts   ",top_user)
print("status_code,count   ",status)
print("busy hour : requests   ",busy_req)
print("bytes served : hour  ",bytes_s)
print("most requested resource : ",freq_resources)




app = Flask(__name__)
@app.route('/')

def index():
    return render_template('index.html',top_user=top_user,status=status,busy_req=busy_req,bytes_s=bytes_s,freq_resources=freq_resources)
    
 
# main driver function
if __name__ == '__main__':
 

    app.run(debug=True)