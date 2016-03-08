#!/usr/bin/python

import logging, requests, json, getpass

def t_logsetting(logfile, loglevel):

    logging.basicConfig(level=loglevel,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logfile,
                        filemode='a')

def t_log(logmessage):
    logging.info(logmessage)
    
def t_translateops(operation):
    "function to translate operation to operation type for View Job REST API"

    switcher = {
        "BUILD":"create",
        "DELETE":"delete",
        "SCALE":"scale",
        "STOP":"control",
        "START":"control",
        "RESTART":"control"
    }
    return switcher.get(operation,"undefined")

def t_exec(operation, iden_domain, l_method, l_rest_endpoint, cert_file, username, password, service_name, compute_shape, dbcs_def_file):

    url = l_rest_endpoint
    headers = { 
                  'X-ID-TENANT-NAME':iden_domain, 
                  'Content-Type':'application/json'
              }    
    
    if operation == 'VIEW':
        url = url + iden_domain + '/' + service_name
        try:
           response = requests.get(url, verify=cert_file, headers=headers, auth=(username,password))
        except Exception as e:
           t_log('An error occurred : %s\n' % e)
           raise
        if response.status_code == 200:
            parsed_response = json.loads(response.text)
            print 'Status of ' + parsed_response['service_name'] + ' - ' + parsed_response['status']
            print 'check logfile for detailed information ...'
            t_log(response.text)
            g_jobid = 0
        else :
            t_log('Job request not accepted - Response code %s' % response.status_code)
            g_jobid = 0
            
    elif operation == 'STOP':
          url = url + iden_domain + '/' + service_name
          data = {'lifecycleState':'Stop'}
          try:
             response = requests.post(url, verify=cert_file, headers=headers, auth=(username,password), data=json.dumps(data) )
          except Exception as e:
             t_log('An error occurred : %s\n' % e)
             raise
          if response.status_code == 202:
	         job_id = response.headers['Location'].split("/")
	         
	         t_log('Job Id : %s' % job_id[len(job_id)-1])
	         g_jobid = job_id[len(job_id)-1]
          else :
	         t_log('Job request not accepted - Response code %s' % response.status_code)
	         g_jobid = 0

    elif operation == 'START':
          url = url + iden_domain + '/' + service_name
          data = {'lifecycleState':'Start'}
          try:
             response = requests.post(url, verify=cert_file, headers=headers, auth=(username,password), data=json.dumps(data) )
          except Exception as e:
             t_log('An error occurred : %s\n' % e)
             raise
          if response.status_code == 202:
	         job_id = response.headers['Location'].split("/")
	         
	         t_log('Job Id : %s' % job_id[len(job_id)-1])
	         g_jobid = job_id[len(job_id)-1]
          else :
             t_log('Job request not accepted - Response code %s' % response.status_code)
             g_jobid = 0
             
    elif operation == 'RESTART':
          url = url + iden_domain + '/' + service_name
          data = {'lifecycleState':'Restart'}
          try:
             response = requests.post(url, verify=cert_file, headers=headers, auth=(username,password), data=json.dumps(data) )
          except Exception as e:
             t_log('An error occurred : %s\n' % e)
             raise
          if response.status_code == 202:
	         job_id = response.headers['Location'].split("/")
	         
	         t_log('Job Id : %s' % job_id[len(job_id)-1])
	         g_jobid = job_id[len(job_id)-1]
          else :
             t_log('Job request not accepted - Response code %s' % response.status_code)
             g_jobid = 0
             
    elif operation == 'SCALE':
          url = url + iden_domain + '/' + service_name
          data = {'shape':compute_shape}
          try:
             response = requests.put(url, verify=cert_file, headers=headers, auth=(username,password), data=json.dumps(data) )
          except Exception as e:
             t_log('An error occurred : %s\n' % e)
             raise
          if response.status_code == 202:
	         job_id = response.headers['Location'].split("/")
	         
	         t_log('Job Id : %s' % job_id[len(job_id)-1])
	         g_jobid = job_id[len(job_id)-1]
          else :
             t_log('Job request not accepted - Response code %s' % response.status_code)
             t_log(response.headers)
             g_jobid = 0

    elif operation == 'BUILD':
          url = url + iden_domain
          try:
             json_file =  open(dbcs_def_file,'r')
             json_str = json_file.read()
             json_data = json.loads(json_str)
          except Exception as e:
             t_log('An error occurred in processing dbcs json file: %s\n' % e)
          try:
             response = requests.post(url, verify=cert_file, headers=headers, auth=(username,password), data=json.dumps(json_data) )
          except Exception as e:
             t_log('An error occurred : %s\n' % e)
             raise
          if response.status_code == 202:
	         job_id = response.headers['Location'].split("/")
	         
	         t_log('Job Id : %s' % job_id[len(job_id)-1])
	         g_jobid = job_id[len(job_id)-1]
          else :
             t_log('Job request not accepted - Response code: %s' % response.status_code)
             t_log('Response Message: %s ' % response.text)
             g_jobid = 0

    elif operation == 'DELETE':
          url = url + iden_domain + '/' + service_name
          try:
             response = requests.delete(url, verify=cert_file, headers=headers, auth=(username,password))
          except Exception as e:
             t_log('An error occurred : %s\n' % e)
             raise
          if response.status_code == 202:
	         job_id = response.headers['Location'].split("/")
	         
	         t_log('Job Id : %s' % job_id[len(job_id)-1])
	         g_jobid = job_id[len(job_id)-1]
          else :
             t_log('Job request not accepted - Response code %s' % response.status_code)
             g_jobid = 0

    return g_jobid
     
def t_viewjob (operation, iden_domain, l_rest_endpoint, cert_file, username, password, jobid):
    "function to return status of a job "
    
    url = l_rest_endpoint + iden_domain + '/status/' + t_translateops(operation) + '/job/' + str(jobid)
    #print 'view job url', url

    headers = { 
                  'X-ID-TENANT-NAME':iden_domain, 
              }    
              
    try:
       response = requests.get(url, verify=cert_file, headers=headers, auth=(username,password))
    except Exception as e:
       t_log('An error occurred in view job status: %s\n' % e)
       raise
    try:
       parsed_response = json.loads(response.text)
       t_log('Job Opeartion ' + parsed_response['job_operation'])
       t_log('Job Status ' + parsed_response['job_status'])
       t_log(parsed_response['message'])
    except ValueError as e:
       t_log('Malformed Json file')
       parsed_response = {}
    return parsed_response

if __name__ == "__main__":

    l_logfile='/tmp/pythontest.log'
    l_loglevel=logging.INFO
    
    t_logsetting(l_logfile, l_loglevel)
    
    t_log('A DEBUG MESSAGE')
    t_log('An Error Message')
    t_log('A Warning  Message')
    #t_exec('VIEW','DomainName','GET','https://dbaas.oraclecloud.com/paas/service/dbcs/api/v1.1/instances/','/Users/bipul/keys/cacert.pem','uname','password','Service_name')
    '''
    print 'BUILD', t_translateops('BUILD')
    print 'DELETE',t_translateops('DELETE')
    print 'SCALE_UP',t_translateops('SCALE_UP')
    print 'SCALE_DOWN',t_translateops('SCALE_DOWN')
    print 'RESTART',t_translateops('RESTART')
    print 'START',t_translateops('START')
    print 'STOP',t_translateops('STOP')
    print 'UNKNOWN',t_translateops('UNKNOWN')
    '''
    #password = getpass.getpass('Identity Domain Password:')
    #jobid = raw_input('Job Id :')
    #parsed_response = t_viewjob('START','domain name','https://dbaas.oraclecloud.com/paas/service/dbcs/api/v1.1/instances/','/Users/bipul/keys/cacert.pem','username',password,jobid)
    #print json.dumps(parsed_response, indent=4, sort_keys=True)
