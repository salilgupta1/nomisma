from fabric.api import local, run, hosts
import os


@hosts(['ec2-23-23-210-37.compute-1.amazonaws.com'])
def deploy():
	local('heroku maintenance:on')
	local('git push heroku master')
	#run('psql -d %s -af User.sql' % (os.environ['DATABASE_URL'],))
	#run('psql -d %s -af Transaction_Analytics.sql' % (os.environ['DATABASE_URL'],))
	local('heroku maintenance:off')