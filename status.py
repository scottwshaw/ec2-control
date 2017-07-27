#/usr/bin/python
 
import boto.ec2

conn = boto.ec2.connect_to_region("ap-southeast-2")
instances = conn.get_all_instances()
for instance in instances:
    print(instance.tags)
