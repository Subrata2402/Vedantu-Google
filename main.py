import discord
import requests
import json
import time
import datetime
import os
from lomond import WebSocket
from dhooks import Webhook, Embed
import websocket
from websocket import create_connection	
import aniso8601
from pytz import timezone
from bs4 import BeautifulSoup
from pymongo import MongoClient
global question
pattern = []
question = None

btk = os.env["TOKEN"] or ""

web_url = os.env["WEBHOOK_URL"] or ""

try:
	hook = Webhook(web_url)
except:
	print('Url Invalid')


def gameId():
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
	global prize
	prize = data["prizeAmount"]
	gameId = data['_id']
	return gameId

def c1():
	sid_url = f'https://vquiz.vedantu.com/socket.io/?EIO=3&transport=polling&quizId={gameId()}'
	
	headers = {
		'method':'GET',
		'path':f'/socket.io/?EIO=3&transport=polling&quizId={gameId()}',
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
		return c1
	except:
		print('Cookie error')

def SID():
	sid_url = f'https://vquiz.vedantu.com/socket.io/?EIO=3&transport=polling&quizId={gameId()}'
	
	headers = {
		'method':'GET',
		'path':f'/socket.io/?EIO=3&transport=polling&quizId={gameId()}',
		'authority':'vquiz.vedantu.com',
		'scheme':'https',
		'accept':'*/*',
		'x-ved-token': btk,
		'accept-encoding':'gzip',
		'user-agent':'okhttp/3.14.4',
	}
	r = requests.get(url=sid_url, headers=headers)
	
	try:
		rdata = r.text
		rdata = rdata[rdata.find('{'):]
		rjson = json.loads(rdata)
		SID = rjson["sid"]
		return SID
	except:
		print('SID Error...')

def c2():
	c1 = c1()
	SID = SID()
	gameId = gameId()
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
		return c1
	except:
		print('Cookie error')

def header():
	header = {
		'Upgrade':'websocket',
		'Connection':'Upgrade',
		'Sec-WebSocket-Key':'zKIu+BwuI++DC9+ZMBv4Ow==',
		'Sec-WebSocket-Version':'13',
		'X-Ved-Token': btk,
		'Cookie':c2(),
		'Host':'vquiz.vedantu.com',
		'Accept-Encoding':'gzip',
		'User-Agent':'okhttp/3.14.4'
	}
	return header

try:
	import thread
except ImportError:
	import _thread as thread

import time

def on_message(ws, message):
	if message == '3probe':
		print('Success')
		hook.send('Successfully Connected!')
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
				global question, qcnt, fqcnt, gq, prize, opt1, opt2, opt3
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
				
				time.sleep(6)
				tm = Embed(title="**⏰ | Time's Up!**", color=0x000000)
				hook.send(embed=tm)
				

			elif getType == 'SOLUTION':
				answer = mm['answer']
				ansNum = mm['answerNumber'][0]
				countData = mm['countData']
				pattern.append(ansNum)
				s = 0
				for i in countData:
					s = s + int(countData[i])
				advancing = countData[ansNum]
				eliminated = s - int(advancing)
				ans = (int(prize))/(int(advancing))
				payout = float("{:.2f}".format(ans))
				percentAdvancing = (int(advancing)*(100))/s
				pA = float("{:.2f}".format(percentAdvancing))
				percentEliminated = (int(eliminated)*(100))/s
				pE = float("{:.2f}".format(percentEliminated))
			
				
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
					
			elif getType == 'WINNER':
				tw = mm['winnerCount']
				top = mm['totalParticpants']
				ans = (int(prize))/(int(tw))
				payout = float("{:.2f}".format(ans))
				an = (int(tw)*100)/(int(top))
				pA = float("{:.2f}".format(an))
				
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
	ws = websocket.WebSocketApp(f'wss://vquiz.vedantu.com/socket.io/?EIO=3&sid={SID()}&transport=websocket&quizId={gameId()}',
		                        on_message = on_message,
		                        on_error= on_error,
		                        on_close = on_close,
		                        cookie = c2(),
		                        header = header())

	ws.on_open = on_open
	ws.run_forever()
