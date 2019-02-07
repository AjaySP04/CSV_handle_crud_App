import os
import csv
import sys
import pickle

from dateutil import parser
from datetime import date, time, datetime, timedelta

#student data holder
MASTER_STUDENT_LIST = list()

#main method for working
def main():
	login()

# will create a student class that will instantiate the object and hold record.
class Student():
	id_counter = 0
	def __init__(self, fname, lname, dob, address, postcode, gender, email):
		Student.id_counter = Student.id_counter + 1
		self.rollno = Student.id_counter
		self.fname = fname 
		self.lname = lname
		self.dob = dob
		self.address = address
		self.postcode = postcode
		self.gender = gender
		self.email = email
		
	def get_age(self):
		today = date.today()
		birth_date = parser.parse(self.dob)
		return today.year - birth_date.year - ((today.month, today.day) < ( birth_date.month, birth_date.day))
		
	def __str__(self):
		return ("{} - {} {} - {} ".format(self.rollno, self.fname, self.lname, self.email))
		
	@classmethod
	def get_total_number_of_student():
		return Student.id_counter
	
	
	
#login method
def login():
	username = 'tutor'
	password = 'password'
	
	print('Enter Username : ')
	user = str(input())
	
	print('Enter Password : ')
	pwd = str(input())
	
	if (user == username and pwd == password):
		print('Welcome {} - Access granted.'.format(user))
		menu()
	else:
		print((25 * '*' ) + ' Bad Username or Password. Access Denied!' + (25 * '*'))
		print(50 * '*' )
		sys.exit()

#menu method
def menu():
	print((25 * '-') + ' Menu ' + (25 * '-') + '\n')
	#time.sleep(1)
	
	print()
	choice = input('''
		A : Enter Student Details
		B : View Student Details
		C : Search by ID number
		D : Produce Reports
		Q : Quit/Log Out
		
		Please Enter your Choice: ''')
	
	if choice == 'A' or choice == 'a':
		enter_student_details()
	elif choice == 'B' or choice == 'b':
		view_student_details()
	elif choice == 'C' or choice == 'c':
		search_by_id()
	elif choice == 'D' or choice == 'd':
		produce_reports()
	elif choice == 'Q' or choice == 'q':
		sys.exit()
	else:
		print('Must choose only valid options.')
		print('Please Try Again')
		menu()
		
def enter_student_details():
	
	print((30*'-') + ' Student Data Form ' + (30*'-'))
	# take user input for details that needed to be stored in file data
	rollno = int(input('Enter RollNo : '))
	fname = str(input('Enter First name : '))
	lname = str(input('Enter Last name : '))
	
	# enter dob of the student in specified format of %d/%m/%Y
	while (True):
		dob = str(input('Enter Date Of Birth : '))
		try:
			dob = datetime.strptime(dob, "%d/%m/%Y")
			break
		except ValueError as e:
			print('Error : Must be of format dd/mm/yyyy.')
			user_key = input('press 1 to try again or 0 to exit application.')
			if user_key == 0:
				sys.exit()
				
	address = str(input('Enter first line of address: '))
	postcode = str(input('Enter Pincode : '))
	gender = str(input('Enter Gender (M or F) : '))
	email = str(input('Enter Email ID : '))
	
	with open('student_data_file.txt', 'a') as student_data_file:
		studentFileWriter = csv.writer(student_data_file)
		studentFileWriter.writerow([rollno, fname, lname, dob, address, postcode, gender, email])
		print('**** Student Record is written, Successfully! ****')
		student_data_file.close()
		menu()
	
	
	
def view_student_details():
	# open file to read for the data records
	student_file = open('student_data_file.txt', 'r', encoding='utf-8')
	
	#create a list called 'student_data_display_list'
	student_data_display_list = student_file.read()
	
	#print all the record present in the database
	print((25*'-') + 'Student Database Records' + (25*'-') )
	print(student_data_display_list)
	student_file.close()
	menu()
	
def search_by_id():
	 #Teacher can input an ID number and display the relevant student's details
	#open the file as student_file (varibale)
	with open('student_data_file.txt', 'r', encoding='utf-8') as student_file:
		#prompt user to enter id to search 
		id_number = input('Enter ID number you require : ')
		print((25 * '-') + ' Search Result ' + (25 * '-'))
		
		#call upon our reader (this allow us to work with our file)
		studentFileReader = csv.reader(student_file)
		
		# for each row this is read by the reader
		for row in studentFileReader:
			#add for each field in that row (this is automatically for us)
			for field in row:
				#if field is equal to the id number that is being searched for
				if field == id_number:
					#print the row corresponding to search
					print(row)
					student = Student(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
					print('Student Searched : \n', student)
					print('Age Of {} : {} years '.format(student.fname, student.get_age()))
					#return to main menu for futher processing of program
		print(100 * '-')
		menu()
	
	
def produce_reports():
	 #Teacher can produce clever reports such as:
    #a) list of names of males and email addresses (to email a reminder about boys football club)
    #b) list of names of females in specific postcode (to remind them of a girls coding club in the area)
    #c) list of all names, birthdays and addresses (to send out birthday cards!)
	print((25 * '-') + ' Produce Reports ' + (25 * '-'))
	#time.sleep(1)
	print()
	choice = input('''
		A : View all Student details    *For General use
		B : List of Males and Emails    *For Footbal club trials
		C : List Females and Emails     *For Female Clubs
		D : Search by D.O.B and Address *For Birthday Cards
		Q : Return to Main Menu
		Please Enter Choice : ''')
		
	if choice == 'A' or choice == 'a':
		view_students()
	elif choice == 'B' or choice == 'b':
		males_emails()
	elif choice == 'C' or choice == 'c':
		females_emails()
	elif choice == 'D' or choice == 'd':
		dob_address()
	elif choice == 'Q' or choice == 'q':
		#return to main menu
		menu()
	else:
		#error checking - if they put in nonsense , make sure they know what to do!
		print('Must Enter a valid choice.')
		print('Please try again.')
		
		#return to main menu
		menu()
	
def view_students():
	# open file to read for the data records
	student_file = open('student_data_file.txt', 'r', encoding='utf-8')
	
	#create a list called 'student_data_display_list'
	student_data_display_list = student_file.read()
	
	#print all the record present in the database
	print((25 * '-') + ' View Student Data ' + (25 * '-') )
	print(student_data_display_list)
	student_file.close()
	produce_reports()
	
def males_emails():
	 #Teacher can input an ID number and display the relevant student's details
	#open the file as student_file (varibale)
	with open('student_data_file.txt', 'r', encoding='utf-8') as student_file:
		#prompt user to enter id to search 
		id_number = input('Enter ID number you require : ')
		print((25 * '-') + ' Search Result ' + (25 * '-'))
		
		#call upon our reader (this allow us to work with our file)
		studentFileReader = csv.reader(student_file)	
		
		# for each row this is read by the reader
		for row in studentFileReader:
			#add for each field in that row (this is automatically for us)
			for field in row:
				#if field is equal to the id number that is being searched for
				if field == id_number:
					#print the row corresponding to search
					print(row)
					student = Student(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
					print('Student Searched : \n', student)
					#return to main menu for futher processing of program
		print(100 * '-')

	print('This is males email module. - Work In progress')
	print('please continue with other options')
	produce_reports()
	
def females_emails():
	print('This is Females email module. - Work In progress')
	print('please continue with other options')
	produce_reports()
	
def dob_address():
	print('This is dob and address module. - Work In progress')
	print('please continue with other options')
	produce_reports()

'''	
def dob_address():
	# open the file as student file
	with open('student_data_file.txt', 'r') as student_file:
		#prompt user to enter today's date 
		print((25 * '-') + 'Do NOT Forget Anyones birthday' + (25 * '-'))
		
		current_date = date.today()
		
		#call 	upon our reader (this allows us to work with our file)
		studentFileReader = csv.reader(student_file)
		
		birthday_flag = False
		#for each row that is read by the Reader
		for row in studentFileReader:	
			for field in row:
					if current_date in field:
						# print the row corresponding to dob 
						print('Searching file .... Please wait')
						print('Send a card to : ', row)
						birthday_flag = True
		if (birthday_flag == False):
			print('Hey Looks like no one has birthday today.')
			menu()
			
		#return to main menu for further options or to quit the program				
		presenter = input ("Press 'M' to return to Main Menu : ") # press enter = presenter !
		if presenter== 'M' or presenter == 'm':
			menu()
		else:
			dob_address()

'''			
#program main to initiate the program.
if __name__=='__main__':
	main()
		
	
	
