pipeline {
	agent any
    
	
	stages {
		stage("Syntax check") {
			steps {
				git url: 'https://github.com/sunchill06/SRE_Assignment.git', branch: 'master'
				sh '''
				echo "Syntax checking playbook"
				# Run a syntax check for the playbook
				ansible-playbook -i ./TASK-2/playbooks/inventory.txt --syntax-check ./TASK-2/playbooks/tomcat-install.yml
				'''
			}
		}
		
		stage("Deploy tomcat using Ansible Playbook") {
			steps {
				ansiblePlaybook(                                                                                                                                                                                                                                    
					[                                                                                                                                                                                                                                               
						credentialsId: "Ansible",                                                                                                                                                                                                      
						inventory: './TASK-2/playbooks/inventory.txt',                                                                                                                                                                                                   
						playbook: './TASK-2/playbooks/tomcat-install.yml',
						hostKeyChecking: false
					]                                                                                                                                                                                                                                               
				)
			}
		}
	}
}
