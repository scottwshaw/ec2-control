import fabric
from fabric.api import env, run

def hostname():
    print('hostname is ' + run('hostname'))

env.hosts = ['ec2-user@ec2-13-211-24-200.ap-southeast-2.compute.amazonaws.com']
env.key_filename = 'AWSKey02.pem'
fabric.tasks.execute(hostname)
