#!/usr/bin/python3
"""
PCMUS - GUI controls for CMUS written in Python with Tkinter
Copyright (C) 2014 0rovan

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import socket
import tkinter as tk
from os.path import dirname

class Host(object):
	def __init__(self,ip,passwd,port):
		self.so=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.so.settimeout(2);
		try:self.so.connect((ip,int(port)))
		except:
			Error('Unable to connect to\n'+ip+':'+str(port)).mainloop()
			exit()
		if not self.cmd(passwd):
			Error('Invalid password').mainloop()
			self.so.close()
			exit()
	def cmd(self,command):
		self.so.send((command+'\n').encode())
		res=self.so.recv(1024).decode()[:-1]
		return True if res=='' else False

class Window(tk.Frame):
	def __init__(self,geometry,title):
		tk.Frame.__init__(self)
		self.grid()
		x=(self.master.winfo_screenwidth()-int(geometry.split('x')[0]))/2
		y=(self.master.winfo_screenheight()-int(geometry.split('x')[1]))/2
		self.master.geometry(geometry+'+'+str(round(x))+'+'+str(round(y)))
		self.master.title(title)
	def close(self):
		self.master.destroy()

class Pcmus(Window):
	def __init__(self,host):
		Window.__init__(self,'365x190','PCMUS')
		Player(self,host)

class Login(Window):
	def __init__(self):
		conf=open(REL_PATH+'/pcmus.conf','r')
		config=conf.readlines()
		conf.close()
		Window.__init__(self,'255x300','LOGIN')
		tk.Label(self,text='PCMUS',font='Mono 12 bold',pady=15).grid(row=0,columnspan=2)
		tk.Label(self,text='Host:',width=10,font='Mono 12',pady=20).grid(row=1,column=0)
		self.host=tk.Entry(self,width=14,font='Mono 12')
		self.host.grid(row=1,column=1)
		self.host.insert(0,config[0][:-1])
		tk.Label(self,text='Port:',width=10,font='Mono 12',pady=20).grid(row=2,column=0)
		self.port=tk.Entry(self,width=14,font='Mono 12')
		self.port.grid(row=2,column=1)
		self.port.insert(0,config[1][:-1])
		tk.Label(self,text='Password:',width=10,font='Mono 12',pady=20).grid(row=3,column=0)
		self.passwd=tk.Entry(self,width=14,font='Mono 12')
		self.passwd.grid(row=3,column=1)
		self.passwd.insert(0,config[2][:-1])#
		tk.Label(self).grid()
		tk.Button(self,text='Log In',command=self.authorize,font='Mono 12 bold').grid(columnspan=2)
	def authorize(self):
		host=self.host.get()
		passwd=self.passwd.get()
		port=self.port.get()
		self.close()
		conf=open(REL_PATH+'/pcmus.conf','w')
		conf.write(host+'\n'+port+'\n'+passwd+'\n')
		conf.close()
		Pcmus(Host(host,passwd,port)).mainloop()

class Error(Window):
	def __init__(self,text):
		Window.__init__(self,'255x120','Error')
		tk.Label(self,text=text+'',width=25,font='Mono 12 bold',pady=20).grid(sticky=tk.N)
		tk.Button(self,text='ok',command=self.close,font='Mono 12 bold').grid()
	def close(self):
		self.master.destroy()
		Login().mainloop()

class Player(tk.Frame):
	def __init__(self,master,host):
		tk.Frame.__init__(self,master)
		self.grid()
		tk.Button(self,bitmap='@'+REL_PATH+'/img/play.xbm',command=lambda:host.cmd('player-play')).grid(row=0,column=0)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/pause.xbm',command=lambda:host.cmd('player-pause')).grid(row=0,column=1)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/stop.xbm',command=lambda:host.cmd('player-stop')).grid(row=0,column=2)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/s.xbm',command=lambda:host.cmd('toggle shuffle')).grid(row=0,column=3)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/prev.xbm',command=lambda:host.cmd('player-prev')).grid(row=1,column=0)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/back.xbm',command=lambda:host.cmd('seek -1m')).grid(row=1,column=1)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/forward.xbm',command=lambda:host.cmd('seek +1m')).grid(row=1,column=2)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/next.xbm',command=lambda:host.cmd('player-next')).grid(row=1,column=3)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/mute.xbm',command=lambda:host.cmd('vol 0%')).grid(row=2,column=0)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/minus.xbm',command=lambda:host.cmd('vol -5%')).grid(row=2,column=1)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/plus.xbm',command=lambda:host.cmd('vol +5%')).grid(row=2,column=2)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/fullvol.xbm',command=lambda:host.cmd('vol 96%')).grid(row=2,column=3)
		tk.Label(self,text='Open file',font='Mono 10').grid(row=3,column=0)
		address=tk.Entry(self,font='Mono 8',width=29)
		address.grid(row=3,column=1,columnspan=2)
		tk.Button(self,bitmap='@'+REL_PATH+'/img/load.xbm',command=lambda:host.cmd('player-play '+address.get())).grid(row=3,column=3)
		

REL_PATH=dirname(__file__)
Login().mainloop()
