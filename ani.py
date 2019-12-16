#Karjok pangesty
#Mei 2019
#ANI

'''
Tool cacad
cuma skreping skreping doang

'''

from requests import *
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode as uenc
import sys,os,re
lr = '\033[91m'
lg = '\033[92m'
lp = '\033[95m'
lc = '\033[96m'
lx = '\033[0m'

def download(hehe):
	with open('Results/'+ui+'/'+hehe[1],'wb') as f:
		r = get(hehe[0],stream=True)
		try:
			lenk = r.headers['Content-Length']
		except:
			lenk = len(r.content)
		no = 0
		flen = round(int(lenk)/1024,1)
		if flen >= 1024:
			flen = round(flen/1024,1)
			bin = 'MB'
		else:
			bin = 'KB'
		print(f' {lp}[{lx}{flen}{bin}{lp}] {lc}{hehe[1]}')
		f.write(r.content)

content =[]
names =[]
def getimage(link):
	r = s.get(link).text
	bb = bs(r,'html.parser')
	d = bb.find('div',attrs={'class':'grid-1'})
	cek = d.find_all('div',attrs={'class':'grid-1'})
	#print(d)
	if len(cek) != 0:
			for div in cek:
				dl = div.find('a',attrs={'class':'btn btn-primary'})
				pref = re.search(r'\/\d(.*?)\.',str(dl)).group(1)
				names.append(ui+'_'+pref+'.jpg')
				content.append(dl.get('href'))
	else:
			dl = d.find('a',attrs={'class':'btn btn-primary'})
			pref = re.search(r'\/\d(.*?)\.',str(dl)).group(1)
			names.append(ui+'_'+pref+'.jpg')
			content.append(dl.get('href'))
	print(f'\r{len(content)} images collected\nctrl + c to stop..',end=''),;sys.stdout.flush()
def getvideo(link):
	r = s.get(link).text
	b = bs(r,'html.parser')
	d = b.find('div', attrs={'class':'grid-1'})
	cek = d.find_all('div',attrs={'class':'grid-1'})
	if len(cek) != 0:
		for div in cek:
			dl = div.find('a',attrs={'class':'btn btn-primary'})
			pref = re.search(r'\/\d(.*?)\.',str(dl)).group(1)
#			pref = re.findall(r'\/vp/(.*?)\/',str(dl))[0][:5]
			names.append(ui+'_'+pref+'.mp4')
			content.append(dl.get('href'))
	else:
		dl = d.find('div',attrs={'class':'media-download-link'}).find('a')
#		pref = re.findall(r'\/vp/(.*?)\/',str(dl))[0]
		pref = re.search(r'\/\d(.*?)\.',str(dl)).group(1)
		names.append(ui+'_'+pref+'.mp4')
		content.append(dl.get('href'))
	print(f'\rget {len(content)} videos..',end=''),;sys.stdout.flush()

def go(uid):
	global ui,pv,s
	s = Session()
	ui = uid
	data = {'url':'https://www.instagram.com/'+uid}
	data = uenc(data)
	url = 'https://instavideosdownloader.com/download-instagram-photos/'
	no = 0
	link =[url+'?'+data]
	linkimg = []
	pv = input(f'{lc}Download for photo/video/all ? (p/v/a):{lx} ')
	print(f'{lc}Geting {lx}{uid} {lc}info..')


	if pv == 'p':
		while True:
			try:
				r = s.get(link[no])
				no += 1
				b = bs(r.text,'html.parser')
				res = b.find('div',attrs={'class':'igphotos'})
				for a in res.find_all('a'):
					if 'ig_cache_key' in str(a):
						getimage(url+a.get('href'))
				link.append('https:'+b.find('a',attrs={'class':'next-page-block'}).get('href'))
			except:
				break

	elif pv == 'v':
		while True:
			try:
				r = s.get(link[no])
				no += 1
				b = bs(r.text,'html.parser')
				res = b.find('div',attrs={'class':'igphotos'})
				for a in res.find_all('a'):
					if not 'ig_cache_key' in str(a):
						getvideo(url+a.get('href'))
				link.append('https:'+b.find('a',attrs={'class':'next-page-block'}).get('href'))
			except:
				break
	elif pv =='a':
		while True:
			try:
				r = s.get(link[no])
				no += 1
				b = bs(r.text,'html.parser')
				res = b.find('div',attrs={'class':'igphotos'})
				for a in res.find_all('a'):
					if not 'ig_cache_key' in str(a):
						getvideo(url+a.get('href'))
					else:
						getimage(url+a.get('href'))
				link.append('https:'+b.find('a',attrs={'class':'next-page-block'}).get('href'))
			except:
				break
	else:
		exit()



#	from multiprocessing.pool import ThreadPool as tp
#	a = tp(1000)
	if len(content) != 0:
		print(f'\nDownloading {str(len(content))} media..')
#	nc = [nc for nc in zip(content,names)]
#	c = a.map(download,nc)

		for i in zip(content,names):
			download(i)
		print(lc+f'\n{str(len(content))} media sucessfully downloaded.')
		print(f'{lc}File saved in {lx}Results/{uid}')
def cek(id):
	print(f'{lc}Check {lx}{id}{lc} availabilities..')
	r = get('https://www.instagram.com/'+id).text
	b = bs(r,'html.parser')
	title = b.find('title').text
	if 'Page Not Found' in title:
		print(f'{lc}Sorry. {lx}{id} {lc}is not available !')
		print(f'{lc}You can visit {lx}https://www.instagram.com/{id} {lc}to check it.')
	else:
		r = get('https://instavideosdownloader.com/download-instagram-photos/?url='+id)
		if 'Not authorized to view user' in r.text:
			print(f'{lc}Oops ! {lx}{id}{lc} is private user  :(')
		else:
			try:
				os.mkdir('Results/'+id)
			except:
				pass
			print(f'{lx}{id} {lc}is available. !')
			go(id)
def banner():
	os.system('clear')
	print(f'''{lp}
	::::::::::::::::::::::::::::::
	::::::{lc}████{lp}::::::::::::::::::::
	::::::{lc}██{lp}::{lc}██{lp}::{lc}██{lp}{lc}██{lp}::::{lc}██{lp}::::::
	::::::{lc}██████{lp}::{lc}██{lp}::{lc}██{lp}::{lc}██{lp}::::::
	::::::{lc}██{lp}::{lc}██{lp}::{lc}██{lp}::{lc}██{lp}::{lc}██{lp}::::::
	::{lc}Instagram Media Downloader{lp}::
	::::::::::::::::::::::::::::::{lx}
''')
def menu():
	banner()
	print(f"{lc}This tool is automatically download your target instagram media.\nYou can asking or requesting for new feature to the author.\nType {lx}'help'{lc} to show the options")
	sss = input(f'{lc}\n>> {lx}')
	if sss == 'start':
		banner()
		try:
			os.mkdir('Results')
		except:
			pass
		id = input(f'{lc}Username (ex:karjok.pangesty) :{lx} ')
		while len(id) == 0:
			print(f"{lr}can't be blank.")
			id = input(f'{lc}Username (ex:karjok.pangesty) :{lx} ')
		cek(id)
	elif sss == 'help':
		banner()
		print(f'''{lc}
type anything options are available below:

options		informations
{lx}-------		------------
{lc}help{lx}		print this help and exit
{lc}start{lx}		starting the ANI Downloader Tool
{lc}about{lx}		show this tool informations
''')
	elif sss == 'about':
		banner()
		print(f'''
{lc}About
{lx}------

{lc}Name		:{lx} ANI
{lc}Version		:{lx} 1.0
{lc}Date		:{lx} May 11th, 2019 8:53PM
{lc}Author		: {lx}Karjok Pangesty (https://t.me/om_karjok)
{lc}Thanks to	:{lx} Allah SWT, Eka Pangesty,
		  my CRABS family and others.
{lc}Special thanks	: {lx}https://instavideosdownloader.com
{lc}Info		:{lx} This is a tool for downloading
		  all media from Instagram account.
		  It is very simple to use.
		  No login required
		  and it mean this tool is very safe.

''')

	else:
		exit()

if __name__=='__main__':
	banner()
	try:
		menu()
	except Exception as e:
		print(lx+'-'*40)
		print(lr+'OOps !\nSomething went wrong !')
		ex = sys.exc_info()
		print(f'{lr}error: {lx}{ex[0].__name__}\n{lr}text:{lx} {e}\n{lr}line: {lx}{ex[2].tb_lineno}')
		print(lx+'-'*40)
		print(f"""
{lc}If you don't know why this happened,
Please contact the author at
 - {lx}https://t.me/om_karjok{lc}
 - {lx}https://fb.me/om.karjok{lc}
""")
