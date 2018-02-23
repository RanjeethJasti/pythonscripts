import sys
import json
import requests
import time
import progressbar
import os

def generate_configs(sitename, tag):

	site = "%s:%s" %(sitename, tag)
	num = int(tag)
	ID = ['blue' if num%2 else 'green']
	global app_id
	app_id = "%s-%s" %(sitename, ID[0])
	file1 = open("template_app.json")
	file2 = open("app_config.json", 'w')
	for i in file1.readlines():
		if "<ID>" or "<SITENAME>" in i:
			if "<ID>" in i:
				i = i.replace("<ID>", app_id)
			
			elif "<SITENAME>" in i:
				i = i.replace("<SITENAME>:<TAG>", site)
		file2.write(i)
	file2.close()
	file2 = open("app_config.json", 'r')
	data = json.load(file2)
	file2.close()
	formatted_data = json.dumps(data, indent=4, sort_keys=False)
	file2 = open("app_config.json", 'w')
	file2.write(formatted_data)
	file2.close()

def check_app_status(app_id):

	message = "Checking status of your app %s. Please hold on." %app_id
	print message

	for i in range(9):
		url = "http://192.168.33.51:8080/v2/apps/%s/" %(app_id)
		response = requests.get(url)
		data = json.loads(response.text)
		if data['app']['deployments']:
			time.sleep(10)
			sys.stdout.write("\r%d%% Done" % int(i*10))
			sys.stdout.flush()
		else:
			sys.stdout.write("\r100% Done")
			break
	print "\n"
	if data['app']['deployments']:
		flag = False
	else:
		flag = True
	return flag

def deploy_service():

	headers = {
    'Content-Type': 'application/json',
	}
	data = open('app_config.json')
	try:
		response = requests.post('http://192.168.33.51:8080/v2/apps', headers=headers, data=data)
		print "deployed succesfully"
	except Exception as e:
		print e

def health_check():

	if_deployed = check_app_status(app_id)

	if not if_deployed:
		print "Your app %s is not deployed properly. Please check" %(app_id)
		undeploy_app(app_id)
		exit(1)

	node_details = []
	url = "http://192.168.33.51:8080/v2/apps/%s/tasks" %app_id
	response = requests.get(url)
	data = json.loads(response.text)
	j = 1
	for i in data['tasks']:
		if i['healthCheckResults'][0]['alive']:
			ip = port = None
			ip = str(i['host'])
			port = str(i['ports'][0])
			socket = "%s:%s" %(ip, port)
			node_details.append(socket)
		else:
			print "\nNode %s(%s) is unhealthy. Please check." %(j, socket)
			exit(1)
		j += 1
	print "All deployed nodes are healthy for your app - %s" %app_id
	return node_details

def deploy_nginx(node_details, app_id):

	file1 = open("/etc/nginx/sites-enabled/default", 'r')
	file2 = open("/home/vagrant/default", 'w')
	for i in file1.readlines():
		file2.write(i)
	file1.close()
	file2.close()
	file1 = open("nginx_template.conf", 'r')
	file2 = open("/etc/nginx/sites-enabled/default", 'w')
	for i in file1.readlines():
		if "<SERVER>" in i:
			for j in range(len(node_details)):
				i = "server %s; #%s%s" %(node_details[j], app_id, str(j))
				file2.write(i)
				file2.write("\n")
		else:
			file2.write(i)
	file2.close()

	a = os.system("nginx -t")
	if a:
		file1 = open("/home/vagrant/default", 'r')
		file2 = open("/etc/nginx/sites-enabled/default", 'w')
		for i in file1.readlines():
			file2.write(i)
		file1.close()
		file2.close()

		print "Error in nginx conf.. Reverting changes"
		undeploy_app(app_id)
		exit(1)	
	else:
		a = os.system("service nginx reload")
		if a:
			print "Errors while reloading nginx conf.. Please check.."
			exit(1)
		else:
			print "\nNginx conf reloaded successfully.."

			if "blue" in app_id:
				app_id = app_id.replace('blue', 'green')
			else:
				app_id = app_id.replace('green', 'blue')
			
			undeploy_app(app_id)

def undeploy_app(app_id):

	url = "http://192.168.33.51:8080/v2/apps/%s/" % app_id
	response = requests.get(url)
	data = json.loads(response.text)
	for i in range(len(data['app']['tasks'])):
		response = requests.delete(url)
	print "App %s undeployed successfully" %app_id

if __name__ == '__main__':
				
	if len(sys.argv) == 3:
		generate_configs(sys.argv[1], sys.argv[2])
		deploy_service()
		node_details = health_check()
		deploy_nginx(node_details, app_id)
	else:
		print "Usage: python deploy_mysite <sitename> <version>"
		exit(1)




