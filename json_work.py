
import os
import sys

import json

student_string = '''
{
  "students" : [
   {
    "roll_number" : "S00001",
	"name" : "Test Student1",
	"age" : 22,
	"gender" : "Male"
   },
   {
    "roll_number" : "S00002",
	"name" : "Test Student2",
	"age" : 24,
	"gender" : "Female"
   },
   {
    "roll_number" : "S00003",
	"name" : "Test Student3",
	"age" : 22,
	"gender" : "Male"
   },
   {
    "roll_number" : "S00004",
	"name" : "Test Student4",
	"age" : 19,
	"gender" : "Female"
   }
  ]
}
'''

def training():
	data = json.loads(student_string)
	#print(type(data))
	
	for student in data['students']:
		del student['gender']
		
	new_student_string = json.dumps(data, indent=2, sort_keys=True)
	print(new_student_string)
	
def training_file(file):
    
	with open(file, 'r') as f:
		data = json.load(f)
	
	f.close()
	print(type(data))
	print(type(data['students']))
	print(type(data['students'][0]))
	print(type(data['students'][0]['name']))
	
	for student in data['students']:
		print(student['name'] + ' - ' + student['roll_number'])
		del student['gender']
		
	with open('new_student_temp_data.txt', 'w') as f:
		json.dump(data, f, indent=2, sort_keys=True)
	f.close()
	
def read_file_as_json(file):
	#: read the data from a file.
	with open(file, 'r') as f:
		data = json.load(f)
	f.close()
	
	return data
	
def write_json_to_file(data, file):
	#: write the currently changed data into the file.
	with open(file, 'w') as f:
		json.dump(data, f, indent=2, sort_keys=True)
	f.close()
	
	
def add_student(file, target_file):
	#: read the data
	data = read_file_as_json(file)
		
	#: create a student data as dictionary
	name = 'New Student'
	roll_number = 'S00005'
	age = 19
	gender = 'Male'
	
	dict_student_obj = {
	                     'roll_number' : roll_number,
						 'name' : name,
						 'age' : age,
						 'gender' : gender
					   }
	
	#: append the student dictionary object to data['students']
	data['students'].append(dict_student_obj)
	
#	print(data)
	
	#: write the currently changed data into the file.
	write_json_to_file(data, target_file)


'''
	Edit/Update the student information.
'''
def update_student_detail(file, target_file, _id=''):
	#: read the data
	data = read_file_as_json(file)
	
	# fetch details for the student to be updated.
	if _id == '':
		roll_number = 'S00005'
	else: 
	    roll_number = _id
	
	# data initialized
	name = ''
	age = 0
	gender = ''
	
	# data to be edit/update
	name = 'John Doe'
	gender = 'Male'
	age =  30
	
	for student in data['students']:
		#: Can fetch student from roll number field.
		#: Roll Number is NOT allowed to change.
		if student['roll_number'] == roll_number:
			# update/edit the name for student.			
			if name != '':
				student['name'] = name
			# update/edit the age for student
			if age != 0:
				student['age'] = age
			# update/edit the gender information for student.	
			if gender != '':
				student['gender'] = gender
	#: print(data) - help in catastrophe
	
	#: write the currently changed data into the file.
	write_json_to_file(data, target_file)

'''
	Delete a particular student from database.
'''
def delete_student_from_data(file, target_file, _id=''):
	#: read the data
	data = read_file_as_json(file)
	
	# fetch details for the student to be updated.
	if _id == '':
		roll_number = 'S00005'
	else:
		roll_number = _id
	
	for student in data['students']:
		#: Can fetch student from roll number field.
		#: Roll Number is NOT allowed to change.
		if student['roll_number'] == roll_number:
			#: delete the student from database list.
			data['students'].remove(student)
	
	#: write the currently changed data into the file.
	write_json_to_file(data, target_file)

def search_student_from_data(file, target_search_string=''):
	
	list_of_matched_student = []
	
	if target_search_string == '':
		print('Nothing specified for search...')
	else:
		# get all students in the database.
		list_of_students = list_all_students(file)
		
		#: loop on the string to find the student.
		for student in list_of_students:
			
			if student['roll_number'] == target_search_string:
				list_of_matched_student.append(student)
			
			if student['name'] == target_search_string:
				list_of_matched_student.append(student)
				
	return list_of_matched_student
	
def list_all_students(file):
	#: read the data
	data = read_file_as_json(file)
	
	#: create a list for the fetched students.
	list_of_all_students = data['students']
		
	#: return the list of the students in the database
	return list_of_all_students
	
def display_student_list(list):
	for item in list:
		print('''
			Name : {}
			Roll Number : {}
			Age : {}
			Gender : {}
		'''.format(item['name'], item['roll_number'], item['age'], item['gender']), end='\n') 
	
def main():
	#training()
	
	file = 'student_temp_data.txt'
	target_file = 'new_student_temp_data.txt'
	#training_file(file)
	
	#: list all the student data.
	#list = list_all_students(target_file)
	
	target_search_string = input('Enter Student to search : ')
	list = search_student_from_data(target_file, target_search_string)
	
	# Display all fetched data.
	display_student_list(list)
	
	#add_student(file, target_file)
	#update_student_detail(target_file, target_file)
	#delete_student_from_data(target_file, target_file)
	
	pass


if __name__=='__main__':
	main()

