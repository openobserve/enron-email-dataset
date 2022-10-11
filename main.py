from os import listdir
from os.path import isfile, join

import base64
import json
import requests

# List all folders and files
def list_all(folder_name):
    folder_list = []
    for f in listdir(folder_name):
        folder_list.append(f)

    return folder_list

# List all files
def list_files(folder_name):
    return [f for f in listdir(join(folder_name)) if isfile(join(folder_name, f))]


def parse_data(data_lines):
    data = {
        "To": None,
        "From": None,
        "Subject": None,
        "Body": ""
    }
    for line in data_lines:
        #  print(line)
        if line.find("Message-ID:", 0) == 0:
            data['Message-ID'] = line[9:len(line)]
        elif line.find("Date:", 0) == 0:
            data['Date'] = line[9:len(line)]
        elif line.find("From:", 0) == 0:
            data['From'] = line[6:len(line)]
        elif line.find("To:", 0) == 0:
            data['To'] = line[4:len(line)]
        elif line.find("Subject:", 0) == 0:
            data['Subject'] = line[9:len(line)]
        elif line.find("Cc:", 0) == 0:
            data['Cc'] = line[9:len(line)]
        elif line.find("Mime-Version:", 0) == 0:
            data['Mime-Version'] = line[9:len(line)]
        elif line.find("Content-Type:", 0) == 0:
            data['Content-Type'] = line[9:len(line)]
        elif line.find("Content-Transfer-Encoding:", 0) == 0:
            data['Content-Transfer-Encoding'] = line[9:len(line)]
        elif line.find("X-From:", 0) == 0:
            data['X-From'] = line[9:len(line)]
        elif line.find("X-To:", 0) == 0:
            data['X-To'] = line[9:len(line)]
        elif line.find("X-cc:", 0) == 0:
            data['X-cc'] = line[9:len(line)]
        elif line.find("X-bcc:", 0) == 0:
            data['X-bcc'] = line[9:len(line)]
        elif line.find("X-Folder:", 0) == 0:
            data['X-Folder'] = line[9:len(line)]
        elif line.find("X-Origin:", 0) == 0:
            data['X-Origin'] = line[9:len(line)]
        elif line.find("X-FileName:", 0) == 0:
            data['X-FileName'] = line[9:len(line)]
        else:
            data['Body'] = data['Body'] + line

    return data


def index_data(data):
    user = "admin"
    password = "Complexpass#123"
    bas64encoded_creds = base64.b64encode(
        bytes(user + ":" + password, "utf-8")).decode("utf-8")

    headers = {"Content-type": "application/json",
               "Authorization": "Basic " + bas64encoded_creds}

    index = "enron1"
    zinc_host = "https://playground.dev.zincsearch.com"
    zinc_url = zinc_host + "/api/" + index + "/_doc"

    res = requests.put(zinc_url, headers=headers, data=json.dumps(data))


def main():
    user_list = list_all("./maildir")

    for user in user_list:
        folders = list_all("./maildir/" + user)
        for folder in folders:
          mail_files = list_files(
              "./maildir/" + user + "/" + folder + "/")
          for mail_file in mail_files:
              print("Indexing : ", user + "/" + folder + "/" + mail_file)
              sys_file = open("./maildir/" + user + "/" +
                              folder + "/" + mail_file, 'r')
              lines = sys_file.readlines()

              index_data(parse_data(lines))


if __name__ == "__main__":
    main()
