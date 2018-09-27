/******************************* PREREQUISITES ***************************************/

The following software needs to be installed on a Mac OS:
1. ansible
`brew install ansible`

2. Python Virtual Env Wrapper
`pip install virtualenvwrapper`

3. boto
`pip install boto boto3`

/******************************* PREPARE ***************************************/

 ***Note: Have an AWS account and Secret Keys ready***

1. Edit ansible.cfg and change the private_key_file

2. Check and/or update files under files/ with the desired installation packages.
mongodb-mms-3.6.2.596-1.x86_64.rpm  -> ops manager installation kit
mongodb.repo                        -> repo file to download mongodb installation kits
userdemo.json                       -> Ops Manager first user details
parameters_om.config                -> Ops Manager configuration parameters. These values are typically provided during the first set up using the web UI.
Ops Manager web UI url is added at the end automatically.

3. Add the following variables to ~/.bash_profile and source it
$AWS_ACCESS_KEY
$AWS_SECRET_KEY
$AWS_GROUP_ID

4. Modify variables under group_vars/all with the required values:
ami_id: ami-d834aba1
instance_type_om: m3.xlarge  -> general recommendation is to use this for OM instance
instance_type_rs: t2.small
rs_size: 3            -> replica set size
key_name:             -> AWS key
aws_region:           -> AWS region where the instances will be created
tags_om: {"owner": "veronica.tudor", "expire-on": "2018-04-10", "Name": "veronica-demo-om", "project":"Veronica Ops Manager Demo"}
tags_rs: {"owner": "veronica.tudor", "expire-on": "2018-04-10", "Name": "veronica-demo-rs", "project":"Veronica Ops Manager Demo"}
opsmanager_kit        -> must match the installation kit name present under files/


5. Modify lines 6,7,8 in addNewHosts.py. The values must match those in groups_vars/all
conn = boto.ec2.connect_to_region("...")
keyname = "..."   -> key_name in group_vars/all
project = "..."   -> project in tags_om


/***************************** DEPLOY *****************************************/

Run setup.sh from within the om-demo directory:
`./setup.sh`

--------------
This will:
  5.1. Prepare the hosts file

  5.2. Run ansible to create the AWS instances for OM and 3 members RS
      `ansible-playbook -i hosts playbooks/ansible-aws.yml`

  5.2. Append AWS instance names to hosts file - inventory
       `python addNewHosts.py`

  5.3. Install OM
       `ansible-playbook -i hosts playbooks/ansible-install-om.yml`

  5.4. Append the new instances to the hosts file

  5.5. Configure OM
       `ansible-playbook -i hosts playbooks/ansible-config-om.yml`

       5.5.1. Create HEAD dir on Ops Manager host
       5.5.2. Create a first user for OM
       5.5.3. Create a first group
       5.5.4.  Add configuration paramters from parameters_om.config to /opt/mongodb/mms/conf/conf-mms.properties and restart Ops manager

       5.5.5. Configure Replica Set members, add automation agent and mongodb enterprise

Before the following step you need to manually add your IP to the Whitelist.
   5.6. Onboard the replicaset
   (here for AWS I need a slightly different approach because of the internal hostnames vs. DNS names of AWS instances )


-----------------------
The Following files are produced:
first user details are saved under: /home/ec2-user/firstuser.json
the group created (Group Demo) has the details recorded under: /home/ec2-user/omgroup.json

------------------------


Backup considerations:
/data/HEAD is the The configured backup directory
Blockstore is configured as method to store MongoDB Snapshots
localhost:27017 is the connection to the blockstore database (where localhost is actually the Ops Man server)


---------------------------------------------
LEFT TO DO after running the ./setup script
-- need to manually enable the backup for the cluster
-- need to enable the backup for the cluster
-- load data
-- start workload


-- To query a snapshot use:
- First add an entry in /etc/hosts for ops manager server
- Run the following: ./tunnel-5ae094067e669818053f4763 --remote om.demo:25999 -v
