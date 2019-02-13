import os
#: re for regex functionality, used in search.
import re
#: file data will be read through json format for read write operation
import json
#: provide security option's like password hashing.
from werkzeug.security import check_password_hash, generate_password_hash

'''
Created by : Ajay Singh Parmar
Date : Febuary 12, 2019
Description : Containes all the database functinality for user authentication.
-Thus module is written to simulate the behavior of any database query language
-The methods present her are exported to other directories in project.
Process flow -
Read the file -
-count = 0
-if present :
-count how many records -> count will be used for id
else if not present -
-count = 1
-open file in write mode and append the id and admin and password
'''


#: read operation on file
def read_file_as_json(file):
    #: open in read and fetch data from file.
    with open(file, 'r') as f:
        #: load data to the file.
        data = json.load(f)
    f.close()  #: close the file.
    return data


#: write operation on file
def write_json_to_file(data, file):
    #: open file in write mode.
    with open(file, 'w') as f:
        #: dump data into the file.
        json.dump(data, f, indent=2, sort_keys=True)
        f.close()  #: close the file.


#: count total users in database, used to generate roll number.
def get_last_id(data):
    #: set counter to 0.
    counter = 0
    #: get the last user from list of students.
    last_user = data['users'][-1]
    #: return the last user for the partcular id
    return last_user['id']


#: to delete a particular user from database.
def delete_user(file, _id=1):
    #: read data
    data = read_file_as_json(file)
    #: iterate through the users list
    for user in data['users']:
        #: fetch user for provided id.
        if user['id'] == _id:
            #: delete user from database.
            data['users'].remove(user)
    #: write updated data back to file.
    write_json_to_file(data, file)


#: to add user to user database.
def add_user(file, username, password):
    #: read data
    data = read_file_as_json(file)
    #: get last user's id
    last_id = int(get_last_id(data))
    #: generate new id for the user entered.
    _id = last_id + 1
    #: create the dict object for user.
    dict_user_obj = {
        'id': _id,
        'username': username,
        'password': password
        }
    #: add user dict obj to user list.
    data['users'].append(dict_user_obj)
    #: write modified data back to file.
    write_json_to_file(data, file)


#: to get list of users in database.
def list_all_users(file):
    #: read data
    data = read_file_as_json(file)
    #: create a list for the fetched users.
    all_users = data['users']
    #: return all users
    return all_users


#: to display users as provied in list form.
def display_user_list(list):
    #: if list provided is empty then display appropriate error message.
    if list == []:
        #: display no record error
        print('Sorry :( No record match found...')
    else:
        #: otherwise for each item in list display details in specific format.
        for item in list:
            print('''
                id : {}
                Username : {}
                Password : {}
            '''.format(
                item['id'],
                item['username'],
                item['password']), end='\n')


#: copy master data file to working file on initialization.
def copy_master_data_to_file(master, file):
    #: fetch masterdata from the master data file.
    master_data = read_file_as_json(master)
    #: write master data into working file.
    write_json_to_file(master_data, file)


#: load data into working temp directory on initialization of database.
def load_data_user(file, target):
    #: try to open the working data file if exist.
    try:
        #: open file in read mode.
        f = open(target, 'r')
        #: close file.
        f.close()
    except FileNotFoundError:
        #: if file do not exist then create the file and copy master data.
        copy_master_data_to_file(file, target)
    pass


#: list all users in working file.
def user_list(file):
    #: return list of users
    return list_all_users(file)


#: authentication for user login credentials.
def login_authenticator(file, username='', password=''):
    #: read data
    data = read_file_as_json(file)
    login_flag = False  #: set indicator for login
    #: search the username for any user in database.
    for user in data['users']:
        #: check the username match
        #: admin is exempted from password hash check.
        #: As admin's password is not hash it's initialized, work in progress.
        if user['username'] == username and user['username'] != 'admin':
            #: check for hashed user's password with entered hash password.
            if check_password_hash(user['password'], password):
                #: on match login success flag will be indicated.
                login_flag = True
                print('login success.')  #: display success message.
                break  #: break the search.
        else:
            #: else is for admin username and password check.
            #: temprory logic for admin credentials.
            #: this will be removed once we fix password hash issue for admin.
            if user['username'] == username:
                if user['password'] == password:
                    login_flag = True
                    print('login success.')
                    break
    #: return login indicator.
    return login_flag
