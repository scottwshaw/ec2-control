#/usr/bin/python
 
import boto.ec2

conn = boto.ec2.connect_to_region("ap-southeast-2")
instances = conn.get_only_instances()
for instance in instances:
    if 'myinstance' in instance.tags:
        if instance.state in ('running', 'stopped', 'pending'):
            print 'Terminating ' + instance.public_dns_name
            instance.terminate()
