import pysnow
import requests
import logging
from logs.logs import createLogFile
import datetime
from config import ConfigVariable
import sys
##############################################################################################
####                                                                                      ####
####                                  For Error logging                                   ####
####                                                                                      ####
##############################################################################################
log_file_path = createLogFile(ConfigVariable.log_folder_path)
flog_fname = datetime.datetime.now().strftime('%b_%Y.txt')
logging.basicConfig(level=logging.INFO, filename=log_file_path.name, filemode="a", format="%(asctime)s %(levelname)s %(message)s")


##############################################################################################
####                                                                                      ####
####                 For ServiceNow Instance Connection                                   ####
####                                                                                      ####
##############################################################################################

myinstance = ConfigVariable.myinstance
username = ConfigVariable.username
password = ConfigVariable.password
c = pysnow.Client(instance=myinstance, user=username, password=password)
incident = c.resource(api_path='/table/incident')
    

#########################################################################################################
####                                                                                                  ####
####             For Fecting Incidents Data FROM ServiceNow REST API                                  ####
####                                                                                                  ####
##########################################################################################################
def fetchIncidetn(incident, username, password):
     query_open_inc = 'state=1^assignment_group=a35ce7dd97fa4210f245b12de053af29'\
          '^ORassignment_group=8a4dde73c6112278017a6a4baf547aa7'\
          '^ORassignment_group=36c741fa731313005754660c4cf6a70d'\
          '^ORassignment_group=d625dccec0a8016700a222a0f7900d06'\
          '^ORassignment_group=0a52d3dcd7011200f2d224837e6103f2'\
          '^ORassignment_group=287ebd7da9fe198100f92cc8d1d2154e'
     
     response = incident.get(query=query_open_inc, stream=True)
     json_response= response._response.json()
     if len(json_response['result']) == 0:
          sys.exit(logging.info(f"Open Incidents are empty from selected groups"))
     for records in json_response['result']:
          sys_id = records['sys_id']
          get_assign_group_url = records['assignment_group']['link']
          get_assign_groups = requests.get(get_assign_group_url, auth=(username, password))
          try:
               get_assign_groups.status_code == 404
          except:
           logging.info(f"No records, {sys_id}")
               
          response_json = get_assign_groups.json()
          get_assign_group_name = response_json['result'].get('name')       
          print('INC Number: '+records['number'], ', Assignment_group: '+get_assign_group_name)
          logging.info(f"INC Number: {records['number']}, Assignment_group: {get_assign_group_name}")
     
          #Assigning Open Incidents 
          if get_assign_group_name == 'GIS':
               update = {"state":2, 'short_description':'Auto Assignment', 'assigned_to':'beth.anglin@example.com'}
               incident.update(query={'number':records['number']}, payload=update)
               logging.info(f"Auto assigned Updates: INC Number: {records['number']}, Assigned group: {get_assign_group_name}, assigned_to:beth.anglin@example.com")
          elif get_assign_group_name == 'Software':
               update = {'state':2, 'assigned_to':'don.goodliffe@example.com'}
               incident.update(query={'number':records['number']}, payload=update)
               logging.info(f"Auto assigned Updates: INC Number: {records['number']}, Assigned group: {get_assign_group_name}, assigned_to:beth.anglin@example.com")
          elif get_assign_group_name == 'Network':
               update = {'state':2, 'assigned_to':'itil@example.com', 'work_notes':'Auto assigned, and work in progress'}
               incident.update(query={'number':records['number']}, payload=update)
               logging.info(f"Auto assigned Updates: INC Number: {records['number']}, Assigned group: {get_assign_group_name}, assigned_to:beth.anglin@example.com")
          elif get_assign_group_name == "Openspace":
               update = {'state':2, 'work_notes': 'Auto assigned, and work in progress','assigned_to':'beth.anglin@example.com'}
               incident.update(query={'number':records['number']}, payload=update)
               logging.info(f"Auto assigned Updates: INC Number: {records['number']}, Assigned group: {get_assign_group_name}, assigned_to:beth.anglin@example.com")
     return {"status":"Successfull"}


def main():
     fetchIncidetn(incident, username, password)
if __name__ == "__main__":
     main()