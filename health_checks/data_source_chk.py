import time
import datetime
import os
print "Last Updated at " , datetime.datetime.now()
connect(userConfigFile='/home/oracle/.keys/wlConfigFile',userKeyFile='/home/oracle/.keys/wlUserKeyFile',url='t3://localhost:7001')
allServers=domainRuntimeService.getServerRuntimes();
maxDS = 150
stc = 0
if (len(allServers) > 0):
        for tempServer in allServers:
                jdbcServiceRT = tempServer.getJDBCServiceRuntime();
                dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();

                if (len(dataSources) > 0):
                        for dataSource in dataSources:
                                print 'Name                               '  ,  dataSource.getName()
                                print 'State                              '  ,  dataSource.getState()
                                print 'Open Socket Count                  '  ,  dataSource.getActiveConnectionsCurrentCount()
                                socketCount = dataSource.getActiveConnectionsCurrentCount()
                                if (dataSource.getState() == 'Shutdown'):
                                        dataSource.start()
                                        print dataSource.getName()+"'s status is now = "+dataSource.getState()
                                        stc = 2
                                if (dataSource.getState() != 'Running'):
                                        dataSource.reset()
                                        print dataSource.getName()+"'s status is now = "+dataSource.getState()
                                        stc = 2
                                if (socketCount >= maxDS):
                                        dataSource.shutdown()
                                        print dataSource.getName()+"'s status is now = "+dataSource.getState()
                                        dataSource.start()
                                        print dataSource.getName()+"'s status is now = "+dataSource.getState()
                                        stc = 2
disconnect()
if stc == 2:
        exit(exitcode=2)
else:
        exit()
