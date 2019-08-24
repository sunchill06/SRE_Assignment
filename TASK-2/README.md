-------------------------------------------------------------------------------------------------
TASK 2 : Tomcat Server installation using Ansible Playbook
-------------------------------------------------------------------------------------------------

Pre-Requisites and Assumptions:

1. Ansible should be installed on the Machine.
2. This playbook will install Tomcat version 9.0.24 onto the Target hosts
3. Playbook will be flexible to provide multiple tomcat installations on the same host, which will further be described below.
4. Playbook will install Tomcat inside /usr/share/tomcat{http_port} e.g. /usr/share/tomcat8080 on the Target host. 
   This is done for multiple installations of tomcat on the same node.
5. Similar to point 4, User/Group for this installation will be tomcat{http_port} e.g. tomcat8080 
6. Same format is kept for systemd service as well and the service will be tomcat{http_port} e.g. tomcat8080

-------------------------------------------------------------------------------------------------a

Snapshot of the Folder structure in Ansible Playbook:

[ansible@controller TASK-2]$ cat playbooks/inventory.txt 
[target]
target1

[ansible@controller TASK-2]$ tree playbooks/
playbooks/
├── inventory.txt
├── roles
│   └── tomcat
│       ├── defaults
│       │   └── main.yml
│       ├── handlers
│       │   └── main.yml
│       ├── meta
│       │   └── main.yml
│       ├── README.md
│       ├── tasks
│       │   ├── main.yml
│       │   └── tomcat-setup.yml
│       ├── templates
│       │   ├── server.xml.j2
│       │   └── tomcat.service.j2
│       └── vars
│           └── main.yml
└── tomcat-install.yml

-------------------------------------------------------------------------------------------------

Case 1. Default Tomcat installation [without any cutom arguments and will make the Tomcat server run on HTTP Port 8080]

[ansible@controller playbooks]$ ansible-playbook -i inventory.txt tomcat-install.yml 

PLAY [Tomcat deployment playbook] **************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************
ok: [target1]

TASK [tomcat : Install JDK] ********************************************************************************************************************************************
changed: [target1]

TASK [tomcat : Add Tomcat group] ***************************************************************************************************************************************
changed: [target1]

TASK [tomcat : Add Tomcat user] ****************************************************************************************************************************************
changed: [target1]

TASK [tomcat : create tomcat installation directory] *******************************************************************************************************************
changed: [target1]

TASK [tomcat : Download Tomcat Package] ********************************************************************************************************************************
changed: [target1]

TASK [tomcat : Extract the Tomcat Package] *****************************************************************************************************************************
changed: [target1]

TASK [tomcat : Copy tomcat service file] *******************************************************************************************************************************
changed: [target1]

TASK [tomcat : Copy tomcat server.xml file] ****************************************************************************************************************************
ok: [target1]

TASK [tomcat : Start and enable tomcat] ********************************************************************************************************************************
changed: [target1]

PLAY RECAP *************************************************************************************************************************************************************
target1                    : ok=11   changed=9    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 


[ansible@target1 ~]$ systemctl status tomcat8080
● tomcat8080.service - Tomcat
   Loaded: loaded (/etc/systemd/system/tomcat8080.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2019-08-24 06:37:58 EDT; 3min 38s ago
  Process: 8139 ExecStart=/usr/share/tomcat8080/bin/catalina.sh start (code=exited, status=0/SUCCESS)
 Main PID: 8144 (java)
   CGroup: /system.slice/tomcat8080.service
           └─8144 /usr/lib/jvm/jre/bin/java -Djava.util.logging.config.file=/usr/share/tomcat8080/conf/logging.properties -Djava.util.logging.manager=org.apache.juli...
		   
		   

------------------------------------------------------------------------------------------------------------------------------------------------

Case 2. Custom Tomcat installation on the same node [with cutom arguments and will make the Tomcat server run on HTTP (and other ports) Port provided in playbook arguments,
specified by --extra-args parameter]

[ansible@controller playbooks]$ ansible-playbook -i inventory.txt tomcat-install.yml --extra-vars "http_port=8081 https_port=8444 shutdown_port=8006 connector_port=8010"

PLAY [Tomcat deployment playbook] **************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************
ok: [target1]

TASK [tomcat : Install JDK] ********************************************************************************************************************************************
ok: [target1]

TASK [tomcat : Add Tomcat group] ***************************************************************************************************************************************
changed: [target1]

TASK [tomcat : Add Tomcat user] ****************************************************************************************************************************************
changed: [target1]

TASK [tomcat : create tomcat installation directory] *******************************************************************************************************************
changed: [target1]

TASK [tomcat : Download Tomcat Package] ********************************************************************************************************************************
ok: [target1]

TASK [tomcat : Extract the Tomcat Package] *****************************************************************************************************************************
changed: [target1]

TASK [tomcat : Copy tomcat service file] *******************************************************************************************************************************
changed: [target1]

TASK [tomcat : Copy tomcat server.xml file] ****************************************************************************************************************************
changed: [target1]

TASK [tomcat : Start and enable tomcat] ********************************************************************************************************************************
changed: [target1]

PLAY RECAP *************************************************************************************************************************************************************
target1                    : ok=11   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


[ansible@target1 ~]$ systemctl status tomcat8081
● tomcat8081.service - Tomcat
   Loaded: loaded (/etc/systemd/system/tomcat8081.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2019-08-24 06:42:37 EDT; 1min 24s ago
  Process: 15691 ExecStart=/usr/share/tomcat8081/bin/catalina.sh start (code=exited, status=0/SUCCESS)
 Main PID: 15696 (java)
   CGroup: /system.slice/tomcat8081.service
           └─15696 /usr/lib/jvm/jre/bin/java -Djava.util.logging.config.file=/usr/share/tomcat8081/conf/logging.properties -Djava.util.logging.manager=org.apache.jul...

---------------------------------------------------------------------------------------------------------------------------

Improvement Ideas:

1. Instead of --extra-args, playbook can also ask for Port details as user input using vars_prompt option in task. User then, however be prompted in case of
   default installation case as well.
2. A Clean-up script for uninstallation. 
3. Some mechanism to suggest users on the available ports on the target machine or existing ports being used.
		   
---------------------------------------------------------------------------------------------------------------------------		  
