##So the basic tree stucture we're walking looks like this:
##ServerRuntimes
##|--< Server (all servers)
##    |--< Application run times (all deployments)
##        |--< Work manager runtimes (all work managers)
## 
##We could probably enumerate all threads and see which are stuck, but this 
##way you can much easier manager the output. As you can see in this tree
##for example, you know which deployment has stuck threads
##'''
## Prevent printing output to the screen
redirect('/dev/null','false')
 
## Insert your own password here
connect(userConfigFile='/home/oracle/.keys/wlConfigFile',userKeyFile='/home/oracle/.keys/wlUserKeyFile',url='t3://localhost:7001')
 
domainRuntime()
servers = ls('/ServerRuntimes','true','c')
 
# We'll store all results in here, using the server name for a key
result=dict()
for server in servers:
    deployments = ls('/ServerRuntimes/' + server + '/ApplicationRuntimes','true','c')
    result[server] = 0;
    for deployment in deployments:
        ## If you are only interested in a single deployment, run that check here, like
        ## if(deployment.getName() == "MyApplication"):
 
        ## Could be that there are multiple workmanagers, I'm not sure, so let's iterate over them
        wms = ls('/ServerRuntimes/'  + server + '/ApplicationRuntimes/' \
        + deployment + '/WorkManagerRuntimes','true','c')
        for wm in wms:
            cd('/ServerRuntimes/' + server + '/ApplicationRuntimes/' \
            + deployment + '/WorkManagerRuntimes/' + wm) 
            result[server] = result[server] + get('StuckThreadCount')
 
## Reenable printing output
redirect('/dev/null','true')
 
## Print all server names and the number of stuck threads we counted per server
## Format for Nagios output etc. from here
for key in result:
        print(key + " has "  + str(result[key]) + " stuck threads.")
