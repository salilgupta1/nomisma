from fabric.api import local, run, hosts
import os


@hosts(['ec2-23-23-210-37.compute-1.amazonaws.com'])
def deploy():
	local('heroku maintenance:on')
	local('git push heroku master')
	local('heroku maintenance:off')
