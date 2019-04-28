#This file sets up a frame manager that can be called by its children.
#It works by importing each primary frame as its own module, and stacking all of those frames
#A lower frame can be accessed by calling frame.tkraise()
#It also populates the arrays used by many of the pages
import os, sys, platform

print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.exit("Python 3.6 or greater is required to run this program.")

version = "0.3b (BETA)"
print("HBUpdaterGUI version {}".format(version))

#My modules
import webhandler 
import homebrewcore
import locations 
from format import * #We import format in this manner for simplicity's sake
import customwidgets as cw #Custom tkinter widgets

#import backend, will not run standalone
import HBUpdater

import tkinter as tk
from tkinter.constants import *
print("using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

#import pages for appManager (Needs to be done after dict is populated)
import injectorpage as ip
import mainpage as mp
import settingspage as sp
import addrepopage as ar

#Main frame handler, raises and pages in z layer
class FrameManager(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		if platform.system() == 'Windows':
			print("Windows detected, setting icon")
			self.iconbitmap(homebrewcore.joinpaths(homebrewcore.assetfolder, 'HBUpdater.ico'))

		# self.resizable(False,False)
		self.geometry("790x510")   #startup size 720p
		self.minsize(width=790, height=510) #minimum size currently supported
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self,
			borderwidth = 0,
			highlightthickness = 0
			)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		#Add frames to dict, with keyword being the name of the frame
		for F in (mp.mainPage,ip.injectorScreen,sp.settingsPage,ar.addRepoScreen):
			page_name = F.__name__
			frame = F(parent=container, controller=self,back_command = lambda: self.controller.show_frame("mainPage")) 
			self.frames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("mainPage") #Show the main page frame

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.frames[page_name]
		frame.tkraise()



def UseCachedJson():
	HBUpdater.setDict(webhandler.getJsonSoftwareLinks(locations.softwarelist)) #Get software links from pre-downloaded jsons (TESTING FUNCTION, IF YOU GET AN ERROR FROM THIS LINE BECUASE I FORGOT TO COMMENT IT ON A COMMIT JUST COMMENT THIS LINE AND UNCOMMENT THE ONE BEFORE)
	HBUpdater.setIJDict(webhandler.getJsonSoftwareLinks(locations.payloadlist))
	HBUpdater.setPayloadInjector(webhandler.getJsonSoftwareLinks(locations.payloadinjector))

def GetUpdatedJson():
	HBUpdater.setDict(webhandler.getUpdatedSoftwareLinks(locations.softwarelist)) #Get fresh software links, falls back on old ones if they don't exist
	HBUpdater.setIJDict(webhandler.getUpdatedSoftwareLinks(locations.payloadlist))
	HBUpdater.setPayloadInjector(webhandler.getUpdatedSoftwareLinks(locations.payloadinjector))

if __name__ == '__main__':  
	#UseCachedJson() #use this to use only pre-downloaded json files
	GetUpdatedJson() #use this to download new json (required to get updates)
	
	for softwarechunk in HBUpdater.hbdict:
		softwarechunk["photopath"] = None

	gui = FrameManager()
	gui.title("HBUpdater")
	gui.mainloop()



# #launch with a passed software list
# def startGui(dicty):
#     setDict(HBUpdater.software)
#     gui = appManagerGui()
#     gui.mainloop()
