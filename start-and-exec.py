#/usr/bin/python
 
import boto.ec2
from fabric.api import env, run
from time import sleep

def wait_til_started(instance):
    state = instance.state
    while state not in ('running', 'stopped'):
        sleep(5)
        instance.update()
        state = instance.state
        print " state:", state

conn = boto.ec2.connect_to_region("ap-southeast-2")
ubuntu_ami = 'ami-e94e5e8a'
tensorflow_ami = 'ami-52332031'
reservation = conn.run_instances(
    tensorflow_ami,
    key_name='AWSKey02',
    instance_type='t2.micro',
    security_groups=['launch-wizard-2']
)

for instance in reservation.instances:
    instance.add_tag('myinstance')

wait_til_started(reservation.instances[0])
hostname = reservation.instances[0].public_dns_name
print('new host is ' + hostname)

# env.hosts = [hostname]
# env.user = 'ubuntu'
# env.key_filename = '~/Work/AWSKey02.pem'
# run('hostname')



    
