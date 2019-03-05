#!/usr/bin/python

import boto
from boto.s3.key import Key
keyId = "AKIAJ2AQECBGGFU7DJRQ"
sKeyId= "rrlHf8yKe2A8wWF720CLySSiGbeQ79rMXdLKvm/2"
fileName="mysqldump.sh"
bucketName="joseph-devopsdairy1"
file = open(fileName)
conn = boto.connect_s3(keyId,sKeyId)
bucket = conn.get_bucket(bucketName)
#Get the Key object of the bucket
k = Key(bucket)
#Crete a new key with id as the name of the file
k.key=fileName
#Upload the file
result = k.set_contents_from_file(file)
#result contains the size of the file uploaded
