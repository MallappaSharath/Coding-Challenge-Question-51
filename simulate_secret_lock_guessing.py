"""
Coding Challenge Question 51 : Most Intelligent People
This program operates in 3 modes:
1. General mode: invoking the program without any options. User needs to guess pass-code
2. Simulation mode: program has to be invoked with -s option followed by count (by default 100) to simulate key guessing
3. Report mode: program has to be invoked with -s option. Report will be generated if more than 75 users already tried unlocking.
"""


# To generate random pass-code
from random import randint

from unittest.mock import MagicMock

import sys
	
# Retrieve Pass-code from user - simulation mode
def get_the_user_input_sim():
	# when program starts in simulation mode, input() has to be mocked
	global inputs_list, input_count
	input = MagicMock(return_value=inputs_list[input_count])
	user_passcode = input("Enter the pass-code: ")
	input_count += 1
	return user_passcode


# Retrieve Pass-code from user - general mode
def get_the_user_input():		
	user_passcode = input("Enter the pass-code: ")
	return user_passcode


# Validte user pass-code
def validate_passcode(user_passcode):
	error = False
	validated_passcode = 0
	try:
		validated_passcode = int(user_passcode)
		if validated_passcode < 0:
			print("Invalid passcode!! No negative numbers")
			error = True
			return validated_passcode, error
		else:
			return validated_passcode, error
	
	except ValueError:
		error = True
		print("Invalid passcode!! passcode should be numeric")
		return validated_passcode, error

		
# Verify the user pass-code against auto-passcode		
def check_the_passcode(user_passcode, auto_passcode):
	success = False
	if user_passcode == auto_passcode:
		print("WELCOME !!!\n")
		success = True
		return success, 0
	elif user_passcode > (auto_passcode + 3):
		print("Walk down some steps\n")
		success = False
		return success, abs(auto_passcode - user_passcode)
	elif user_passcode < (auto_passcode - 3):
		print("Walk up some steps\n")
		success = False
		return success, abs(auto_passcode - user_passcode)
	else:
		print("Hop around\n")
		success = False
		return success, abs(auto_passcode - user_passcode)
		
		
def write_records_to_file(guessed_correctly, attempt_count):
	try:
		file_content = ""
		try:
			FileRead = open("user_records.txt")
			file_content = FileRead.read()
			FileRead.close()
			
		except IOError:
			FH = open("user_records.txt", "w")
			FH.close
		
		FileWrite = open("user_records.txt", "w")
		
		if file_content == "":
			FileWrite.writelines("Total number of records = 1\n")
			FileWrite.writelines("User 1:\n")
			FileWrite.writelines(f"Guessed Correctly?: {guessed_correctly}\n")
			FileWrite.writelines(f"No. of Attempts	  : {attempt_count}\n")
			FileWrite.writelines("--------------------------")
		else:
			lines = file_content.split("\n")
			record_count = int(lines[0].split(' ')[-1])
			record_count += 1
			lines[0] = f"Total number of records = {record_count}"
			line_count = 0
			for each_line in lines:
				FileWrite.write(each_line)
				if line_count < len(lines) - 1:
					FileWrite.write("\n")
					line_count += 1
			user_count = int(lines[-4].split(' ')[-1][:-1])
			# print(int(lines[-4].split(' ')[-1][:-1]))
			FileWrite.writelines(f"\nUser {user_count+1}:\n")
			FileWrite.writelines(f"Guessed Correctly?: {guessed_correctly}\n")
			FileWrite.writelines(f"No. of Attempts	  : {attempt_count}\n")
			FileWrite.writelines("--------------------------")
	
						
		FileWrite.close()
				
	except IOError:
		print("Can't open the Records file")
		
		
# Funny Secret Door Lock program starts here.
def funny_secret_door_lock(chance = 5):

	count = 0
	steps_away = 0
	nearest = 0
	success = False
	
	# Generate automatic pass-code between 10 to 40
	auto_passcode = randint(10, 40)

	print(f"You need to guess the pass-code. You have {chance} chance!\n")

	
	while count < chance:
		error = True
		validated_passcode = 0
		
		while error == True:
		
		
			if len(sys.argv) >= 2:
				if sys.argv[1] == "-s":
					user_passcode = get_the_user_input_sim()  # In simulation mode
			elif len(sys.argv) == 1: 
				user_passcode = get_the_user_input()      	  # In general mode
					
			validated_passcode, error = validate_passcode(user_passcode)
			
		success, steps_away = check_the_passcode(validated_passcode, auto_passcode)
		
		if success == True:
			write_records_to_file(True, count+1)
			break;
			
		if count == 0:
			nearest = steps_away
		else:
			if steps_away < nearest:
				nearest = steps_away
				
		count += 1
	else:
		print(f"Sorry : You were {nearest} steps away")
		write_records_to_file(False, count)

		
				
def simulate_door_lock_guessing(how_many_times=100):
	
	global inputs_list
	global input_count
	
	inputs_list = list()
	
	for count in range(how_many_times):
		del inputs_list[:]
		input_count = 0
		for index in range(5):
			inputs_list.append(randint(10, 40))		
		funny_secret_door_lock()
		
		
# Main starts here
# ================
# Simulation mode
if len(sys.argv) >= 2:
	if sys.argv[1] == "-s":
		if len(sys.argv) == 3:
			try:
				how_many_times = int(sys.argv[2])
				if how_many_times < 0:
					print("No negative numbers")
					print("To invoking simulation: simulate_secret_lock_guessing_2.py -s [count]")
					print("Where 'count' is how many times you want to simulate")
					print("if no 'count' argument provided, program simulates secret lock guessing 100 times")
	
				else:
					simulate_door_lock_guessing(how_many_times)
		
			except ValueError:
				print("To invoking simulation: simulate_secret_lock_guessing_2.py -s [count]")
				print("Where 'count' is how many times you want to simulate")
				print("if no 'count' argument provided, program simulates secret lock guessing 100 times")
		else:
			simulate_door_lock_guessing() # when program called with simulation mode and no simulation count is specified, program simulates 100 times by default

# Report mode
if len(sys.argv) >= 2:
	if sys.argv[1] == "-r":
		try:
			FileRead = open("user_records.txt")
			file_content = FileRead.read()
			if file_content == "":
				print("Not enough users tried unlocking..")
				print("Report will be generated when at least 75 users tried unlocking")
			
			lines = file_content.split("\n")
			record_count = int(lines[0].split(' ')[-1])
			if record_count < 75:
				print("Not enough users tried unlocking..")
				print("Report will be generated when at least 75 users tried unlocking")
			else:
				records_list = list()
				guessed_line_number = 2
				attempts_line_number = 3
				for each_record in range(record_count):
					records_dictionary = dict()
					records_dictionary['Gussed?'] = lines[guessed_line_number][20:]
					records_dictionary['Attepmts'] = int(lines[attempts_line_number][-1:])
					records_list.append(records_dictionary)
					guessed_line_number = guessed_line_number + 4
					attempts_line_number = attempts_line_number + 4
					
				guessed_count = 0
				failed_count = 0
				first_guess = second_guess = third_guess = fourth_guess = fifth_guess = 0
				for each_record in records_list:
				
					if each_record['Gussed?'] == "True":
						guessed_count += 1
						
						if each_record['Attepmts'] == 1:
							first_guess += 1
						elif each_record['Attepmts'] == 2:
							second_guess += 1
						elif each_record['Attepmts'] == 3:
							third_guess += 1
						elif each_record['Attepmts'] == 4:
							fourth_guess += 1
						elif each_record['Attepmts'] == 5:
							fifth_guess += 1
						
					else:
						failed_count += 1
						
				print(f"Most Intelligent People : {first_guess}")
				print(f"Failed to unlock : {failed_count}")
				print("Summary of attempts made by 75 people")
				
				if first_guess > 25:
					print("1>:", '#'*25)
				else:
					print("1>:", '#'*first_guess)
					
				if second_guess > 25:
					print("2>:", '#'*25)
				else:
					print("2>:", '#'*second_guess)

				if third_guess > 25:
					print("3>:", '#'*25)
				else:
					print("3>:", '#'*third_guess)

				if fourth_guess > 25:
					print("4>:", '#'*25)
				else:
					print("4>:", '#'*fourth_guess)

				if fifth_guess > 25:
					print("5>:", '#'*25)
				else:
					print("5>:", '#'*fifth_guess)


		except IOError:
			print("can't open file..")


# General mode
if len(sys.argv) == 1:
	funny_secret_door_lock()
	
