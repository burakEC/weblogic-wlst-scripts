redirect('/dev/null', 'false')

connect(userConfigFile='/home/oracle/.keys/wlConfigFile',userKeyFile='/home/oracle/.keys/wlUserKeyFile',url='t3://localhost:7001')
cd ('AppDeployments')
myapps=cmo.getAppDeployments()
statusCode=0
 
for appName in myapps:
       domainConfig()
       cd ('/AppDeployments/'+appName.getName()+'/Targets')
       mytargets = ls(returnMap='true')
       domainRuntime()
       cd('AppRuntimeStateRuntime')
       cd('AppRuntimeStateRuntime')
       for targetinst in mytargets:
             curstate4=cmo.getCurrentState(appName.getName(),targetinst)
             if curstate4 != 'STATE_ACTIVE':
                 print 'App -', appName.getName(), '@', targetinst, ' is not running. Starting app...'
                 startApplication(appName.getName())
                 statusCode=2
             else:
                 print 'App -', appName.getName(), '@', targetinst, '->', curstate4

disconnect()

if statusCode == 2:
    exit(exitcode=2)
else:
    exit()
