#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}1. Preparing the hosts file..."
rm hosts
cp hosts.default hosts

echo ""
echo "2. Running ansible to create AWS instances for Ops Manager and Replica Set..."
echo "${reset}Check the log at logs/ansible-aws.log"
ansible-playbook -i hosts playbooks/ansible-aws.yml > logs/ansible-aws.log

SORTIDA=$?
if [ "$SORTIDA" -eq 0 ];
then
    echo "${green}OK creating the AWS instances"
    echo ""
    echo "3. Adjusting hosts file with the AWS instance names..."
    python addNewHosts.py > logs/addNewHosts.log

    echo ""
    echo "The hosts file has been modified and this is how it looks now:"
    echo "${reset}"
    cat hosts

    echo "${green}"
    read -rsp $'4. If the file looks OK (all vars have values and all Replica Set members are listed) press any key to continue...\n' -n1 key
    echo ""

    echo "${green}"
    echo "5. Configuring /etc/hosts file on AWS instances with custom hostnames defined under files/customHostnames.txt"

    ansible-playbook -i hosts playbooks/ansible-config-hosts.yml > logs/ansible-config-hosts.log

    SORTIDA=$?
    echo "Waiting for the EC2 instances to come up after reboot..."
    sleep 180

    if [ "$SORTIDA" -eq 0 ];
      then
        echo "6. Installing Ops Manager"
        echo "${reset}Check the log at logs/ansible-install-om.log"

        ansible-playbook -i hosts playbooks/ansible-install-om.yml > logs/ansible-install-om.log

        SORTIDA=$?
        if [ "$SORTIDA" -eq 0 ];
        then
          echo "${green}OK installing Ops Man"
          echo ""
          om_url=`grep "opsmanagerurl=" hosts| head -1| sed 's/opsmanagerurl=/mms.centralUrl=/'`
          echo $om_url >> files/parametersOM.config

          echo "7. Configure OM"
          echo "${reset}Check the log at logs/ansible-config-om.log"
          ansible-playbook -i hosts playbooks/ansible-config-om.yml > logs/ansible-config-om.log

          SORTIDA=$?
          if [ "$SORTIDA" -eq 0 ];
            then
              echo "${green}Ops Manager has been configured successfully"
              echo ""

              echo "$reset"
              tail -2 hosts
              echo "${green}"
              read -rsp $'Login to OM web UI and
              1. add OM server IP to the Whitelist.
              2. enable Enterprise builds in Version Manager.
              Then return here and press any key to continue...' -n1 key
              echo ""

              echo "8. Onboarding Replica Set"
              echo "${reset}Check the logs at logs/ansible-onboard-rs.log"

              ansible-playbook -i hosts playbooks/ansible-onboard-rs.yml > logs/ansible-onboard-rs.log

              SORTIDA=$?
              if [ "$SORTIDA" -eq 0 ];
                then
                  echo ""
                  echo "${green}Replica Set was onboarded successfully"
                  echo "!!! Don't forget to configure and start BACKUP before loading any data to your database !!!"
                  echo "The head directory for the backup daemon has been created : /data/HEAD"
                  echo "The address for the blockstore database is localhost:27017"
                  echo ""

                else
                  echo "${red}Oups! There was a problem onboarding Replica Set. Check  logs/ansible-onboard-rs.log for more details"
              fi

            else
                echo "${red}There was a problem configuring Ops Manager. Check  logs/ansible-config-om.log for more details"
          fi
        else
            echo "${red}Failed to install Ops Man"
            exit
      fi
    else
        echo "${red}Failed to configure custom hostnames"
    fi
else
    echo "${red}Failed to create AWS instances"
fi
