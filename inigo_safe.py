## to-do
##  -comments
##  -survey response converted to db

import discord
import asyncio
import sqlite3 as sq
from survey import *

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	def get_user(name):
		members = client.get_all_members()
		for member in members:
			if member.name.lower() == name.lower().replace(" ", ""):
				return client.get_user_info(member.id)

		return None

	## The !day1 and !day2 commands are legacy and have been merged into the !day command
	
	##	This command is used by guild members to sign up to the first event of the week
	# if message.content.startswith('!day1'):
	# 	file = open('day1.txt', 'r')
	# 	response = message.content.split('!day1')[1]
	# 	found = False
	# 	author = message.author
	# 	for line in file: # will only let the user respond once			
	# 		if format(author) == format(line.split(None, 1)[0]):
	# 			found = True
	# 		if found:
	# 			break
	# 	file.close()
	# 	if not found:
	# 		file = open('day1.txt', 'a')
	# 		if response != '':
	# 			file.write(format(message.author) + ' ' + response.upper() + '\n')
	# 		else:
	# 			await client.send_message(message.author, "Empty role, respond again with '!day1 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
	# 		file.close()
	# 	else:
	# 		await client.send_message(message.author, "Role already sent.")
		

	# ##  This command is used by guild members to sign up to the second event of the week
	# elif message.content.startswith('!day2'):
	# 	file = open('day2.txt', 'r')
	# 	response = message.content.split('!day2')[1]
	# 	found = False
	# 	author = message.author
	# 	for line in file: # will only let the user respond once
	# 		if format(author) == format(line.split(None, 1)[0]):
	# 			found = True
	# 		if found:
	# 			break
	# 	file.close()	
	# 	if not found:
	# 		file = open('day2.txt', 'a')	
	# 		if response != '':
	# 			file.write(format(message.author) + ' ' + response.upper() + '\n')
	# 		else:
	# 			await client.send_message(message.author, "Empty role, respond again with '!day2 [Character Name] [Role:DPS/HEAL/TANK/UNAVAILABLE]'")
	# 		file.close()
	# 	else:
	# 		await client.send_message(message.author, "Role already sent.")

	if message.content.startswith('!day1'):
		try:
			con = sq.connect('events.sqlite')
			cur = con.cursor()
			User = format(message.author)
			cmd = """
			SELECT EXISTS(SELECT 1 FROM Event1 WHERE User=? COLLATE NOCASE) LIMIT 1
			"""
				
			found = cur.execute(cmd, (User,))

			if found.fetchone()[0] == 0:
				cmd = """
				INSERT INTO Event1(User, Response)
				Values(?,?)
				"""
				out = "Signed up successfully."
				Response = message.content.split('!day1')[1]
				cur.execute(cmd, (User,Response))
				con.commit()
			else:
				cmd = """
				UPDATE Event1 SET Response = ? WHERE User = ?
				"""
				out = "Response updated."
				Response = message.content.split('!day1')[1]
				cur.execute(cmd, (Response, User))
				con.commit()
		except IndexError:
			out = "Response empty, try again."
		await client.send_message(message.author, out)

	if message.content.startswith('!day2'):
		try:
			con = sq.connect('events.sqlite')
			cur = con.cursor()
			User = format(message.author)
			cmd = """
			SELECT EXISTS(SELECT 1 FROM Event2 WHERE User=? COLLATE NOCASE) LIMIT 1
			"""
			found = cur.execute(cmd, (User,))

			if found.fetchone()[0] == 0:
				cmd = """
				INSERT INTO Event2(User, Response)
				Values(?,?)
				"""
				out = "Signed up successfully."
				Response = message.content.split('!day2')[1]
				cur.execute(cmd, (User,Response))
				con.commit()
			else:
				cmd = """
				UPDATE Event2 SET Response = ? WHERE User = ?
				"""
				out = "Response updated."
				Response = message.content.split('!day2')[1]
				cur.execute(cmd, (Response, User))
				con.commit()
		except IndexError:
			out = "Response empty, try again."
		await client.send_message(message.author, out) 


	if message.content.startswith('!week'):
		try:
			con = sq.connect('events.sqlite')
			cur = con.cursor()
			day = message.content.split(None, 1)[0]
			User = format(message.author)
			
			cmd = """
			SELECT EXISTS(SELECT 1 FROM Event1 WHERE User=? COLLATE NOCASE) LIMIT 1
			"""
			found = cur.execute(cmd, (User,))
			
			if found.fetchone()[0] == 0:
				cmd = """
				INSERT INTO Event1(User, Response)
				Values(?,?)
				"""
				out = "Signed up successfully."
				Response = message.content.split(day)[1]
				cur.execute(cmd, (User,Response))
				con.commit()
			else:
				cmd = """
				UPDATE Event1 SET Response = ? WHERE User = ?
				"""
				out = "Response updated."
				Response = message.content.split(day)[1]
				cur.execute(cmd, (Response, User))
				con.commit()
			
			cmd = """
			SELECT EXISTS(SELECT 1 FROM Event2 WHERE User=? COLLATE NOCASE) LIMIT 1
			"""
			found = cur.execute(cmd, (User,))
			
			if found.fetchone()[0] == 0:
				cmd = """
				INSERT INTO Event2(User, Response)
				Values(?,?)
				"""
				out = "Signed up successfully."
				Response = message.content.split(day)[1]
				cur.execute(cmd, (User,Response))
				con.commit()
			else:
				cmd = """
				UPDATE Event2 SET Response = ? WHERE User = ?
				"""
				out = "Response updated."
				Response = message.content.split(day)[1]
				cur.execute(cmd, (Response, User))
				con.commit()
		except IndexError:
		 	out = "Response empty, try again."
		await client.send_message(message.author, out)


		
	## Used by an admin or officer to reset the two files holding the event roster; syntax is !setFile [date1] [date2]
	## Restricted from most users message.content.startswith('!setFile') and "@officer" in [x.name.lower() for x in message.author.roles]:
	elif message.content.startswith('!setfile'):
		found = False
		with open('officers.txt', 'r') as f:
			for row in f:
				if row.strip('\n') == format(message.author):
					found = True
					con = sq.connect('events.sqlite')
					cur = con.cursor()

					cmd = """
					DROP TABLE IF EXISTS Event1
					"""
					cur.execute(cmd)

					cmd = """
					DROP TABLE IF EXISTS Event2
					"""
					cur.execute(cmd)

					cmd = """
					CREATE TABLE Event1(
					User TEXT PRIMARY KEY NOT NULL,
					Response TEXT
					);
					"""
					cur.execute(cmd)

					cmd = """
					CREATE TABLE Event2(
					User TEXT PRIMARY KEY NOT NULL,
					Response TEXT
					);
					"""
					cur.execute(cmd)
		if found == False:
			await client.send_message(message.author, "Insufficient permissions.")


	## Used to private message the current event roster to sender
	elif message.content.startswith('!printlist'): #and "officer" in [x.name.lower() for x in message.author.roles]:
		
		con = sq.connect('events.sqlite')
		cur = con.cursor()
		if message.content.split('!printlist')[1] == ' day2':
			out = "Raiders for Event 2:\n"
			cmd = """
			SELECT * FROM Event2
			"""
			cur.execute(cmd)
			rec = cur.fetchall()
			
			for elem in rec:
				out += format(elem[0]) + format(elem[1]) + "\n"
		else:
			out = "Raiders for Event 1:\n"
			cmd = """
			SELECT * FROM Event1
			"""
			cur.execute(cmd)
			rec = cur.fetchall()
			
			for elem in rec:
				out += format(elem[0]) + format(elem[1]) + "\n"
		await client.send_message(message.author, out)

	elif message.content.startswith('!help'):
		commands = "Avaiable commands:\n"
		commands += "!help - returns a list of available commands\n"
		commands += "!day1 - sign up for the first event of the week\n\tex. '!day1 Cudyoustopit DPS'\n"
		commands += "!day2 - sign up for the second event of the week\n\tex. '!day2 Kerchunk TANK'\n"
		commands += "!week - sign up for both events for the week\n\tex. '!week Archdruid HEAL\n"
		commands += "!delete [week, day1, day2] - delete entry for event(s) \n\tex. !delete week\n"
		commands += "!printlist [day2] - returns list of those signed up for the specified event.\n\tNo subcommand needed for day1.\n\n"
		commands += "!survey (survey response) - registers the senders reesponse to the survey results\n"
		commands += ' \tadditional use: !survey print - returns the responses to the current survey\n'
		commands += "Officer only commands\n"
		commands += "!setfile (date 1) (date 2) - clears the current rosters for both events and sets new (given) dates.\n\tex. !setfile 4/1 4/3\n"
		commands += "!invite - sends invites out to raid members\n"
		commands += "!surveyout (survey info) - clears surrent survey results and sets new survey\n"
		
		await client.send_message(message.author, commands)
		# await client.send_message(message.author, commands1)
		# await client.send_message(message.author, commands2)
		# await client.send_message(message.author, commands3)


			

	## Used by an admin or officer to send invites to users in the given list; syntax is !invite [date of first day in raid week]
	## Restricted from most users
	elif message.content.startswith('!invite'):
		officer = False
		try:
			# if "@officer" in [x.name.lower() for x in message.author.roles]:
			with open('officers.txt', 'r') as f:
				for row in f:
					if row.strip('\n') == format(message.author):
						officer = True
			if officer:
				file = open('raiders.txt', 'r')
				date = message.content.split(' ')[1]
				for line in file:
					fName = line.replace('\n', '')
					if get_user(fName) == None:
						await client.send_message(message.author, "Error, couldn't send invite to " + format(fName))
					else:
						target = await get_user(fName)
						await client.send_message(target, "You've been invited to the event(s) in the week of " + format(date) + ""
							"\nTo sign up for both days, respond with !week [Character Name] [DPS/HEAL/TANK/UNAVAILABLE]" +
							"\nOtherwise, to sign up for individual days, respond with '!day1 [Character Name] [DPS/HEAL/TANK/UNAVAILABLE] for Tuesday\n" +
							"and repeat this in a seperate message but substitute '!day1' with '!day2' for Thursday")
				file.close()
			else:
				await client.send_message(message.author, "Insufficient permissions.")
		except IndexError:
			await client.send_message(message.author, "Incorrect syntax, try again.")

	elif message.content.startswith('!surveyout'):

		officer = False
		try:
			with open('officers.txt', 'r') as f:
				for row in f:
					if row.strip('\n') == format(message.author):
						officer = True

						content = message.content.split('!surveyout ')[1]

						survey = Survey()
						survey.set_content(content)
						
						out = ''
						out += survey.get_survey()
						raiders = open('sNames.txt', 'r')
						for line in raiders:
							fName = line.replace('\n', '')
							if get_user(fName) == None:
								await client.send_message(message.author, "Error, couldn't send invite to " + format(fName))
							else:
								target = await get_user(fName)
								await client.send_message(target, out)
						raiders.close()
				if officer == False:
					await client.send_message(message.author, "Insufficient permissions")
						
		except IndexError:
			await client.send_message(message.author, "Incorrect syntax, try again.")

	
	# survey/surveyout/surveyw/e all WIP
	#  -survey response needs to be converted to work with the database
	elif message.content.startswith('!survey'):
		officer = False
		try:
			# out = open('survey.txt', 'r')
			send = 'Survey:\n'
			count = 0
			response = message.content.split('!survey ')[1]
			with open('officers.txt', 'r') as f:
				for row in f:
					if row.strip('\n') == format(message.author):
						officer = True
			if response == 'print' and officer:
				for line in out:
					send += line
					count += 1
					if count > 4:
						await client.send_message(message.author, send)
						send = ''
						count = 0
				if count != 0:
					await client.send_message(message.author, send)
				
				#await client.send_message(message.author, send)					
			elif response == 'print':
				await client.send_message(message.author, "Insufficient permissions.")
			else:
				author = message.author
				found = False
				for line in out: # will only let the user respond once			
					if format(author) == format(line.split(None, 1)[0]):
						found = True
					if found:
						break
				out.close()

				if not found:
					out = open('survey.txt', 'a')
					if response != '':
						out.write(format(author) + ' ' + response + '\n')
						await client.send_message(author, "Response registered.")
					else:
						await client.send_message(author, "Empty response, reply again with a response.")
					out.close()
				else:
					await client.send_message(message.author, "Response already sent")
		
		except IndexError:
			await client.send_message(message.author, "Incorrect syntax, try again.")

	elif message.content.startswith('!bottest'):
		print('ping')
		
# no printing
	# elif message.content.startswith('!sprint'):
	# 	file = open('survey.txt', 'r')
	# 	for line in file:
	# 			await client.send_message(message.author, line)
	# 	file.close()
			
# legacy, likely never needed again
	# elif message.content.startswith('!delete'): # and "officer" in [x.name.lower() for x in message.author.roles]:
	# 	try:
	# 		rName = format(message.author)
	# 		if message.content.split(' ')[1] == 'week':
	# 			file = open('day1.txt', 'r+')
	# 			lines = file.readlines()
	# 			file.seek(0)
	# 			for i in lines:
	# 				if format(i.split(None, 1)[0]) != rName:
	# 					file.write(i)
	# 			file.truncate()
	# 			file.close()
	# 			file = open('day2.txt', 'r+')
	# 			lines = file.readlines()
	# 			file.seek(0)
	# 			for i in lines:
	# 				if format(i.split(None, 1)[0]) != rName:
	# 					file.write(i)
	# 			file.truncate()
	# 			file.close()

	# 		else:
	# 			fName = format(message.content.split(' ')[1]) + '.txt' 
	# 			print(rName)
	# 			file = open(fName, 'r+')
	# 			lines = file.readlines()
	# 			file.seek(0)
	# 			for i in lines:
	# 				if format(i.split(None, 1)[0]) != rName:
	# 					file.write(i)
	# 			file.truncate()
	# 			file.close()
	# 		await client.send_message(message.author, 'Entry deleted.')
	# 	except IndexError:
	# 		await client.send_message(message.author, 'Incorrect Syntax, try again.')





client.run('SECRET_PLACEHOLDER')
