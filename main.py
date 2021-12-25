import discord
import requests
import json
import time
import datetime
from lomond import WebSocket
from dhooks import Webhook, Embed
import websocket
from websocket import create_connection	
import aniso8601
from pytz import timezone
from bs4 import BeautifulSoup
from pymongo import MongoClient
global question
global qcnt
global fqcnt
global gq
global opt1
global opt1
global opt3
pattern = []
global prize
question = None

btk = "BEARER_TOKEN"

web_url = "Webhook url"
webhook = "Webhook url"


try:
	hook = Webhook(web_url)
except:
	print('Url Invalid')

try:
	hook2 = Webhook(webhook)
except:
	print('Url Invalid')


data = MongoClient('mongodb url') # Put your mongodb url
db = data.get_database("database name") # Put your database name
vquiz = db.questions # don't need to change this

upcoming = 'https://vquiz.vedantu.com/dashboard/upcoming'
headers = {
	'method':'GET',
	'path' : '/dashboard/upcoming',
	'authority': 'vquiz.vedantu.com',
	'scheme':'https',
	'x-ved-token': btk,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',
}

r = requests.get(url=upcoming, headers=headers).json()
data = r['result'][0]
upt = data["updatedAt"]
uptm = aniso8601.parse_datetime(upt)
uptim = uptm.astimezone(timezone("Asia/Kolkata"))
up_time = uptim.strftime("%b %d, %Y %I:%M %p")
tim = data["startTime"]
tm = aniso8601.parse_datetime(tim)
x_ind = tm.astimezone(timezone("Asia/Kolkata"))
x_indi = x_ind.strftime("%b %d, %Y %I:%M %p")
prize = data["prizeAmount"]
topic = data["topic"]
time = data["startInSeconds"]
milli=int(time)
hours=(milli/(3600))
hours=int(hours)
minutes=((milli/(60))-(hours*(60)))
minutes=int(minutes)
seconds=((milli)-(hours*(3600))-(minutes*(60)))
seconds=int(seconds)
embed=discord.Embed(
	title="**__Upcoming Vedantu Quiz !__**",
	color=0x000000,
	timestamp = datetime.datetime.utcnow()
	).add_field(
		name="Quiz Topic :",
		value=topic,
		inline = False
	).add_field(
		name="Prize Money :",
		value=f"₹{prize}",
		inline = False
	).add_field(
		name="Quiz Starts In :",
		value=f"{hours} hours, {minutes} minutes, {seconds} seconds",
		inline = False
	).set_thumbnail(
		url="https://cdn.discordapp.com/attachments/799716236442861578/805139417391824896/unnamed.png"
	).set_footer(
		text=f"Vedantu Quiz"
	)
hook.send(embed=embed)
hook2.send(embed=embed)

gameId = data['_id']
sid_url = f'https://vquiz.vedantu.com/socket.io/?EIO=3&transport=polling&quizId={gameId}'

headers = {
	'method':'GET',
	'path':f'/socket.io/?EIO=3&transport=polling&quizId={gameId}',
	'authority':'vquiz.vedantu.com',
	'scheme':'https',
	'accept':'*/*',
	'x-ved-token': btk,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',
}

r = requests.get(url=sid_url, headers=headers)

try:
	x = r.cookies
	c1 = 'AWSALB='+ x['AWSALB']
except:
	print('Cookie error')

try:
	rdata = r.text
	rdata = rdata[rdata.find('{'):]
	rjson = json.loads(rdata)
	SID = rjson["sid"]
except:
	print('SID Error...')

first = f'https://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}'
headers = {
	'method':'GET',
	'path':f'/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}',
	'authority':'vquiz.vedantu.com',
	'scheme':'https',
	'accept':'*/*',
	'x-ved-token': btk,
	'cookie':c1,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',
}

r = requests.get(url=first, headers=headers)

try:
	x = r.cookies
	c1 = 'AWSALB='+ x['AWSALB']
except:
	print('Cookie error')

second = f'https://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}'

headers = {
	'method':'GET',
	'path':f'/socket.io/?EIO=3&sid={SID}&transport=polling&quizId={gameId}',
	'authority':'vquiz.vedantu.com',
	'scheme':'https',
	'accept':'*/*',
	'x-ved-token': btk,
	'cookie':c1,
	'accept-encoding':'gzip',
	'user-agent':'okhttp/3.14.4',
}

r = requests.get(url=second, headers=headers)

header = {
	'Upgrade':'websocket',
	'Connection':'Upgrade',
	'Sec-WebSocket-Key':'zKIu+BwuI++DC9+ZMBv4Ow==',
	'Sec-WebSocket-Version':'13',
	'X-Ved-Token': btk,
	'Cookie':c1,
	'Host':'vquiz.vedantu.com',
	'Accept-Encoding':'gzip',
	'User-Agent':'okhttp/3.14.4'
}

try:
	import thread
except ImportError:
	import _thread as thread

import time

def on_message(ws, message):
	if message == '3probe':
		print('Success')
		#hook.send('Successfull')
	elif message != '3':
		
			message = message[message.find('['):]
			m = json.loads(message)
			mm = m[1]

			getType = mm['type']

			if getType == 'STATUS':
				try:
					qd = mm['metadata']
					qi = qd['current_question_index']
					qno = int(qi) + 1
					tq = qd['questions_count']
				except:
					print('Show not on')

			elif getType == 'QUESTION':
				global question
				global qcnt
				global fqcnt
				global gq
				global prize
				global opt1
				global opt2
				global opt3
				question = str(mm['body']['newText']).strip()
				qs = mm['currentCount']
				qcnt = int(qs) + 1
				fqcnt = mm['totalQuestion']
				options = []
				order = []
				for i in mm['options']:
					options.append(i)
				opt1 = str(options[0]).strip()
				opt2 = str(options[1]).strip()
				opt3 = str(options[2]).strip()
				rq = str(question).replace(' ','+')
				gq ="https://google.com/search?q="+rq
				og1 = str(opt1).replace(' ','+')
				og1 = "https://google.com/search?q="+rq+"+"+og1
				og2 = str(opt2).replace(' ','+')
				og2 = "https://google.com/search?q="+rq+"+"+og2
				og3 = str(opt3).replace(' ','+')
				og3 = "https://google.com/search?q="+rq+"+"+og3
				opt = str(f"{opt1} {opt2} {opt3}").replace(' ','+')
				swa = "https://google.com/search?q="+rq+"+"+opt
				
				if "not" in question.lower():
					is_not = True
				else:
					is_not = False
				embed = discord.Embed(
					title=f'**Question {qcnt} out of {fqcnt}{" (Not Question)" if is_not else ""}**',
					description=f'**[{question}]({gq})\n\n[Search with all options]({swa})**',
					color=0x000000,
					timestamp = datetime.datetime.utcnow()
					).add_field(
						name='**Option -１**',
						value=f'**[{opt1}]({og1})**',
						inline = False
					).add_field(
						name='**Option -２**', 
						value=f'**[{opt2}]({og2})**',
						inline = False
					).add_field(
						name='**Option -３**', 
						value=f'**[{opt3}]({og3})**',
						inline = False
					).set_footer(
						text="Vedantu Quiz"
					).set_thumbnail(
						url="https://cdn.discordapp.com/attachments/803435665898602517/805343857461821470/unnamed.png"
					)
				hook.send(embed=embed)
				hook2.send(embed=embed)

				check = vquiz.find_one({"question": question})
				if check != None:
					answer = str(vquiz.find_one({"question": question})["answer"]).strip()
					if answer == opt1:
						option = "１"
					elif answer == opt2:
						option = "２"
					else:
						option = "３"
					embed = Embed(
						title=f"**__Option {option}. {answer}__**",
						color=0x000000
						)
					hook.send(embed=embed)
					hook2.send(embed=embed)

				r = requests.get(gq)
				soup = BeautifulSoup(r.text, 'html.parser')
				response = soup.find_all("span", class_="st")
				res = str(r.text)
				cnop1 = res.count(opt1)
				cnop2 = res.count(opt2)
				cnop3 = res.count(opt3)
				maxcount = max(cnop1, cnop2, cnop3)
				mincount = min(cnop1, cnop2, cnop3)
				if cnop1 == maxcount:
					embed = Embed(
						title="**__Google Results !__**",
						description=f"**１. {opt1} : {cnop1}**  ✅\n**２. {opt2} : {cnop2}**\n**３. {opt3} : {cnop3}**", 
						color=0x000000
						)
				elif cnop2 == maxcount:
					embed = Embed(
						title="**__Google Results !__**",
						description=f"**１. {opt1} : {cnop1}**\n**２. {opt2} : {cnop2}**  ✅\n**３. {opt3} : {cnop3}**", 
						color=0x000000
						)
				else:
					embed = Embed(
						title="**__Google Results !__**",
						description=f"**１. {opt1} : {cnop1}**\n**２. {opt2} : {cnop2}**\n**３. {opt3} : {cnop3}**  ✅", 
						color=0x000000)
				hook.send(embed=embed)
				hook2.send(embed=embed)


				r = requests.get(gq)
				soup = BeautifulSoup(r.text , "html.parser")
				result = soup.find("div" , class_='BNeawe').text
				if opt1.lower() in result.lower():
					embed=discord.Embed(
						title=f"**__Option １. {opt1}__**",
						description=result,
						color=0x000000,
						timestamp = datetime.datetime.utcnow()
						).set_footer(
							text="Search with Google"
							)
				elif opt2.lower() in result.lower():
					embed=discord.Embed(
						title=f"**__Option ２. {opt2}__**",
						description=result,
						color=0x000000,
						timestamp = datetime.datetime.utcnow()
						).set_footer(
							text="Search with Google"
							)
				elif opt3.lower() in result.lower():
					embed=discord.Embed(
						title=f"**__Option ３. {opt3}__**",
						description=result,
						color=0x000000,
						timestamp = datetime.datetime.utcnow()
						).set_footer(
							text="Search with Google"
							)
				else:
					embed=discord.Embed(
						title=f"**__Direct Search Result !__**",
						description=result,
						color=0x000000,
						timestamp = datetime.datetime.utcnow()
						).set_footer(
							text="Search with Google"
							)
				hook.send(embed=embed)
				hook2.send(embed=embed)

				time.sleep(6)
				tm = Embed(title="**⏰ | Time's Up!**", color=0x000000)
				hook.send(embed=tm)
				hook2.send(embed=tm)
				

			elif getType == 'SOLUTION':
				answer = mm['answer']
				ansNum = mm['answerNumber'][0]
				countData = mm['countData']
				pattern.append(ansNum)
				check = vquiz.find_one({"question": question})
				if check == None:
					q = {
					    "question": question,
					    "option_1": opt1,
					    "option_2": opt2,
					    "option_3": opt3,
					    "answer": answer,
					    "option": ansNum
                    }
					vquiz.insert_one(q)
				s = 0
				for i in countData:
					s = s + int(countData[i])
				advancing = countData[ansNum]
				eliminated = s - int(advancing)
				if int(advancing) != 0:
					ans = (int(prize))/(int(advancing))
					payout = float("{:.2f}".format(ans))
					percentAdvancing = (int(advancing)*(100))/s
					pA = float("{:.2f}".format(percentAdvancing))
				else:
					pA = 0.0
					payout = 0.0
				if int(eliminated) != 0:
					percentEliminated = (int(eliminated)*(100))/s
					pE = float("{:.2f}".format(percentEliminated))
				else:
					pE = 0.0
				if ansNum == '1':
					ansNum = "１"
				if ansNum == '2':
					ansNum = "２"
				if ansNum == '3':
					ansNum = "３"

				embed = discord.Embed(
					title=f"**Question {qcnt} out of {fqcnt}**",
					description=f"**[{question}]({gq})**",
					color=0x000000,
					timestamp = datetime.datetime.utcnow()
					).add_field(
						name="**Correct Answer :-**",
						value=f"**Option {ansNum}. {answer}**",
						inline = False
					).add_field(
						name="**Status :-**",
						value=f"● **Advancing Players : {advancing} ({pA}%)\n● Eliminated Players : {eliminated} ({pE}%)\n● Current Payout : ₹{payout}**",
						inline = False
					).add_field(
						name="**Ongoing Pattern :-**",
						value=f"**{pattern}**",
						inline = False
					).set_footer(
						text="Vedantu Quiz"
					).set_thumbnail(
						url="https://cdn.discordapp.com/attachments/803435665898602517/805343857461821470/unnamed.png"
					)
				hook.send(embed=embed)
				hook2.send(embed=embed)
					
			elif getType == 'WINNER':
				tw = mm['winnerCount']
				top = mm['totalParticpants']
				if int(tw) != 0:
					ans = (int(prize))/(int(tw))
					payout = float("{:.2f}".format(ans))
					an = (int(tw)*100)/(int(top))
					pA = float("{:.2f}".format(an))
				else:
					payout = 0.0
					pA = 0.0
				embed = discord.Embed(
					title='**__Game Summary !__**',
					description=f"● **Payout : ₹{payout}**\n● **Prize Money : ₹{prize}**\n● **Total Winners : {tw} ({pA}%)**\n● **Total Players Played : {top}**",
					color=0x000000,
					timestamp = datetime.datetime.utcnow()
					).set_footer(
						text="Vedantu Quiz"
					).set_thumbnail(
						url="https://cdn.discordapp.com/attachments/803435665898602517/805343857461821470/unnamed.png"
						)
				hook.send(embed=embed)
				hook2.send(embed=embed)
				
		
def on_error(ws, error):
	hook.send('Error')
def on_close(ws):
	hook.send('Closed')

def on_open(ws):
	def run(*args):
		ws.send('2probe')
		ws.send('5')
		while True:
			try:
				time.sleep(15)
				ws.send('2')
			except:
				hook.send('Unable to connect With Socket..')
				break
	thread.start_new_thread(run, ())

if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(f'wss://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID}&transport=websocket&quizId={gameId}',
		                        on_message = on_message,
		                        on_error= on_error,
		                        on_close = on_close,
		                        cookie = c1,
		                        header = header)

	ws.on_open = on_open
	ws.run_forever()
