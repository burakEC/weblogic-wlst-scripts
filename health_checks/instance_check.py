#redirect('/dev/null', 'false')

connect(userConfigFile='/home/oracle/.keys/wlConfigFile',userKeyFile='/home/oracle/.keys/wlUserKeyFile',url='t3://localhost:7001')
domainConfig()
servers = cmo.getServers()

domainRuntime()
stoppedServers = []
nodeManagerIP = []
nodeManagerPort = []

domain_name=domainName
maxS = 120
print "Domain is: " + domain_name

for server in servers:
        machine = server.getMachine();
        nm = machine.getNodeManager()
        nmIP=nm.getListenAddress()
        nmPORT=nm.getListenPort()
        try:
                cd('/ServerRuntimes/' + server.getName())
                currentState = get('HealthState').getState()

                print currentState;

                x = cmo.getOpenSocketsCurrentCount();
                print server.getName() + ' Open Socket Count = ', x
                if (x >= maxS):
                        print server.getName() + ' Open Socket Count is greater than 120 ',x
                        stoppedServers.append(server.getName())
                        nodeManagerIP.append(nmIP)
                        nodeManagerPort.append(nmPORT)

                if currentState == 0:
                        print server.getName() + ': ' + get('State') + ': HEALTH_OK'
                elif currentState == 1:
                        print server.getName() + ': ' + get('State') + ': HEALTH_WARN'
                        stoppedServers.append(server.getName())
                        nodeManagerIP.append(nmIP)
                        nodeManagerPort.append(nmPORT)
                elif currentState == 2:
                        print server.getName() + ': ' + get('State') + ': HEALTH_CRITICAL'
                        stoppedServers.append(server.getName())
                        nodeManagerIP.append(nmIP)
                        nodeManagerPort.append(nmPORT)
                elif currentState == 3:
                        print server.getName() + ': ' + get('State') + ': HEALTH_FAILED'
                        stoppedServers.append(server.getName())
                        nodeManagerIP.append(nmIP)
                        nodeManagerPort.append(nmPORT)
                elif currentState == 4:
                        print server.getName() + ': ' + get('State') + ': HEALTH_OVERLOADED'
                else:
                        print server.getName() + ': ' + get('State') + ': UNKNOWN HEALTH STATE (' + currentState + ')'

        except WLSTException, e:
                print server.getName() + " is not running."
                stoppedServers.append(server.getName())
                nodeManagerIP.append(nmIP)
                nodeManagerPort.append(nmPORT)

disconnect()

if stoppedServers:
        for ss, mn, mp in zip(stoppedServers, nodeManagerIP, nodeManagerPort):
                print "Found stopped servers first one is " + ss + " running machine at " + mn
                #If you want to email info on the failed server (probably a good idea) and are on Linux you can do something like this
                #os.system('echo "Auto restarting failed server: %s" | /bin/mailx -s  "WARNING: Auto restart failed server" Innova-Telco-Operasyon@innova.com.tr' % stoppedServers[0])
                #nmConnect(userConfigFile='/home/weblogic/user_projects/domains/my_domain/nodemanagerConfig.secure',
                #userKeyFile='/home/weblogic/user_projects/domains/my_domain/nodemanagerKey.secure',
                #host='myhost.mydomain.ie', port='5556', domainName='my_domain',
                #domainDir='/home/weblogic/user_projects/domains/my_domain/', nmType='plain')

                #redirect('/dev/null', 'false')
                nmConnect(host=mn, port=mp, domainName=domain_name, nmType='plain')
                runningStatus = nmServerStatus(ss)
                print "Server " + ss + " current running state is " + runningStatus

                #turn redirect off, we want to see how the server kill and start goes
                #redirect('/dev/null', 'true')
                #kill the server and start it again
                try:
                        print "Killing " + ss + " server..."
                        nmKill(ss)
                        nmStart(ss)
                except WLSTException, e:
                        print "Could not kill server, it may not have been running "
                        print "Starting server " + ss + " using nodemanager "
                        nmStart(ss)
                nmDisconnect()
        exit(exitcode=2)
else:
        exit()
