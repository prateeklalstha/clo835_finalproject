from cloudpathlib import CloudPath
import os
import mysql.connector
import socket
from flask import Flask
from flask import render_template
import logging
import boto3
from urllib.parse import urlparse
logging.basicConfig(filename='record.log', level=logging.DEBUG)


app = Flask(__name__)

DB_Host = os.environ.get('MYSQL_SERVICE_HOST') or "localhost"
DB_Database = os.environ.get('DB_Database') or "mysql"
DB_User = os.environ.get('DB_User') or "root"
DB_Password = os.environ.get('DB_Password') or "paswrd"
IMAGE_URL = os.environ.get('IMAGE_URL') or "static"
USER_NAME = os.environ.get('USER_NAME') or ""
print(IMAGE_URL)

def downloadFile():
    try:
        app.logger.info(IMAGE_URL)
        if IMAGE_URL != 'static':
            # cp = CloudPath(IMAGE_URL)
            # cp.download_to('./static')
            parsed_url = urlparse(IMAGE_URL)
            bucket_name = parsed_url.netloc
            object_key = parsed_url.path.lstrip('/')
            
            # Initialize the S3 client
            s3_client = boto3.client('s3')
            
            # Download the file from S3
            s3_client.download_file(bucket_name, object_key, './static/project.jpeg')
            # s3.download_file(IMAGE_URL, './static/')
    except Exception as e:
        err_message = str(e)
        app.logger.warning(err_message)
        print(err_message)

downloadFile()

@app.route("/")
def main():
    db_connect_result = False
    err_message = ""
    app.logger.info("calling download")
    try:
        mysql.connector.connect(
            host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        color = '#39b54b'
        db_connect_result = True
    except Exception as e:
        color = '#ff3f3f'
        err_message = str(e)

    return render_template('home.html', debug="Environment Variables: DB_Host=" + (os.environ.get('MYSQL_SERVICE_HOST') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database') or "Not Set") + "; DB_User=" + (os.environ.get('DB_User') or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password') or "Not Set") + "; " + err_message, db_connect_result=db_connect_result, name=socket.gethostname(), color=color, image_url=IMAGE_URL, user_name=USER_NAME)


@app.route("/debug")
def debug():
    color = '#2196f3'
    return render_template('home.html', debug="Environment Variables: DB_Host=" + (os.environ.get('MYSQL_SERVICE_HOST') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database') or "Not Set") + "; DB_User=" + (os.environ.get('DB_User') or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password') or "Not Set"), color=color, image_url=IMAGE_URL, user_name=USER_NAME)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)