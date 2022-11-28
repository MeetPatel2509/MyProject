#Getting Data From Github to Local
from git import *
from jproperties import Properties

config = Properties()
with open('/home/patel/airflow/dags/DemoCovidProject/codeconfig.properties', 'rb') as config_file:
    config.load(config_file)
    

def cloneData():
    try:
        Repo.clone_from(config.get("GitRepoPathUrl")[0], config.get("GitRepoPath")[0]+'/')
        print("Data Downloaded into Local")
    except:
        repo = Repo(config.get("GitRepoPath")[0])
        repo.remotes.origin.pull()
        print("Data has been updated in Local")