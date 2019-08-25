-------------------------------------------------------------------------------------------------
TASK 3 : Jenkins Pipeline to deploy Tomcat server using Ansible playbook
-------------------------------------------------------------------------------------------------

Pre-Requisites and Assumptions:

1. Using Ansible playbook written in Task 2.
2. Jenkins is installed and Ansible Plugin for Jenkins is installed and configured. Add the Ansible executable path inside Jenkins -> Manage Jenkins -> Global Tool Configuration
3. Also Add the Git Executable path inside Jenkins -> Manage Jenkins -> Global Tool Configuration
4. Add the Global Credentials for the Target host where Tomcat has to be installed i.e. the Target for Ansible Playbook. Credentials -> System -> Add Credentials (Type: Username with Password) e.g. ansible/Password

-------------------------------------------------------------------------------------------------

Setting up the Pipeline Job:

1. Create a new item and select Pipeline as the Type of the Job.
2. Configure the Pipeline Job and choose the "Pipeline script from SCM" option
3. Choose "GIT" as the SCM Source
4. Choose the Relevant Repository URL, e.g. https://github.com/sunchill06/SRE_Assignment.git, This is where our Jenkinsfile is present along with Ansible Playbooks.
5. Choose the credentials from the Credentials earlier created for authentication with target host.
6. Specify appropriate branch .e.g master or develop
7. Apply and Save.
8. Click on Build Now under the newly created Job/Project and Check the logs for the Job to see the progress. If all is configured well, you should see SUCCESS at the end.

Note: A Snapshot of above steps is attached as part of the repository for reference.

-------------------------------------------------------------------------------------------------
Sample Console Output for the Jenkins Pipeline:
---------------------------------------------------------------------------------------------------------------

Started by user Sunil Aggarwal
Obtained Jenkinsfile from git https://github.com/sunchill06/jenkins_pipeline.git
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/Tomcat_Installation_Pipeline
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Declarative: Checkout SCM)
[Pipeline] checkout
using credential Ansible
Cloning the remote Git repository
Cloning repository https://github.com/sunchill06/jenkins_pipeline.git
 > /bin/git init /var/lib/jenkins/workspace/Tomcat_Installation_Pipeline # timeout=10
Fetching upstream changes from https://github.com/sunchill06/jenkins_pipeline.git
 > /bin/git --version # timeout=10
using GIT_ASKPASS to set credentials Ansible Target host
 > /bin/git fetch --tags --progress https://github.com/sunchill06/jenkins_pipeline.git +refs/heads/*:refs/remotes/origin/*
 > /bin/git config remote.origin.url https://github.com/sunchill06/jenkins_pipeline.git # timeout=10
 > /bin/git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
 > /bin/git config remote.origin.url https://github.com/sunchill06/jenkins_pipeline.git # timeout=10
Fetching upstream changes from https://github.com/sunchill06/jenkins_pipeline.git
using GIT_ASKPASS to set credentials Ansible Target host
 > /bin/git fetch --tags --progress https://github.com/sunchill06/jenkins_pipeline.git +refs/heads/*:refs/remotes/origin/*
 > /bin/git rev-parse refs/remotes/origin/master^{commit} # timeout=10
 > /bin/git rev-parse refs/remotes/origin/origin/master^{commit} # timeout=10
Checking out Revision 6980fbe0670673c086268b96e98e54a1acb15bb9 (refs/remotes/origin/master)
 > /bin/git config core.sparsecheckout # timeout=10
 > /bin/git checkout -f 6980fbe0670673c086268b96e98e54a1acb15bb9
Commit message: "Checking in Jenkinsfile"
First time build. Skipping changelog.
[Pipeline] }
[Pipeline] // stage
[Pipeline] withEnv
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Syntax check)
[Pipeline] git
No credentials specified
 > /bin/git rev-parse --is-inside-work-tree # timeout=10
Fetching changes from the remote Git repository
 > /bin/git config remote.origin.url https://github.com/sunchill06/jenkins_pipeline.git # timeout=10
Fetching upstream changes from https://github.com/sunchill06/jenkins_pipeline.git
 > /bin/git --version # timeout=10
 > /bin/git fetch --tags --progress https://github.com/sunchill06/jenkins_pipeline.git +refs/heads/*:refs/remotes/origin/*
 > /bin/git rev-parse refs/remotes/origin/master^{commit} # timeout=10
 > /bin/git rev-parse refs/remotes/origin/origin/master^{commit} # timeout=10
Checking out Revision 6980fbe0670673c086268b96e98e54a1acb15bb9 (refs/remotes/origin/master)
 > /bin/git config core.sparsecheckout # timeout=10
 > /bin/git checkout -f 6980fbe0670673c086268b96e98e54a1acb15bb9
 > /bin/git branch -a -v --no-abbrev # timeout=10
 > /bin/git checkout -b master 6980fbe0670673c086268b96e98e54a1acb15bb9
Commit message: "Checking in Jenkinsfile"
[Pipeline] sh
+ echo 'Syntax checking playbook'
Syntax checking playbook
+ ansible-playbook -i ./TASK-2/playbooks/inventory.txt --syntax-check ./TASK-2/playbooks/tomcat-install.yml

playbook: ./TASK-2/playbooks/tomcat-install.yml
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Deploy tomcat using Ansible Playbook)
[Pipeline] ansiblePlaybook
[Tomcat_Installation_Pipeline] $ sshpass ******** ansible-playbook ./TASK-2/playbooks/tomcat-install.yml -i ./TASK-2/playbooks/inventory.txt -u ansible -k

PLAY [Tomcat deployment playbook] **********************************************

TASK [Gathering Facts] *********************************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Install JDK] ****************************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Add Tomcat group] ***********************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Add Tomcat user] ************************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : create tomcat installation directory] ***************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Download Tomcat Package] ****************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Extract the Tomcat Package] *************************************
skipping: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Copy tomcat service file] ***************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Copy tomcat server.xml file] ************************************
ok: [itsmebharat842c.mylabserver.com]

TASK [tomcat : Start and enable tomcat] ****************************************
ok: [itsmebharat842c.mylabserver.com]

PLAY RECAP *********************************************************************
itsmebharat842c.mylabserver.com : ok=9    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS
