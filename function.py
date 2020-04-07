from __future__ import print_function

import csv
import json
import sys
import time
from datetime import date
from venv import logger

import boto3
import botocore
import pymysql
import os

VERBOSE = 1
SLEEP = 2

client = boto3.client('cloudformation')
rds = boto3.client('rds')
template = "database.template"
parameters = "database-parameters.json"
stack_name = "air-quality-data-stack"
dataset_name = "air-quality-data-set"
file_location = 'data-set/'
rds_user_name = "admin"
rds_password = "myname18"
db_name = "airqualitydatabase"

imports = [
  "const express = require('express');",
  "const cors = require('cors');",
  "const bodyParser = require('body-parser');",
  "const mysql = require('mysql');",
  "const events = require('./events');"
]


def update_stack(params):
  print('Updating {}'.format(stack_name))
  response = client.update_stack(**params)
  waiter = client.get_waiter('stack_update_complete')
  print("...waiting for stack to be ready...")
  waiter.wait(StackName=stack_name)
  return response['ResponseMetadata']['HTTPStatusCode']


def create_stack(params):
  print('Creating {}'.format(stack_name))
  response = client.create_stack(**params)
  waiter = client.get_waiter('stack_create_complete')
  print("...waiting for stack to be ready...")
  waiter.wait(StackName=stack_name)
  return response['ResponseMetadata']['HTTPStatusCode']


def delete_stack(stack_name):
  print('Deleting {}'.format(stack_name))
  response = client.delete_stack(
    StackName=stack_name
  )
  waiter = client.get_waiter('stack_delete_complete')
  print("...waiting for stack to be deleted...")
  waiter.wait(StackName=stack_name)
  return response['ResponseMetadata']['HTTPStatusCode']


def parse_template(template):
  with open(template) as template_fileobj:
    template_data = template_fileobj.read()
  client.validate_template(TemplateBody=template_data)
  return template_data


def parse_parameters(parameters):
  with open(parameters) as parameter_fileobj:
    parameter_data = json.load(parameter_fileobj)
  return parameter_data


# Method to create a RDS instance
def get_database_url():
  response = rds.describe_db_instances(
    DBInstanceIdentifier=db_name + "instance"
  )
  return response['DBInstances'][0]['Endpoint']['Address']


def create_database():
  template_data = parse_template(template)
  parameter_data = parse_parameters(parameters)

  params = {
    'StackName': stack_name,
    'TemplateBody': template_data,
    'Parameters': parameter_data,
    'Capabilities': ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
    'Tags': [
      {
        "Key": "Purpose",
        "Value": "Data Storage"
      },
      {
        "Key": "Date",
        "Value": str(date.today())
      }
    ]
  }
  try:
    if stack_exists(stack_name):
      response = update_stack(params)
      waiter = client.get_waiter('stack_update_complete')
      if (VERBOSE == 1):
        if response == 200:
          print('Stack update: SUCCESSFULL')
        else:
          print(f'Stack update: FAILED', response)
    else:
      response = create_stack(params)
      if (VERBOSE == 1):
        if response == 200:
          print('Stack create: SUCCESSFULL')
        else:
          print(f'Stack create: FAILED', response)
  except botocore.exceptions.ClientError as ex:
    error_message = ex.response['Error']['Message']
    if error_message == 'No updates are to be performed.':
      print("No changes")
    else:
      raise


def delete_database():
  time.sleep(SLEEP)
  try:
    if stack_exists(stack_name):
      response = delete_stack(stack_name)
      if (VERBOSE == 1):
        if response == 200:
          print('Stack deleted: SUCCESSFULLY')
        else:
          print(f'Stack deleted: FAILED', response)
    else:
      print('Stack does not exist: {}'.format(stack_name))
  except botocore.exceptions.ClientError as ex:
    error_message = ex.response['Error']['Message']
    print(error_message)


def stack_exists(stack_name):
  stacks = client.list_stacks()['StackSummaries']
  for stack in stacks:
    if stack['StackStatus'] == 'DELETE_COMPLETE':
      continue
    if stack_name == stack['StackName']:
      return True
  return False


# Method to process the CSV file
def process_data(file):
  with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    entries = []
    for row in csv_reader:
      entry = {}
      if line_count == 0:
        line_count += 1
      else:
        entry["Date"] = row[0]
        entry["Time"] = row[1]
        entry["CO(GT)"] = row[2]
        entry["PT08.S1(CO)"] = row[3]
        entry["NMHC(GT)"] = row[4]
        entry["C6H6(GT)"] = row[5]
        entry["PT08.S2(NMHC)"] = row[6]
        entry["NOx(GT)"] = row[7]
        entry["PT08.S3(NOx)"] = row[8]
        entry["NO2(GT)"] = row[9]
        entry["PT08.S4(NO2)"] = row[10]
        entry["PT08.S5(O3)"] = row[11]
        entry["T"] = row[12]
        entry["RH"] = row[13]
        entry["AH"] = row[14]
        entries.append(entry)
        line_count += 1

    print(f'Processed {line_count} lines.')
    # Remove corrupt data
    entries = clean_data(entries)
    return entries


def create_table(url):
  try:
    conn = pymysql.connect(url, user=rds_user_name, passwd=rds_password, db=db_name, connect_timeout=5)
    cursor = conn.cursor()
    cursor.execute(
      "create table airquality (id int auto_increment primary key, date varchar(255) not null, time varchar(255) not null, co varchar(255) not null, tin_oxide varchar(255) not null, metanic_hydro varchar(255) not null, benzene_conc varchar(255) not null, titania varchar(255) not null, nox varchar(255) not null, tungsten_oxide_nox varchar(255) not null, average_no2 varchar(255) not null, tungsten_oxide_no2 varchar(255) not null, indium_oxide varchar(255) not null, temp varchar(255) not null, relative_humidity varchar(255) not null, absolute_humidity varchar(255) not null);")
    conn.commit()
  except Exception as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    logger.error(e)
    sys.exit()


logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


# Method to insert the data into the database
def insert_data(data, url):
  try:
    conn = pymysql.connect(url,
                           user=rds_user_name, passwd=rds_password, db=db_name, connect_timeout=5)
    rows = []
    for entry in data:
      row = ()
      values = []
      for attribute, value in entry.items():
        values.append(value)
      row = tuple(values)
      rows.append(row)

    cursor = conn.cursor()

    query = "INSERT INTO airquality (date, time,co, tin_oxide, metanic_hydro, benzene_conc, titania, nox," \
            "tungsten_oxide_nox,average_no2, tungsten_oxide_no2, indium_oxide, temp, relative_humidity," \
            "absolute_humidity) VALUES " + ",".join(
      "(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)" for _ in rows)
    flattened_values = [item for sublist in rows for item in sublist]
    cursor.execute(query, flattened_values)

    conn.commit()
  except Exception as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    logger.error(e)
    sys.exit()

  logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def clean_data(entries):
  clean_entries = []
  for entry in entries:
    valid_data = True
    for attribute, value in entry.items():
      if value == "":
        valid_data = False
        break
    if valid_data:
      clean_entries.append(entry)
  return clean_entries


def line_prepender(filename, line):
  with open(filename, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(line.rstrip('\r\n') + '\n' + content)


def main():
  # 1. Create RDS database
  create_database()
  print("Database created...")
  url = get_database_url()
  print("Database url:" + url)
  statement = "const connection = mysql.createConnection({host:'" + url + "',user:'" + rds_user_name + "',password:'" + rds_password + "',database:'" + db_name + "'});"
  imports.insert(0,statement)
  for line in imports:
    line_prepender("app/src/index.js", line)
  # 2. Process data from CSV files
  entries = process_data(file_location + "AirQualityUCI.csv")
  print("The corrupt data has been removed. There is now {} entries".format(len(entries)))
  # 3. Insert the data into the database
  # create_table(url)
  # insert_data(entries, url)
  # 4. Run the Express server
  os.system("node app/src/index.js")


if __name__ == '__main__':
  main()
