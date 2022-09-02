import cx_Oracle
import oci
import time
import sys
from base64 import b64decode

# Function to get secrets from vault
def get_sec(secret_id):
  ociConfigFilePath = "/root/.oci/config"
  ociProfileName = "DEFAULT"
  config = oci.config.from_file(ociConfigFilePath, ociProfileName)
  secrets_client = oci.secrets.SecretsClient(config)
  get_secret_response = secrets_client.get_secret_bundle(secret_id)
  
  # Get the data from response
  
  value = b64decode(get_secret_response.data.secret_bundle_content.content.encode()).decode()
  #print("{}".format(value))
  
  return value


### Database Connection Block ###
username='SYSTEM'
#Provide Secret OCID
sec_id='ocid1.vaultsecret.oc1.phx.amaaaaaaytsgwayaa7j6zaut2uqaxajpvzh6y4vas3jolz2owj42beu6hhga'
passwd= get_sec(sec_id)
dsn_name="""madb.sub04050841080.gomvcn.oraclevcn.com:1521/MDB_PHX.sub04050841080.gomvcn.oraclevcn.com"""
encoding_name="UTF-8"

connection = cx_Oracle.connect(user=username,password=passwd,dsn=dsn_name,encoding=encoding_name)
cur = connection.cursor()
cur.execute("select sysdate from dual")
res = cur.fetchall()
for row in res:
    print(row)
cur.close()
