#!/usr/bin/python

import optparse
import mimetypes
import os.path
import tempfile
import zipfile
import shutil
import plistlib



class Conventer(object):
	def __init__(self, sourcepath, **kwargs):
		self.path = sourcepath
		self.themename = os.path.splitext(os.path.basename(sourcepath))[0]
		print 'Assigned theme name - ' + self.themename
		self.plist = plistlib.readPlist(self.FindPListFile())
		print self.plist

	def SavePidginTheme(self, path):
		pass

	def GetPidginThemeDefaultDir(self):
		pass

	def MkThemeDir(self):
		path = self.GetPidginThemeDefaultDir()
		print 'Making theme dirs : %s ...' % path
		try:
			os.makedirs(path)
		except OSError:
			print 'Cannot make dir %s , maybe already theme exist?' % path
			#Exit('Cannot make dir %s , maybe already theme exist?' % path)
		
		return path


	def FindPListFile(self):
		for file in os.listdir(self.path):
			if os.path.splitext(file)[1].lower()=='.plist':
				print "Found .plist file: " + self.path+'/'+file
				return self.path+'/'+file



class ConventerSound(Conventer):
	###Very small list of pidgin's messages
	__convtable = {
	'Connected': '',
'Disconnected': '',
'New Mail Received' : '',
'Authorization Requested' : '',
'Contact is no longer seen' :'',
'Contact is seen' : '',
'Contact Returned from Away' : '',
'Contact Returned from Idle' : '',
'Contact Signed Off' : 'logout',
'Contact Signed On' : 'login',
'Contact Went Away' : '',
'Contact Went Idle' :'',
'Contact Invites You to Chat'
'Contact Joins' : 'join_chat',
'Contact Leaves' : 'left_chat',
'Message Received': 'im_recv',
'Message Received (Background Chat)':'',
'Message Received (Background Group Chat)':'',
'Message Received (Group Chat)' :'chat_msg_recv',
'Message Received (New)':'first_im_recv',
'Message Sent': 'send_im',
'Notification received':'',
'You Are Mentioned (Group Chat)':'nick_said',
'File Transfer Began':'',
'File Transfer Being Offered to Remote User':'',
'File Transfer Canceled Remotely':'',
'File Transfer Complete':'',
'File transfer failed':'',
'File Transfer Request':'',
'Error':'',
'Miscellaneous1':'',
'Miscellaneous2':'',
'Miscellaneous3':'',
'Miscellaneous4':'',
'Miscellaneous5':'',
'Miscellaneous6':'',
'Miscellaneous7':'',
'Miscellaneous8':'',
'Miscellaneous9':'',
'Miscellaneous10':'',
'Miscellaneous11':'',
'Miscellaneous12':'',
'Miscellaneous13':'',
'Miscellaneous14':'',
'Miscellaneous15':'',
'Miscellaneous16':'',
'Miscellaneous17':'',
'Miscellaneous18':'',
'Miscellaneous19':'',
}

	
	def __init__(self, sourcepath, **kwargs):
		super(ConventerSound,self).__init__(sourcepath, **kwargs)
		self.sound_format = kwargs['sound_format']
	

	def GetPidginThemeDefaultDir(self):
		return os.path.expanduser('~/.purple/themes/'+self.themename+'/purple/sound')


	def SavePidginTheme(self,path):
		import xml.etree.ElementTree
		ET = xml.etree.ElementTree
		import datetime
		theme = ET.Element("theme")
		desk = ET.SubElement(theme, "description")
		desk.text = "Generated at %s in adium2pidgin theme convert" % \
				datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		theme.attrib = {"type":"sound", "name":self.themename,\
				 'author':"adium2pidgin conventer"}
		events = []
		if not path:
			path = self.MkThemeDir()
		for soundtype in self.plist['Sounds']:
			try:
				if self.__convtable[soundtype]!='':
					sourcefile = self.path + '/'+ self.plist['Sounds'][soundtype]
					resultfile = os.path.basename(\
						os.path.splitext(sourcefile)[0]+'.'+self.sound_format)
					events.append(ET.SubElement(theme, "event"))
					events[-1].attrib={'name':self.__convtable[soundtype],
							'file':resultfile}
					command = "ffmpeg -i '%s' -f %s '%s'" % \
						(sourcefile, self.sound_format, path+'/'+resultfile)
					print "Converting sounds: running %s ..." % command
					os.system(command)
				else:
					print ":( cannot find pidgin event for %s adium event" % soundtype
			except KeyError:
				print "Unknow adium event: %s" % soundtype
		tree = ET.ElementTree(theme)
		xmlfilepath = path+'/'+'theme.xml'
		print 'Soaving theme.xml in %s' % xmlfilepath
		tree.write(xmlfilepath)
		os.system("xmllint --format '%s' --output '%s'"%(xmlfilepath,xmlfilepath))		
		

class ConventerDock(Conventer):
	def GetPidginThemeDefaultDir(self):
                return os.path.expanduser('~/.config/cairo-dock/third-party/pidgindock/Themes/'+self.themename)
	def SavePidginTheme(self,path):
		if not path:
                        path = self.GetPidginThemeDefaultDir()
		shutil.copytree(self.path, path)
		print "Docktheme installed to %s" % path



class ConventerEmoticon(Conventer):
	
	def GetPidginThemeDefaultDir(self):
		return os.path.expanduser('~/.purple/smileys/'+self.themename)

	def SavePidginTheme(self,path):
		import datetime
		description = "Generated at %s in adium2pidgin theme convert" % \
				datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		name = self.themename
		author = "adium2pidgin conventer"

		icons = []
		if not path:
			path = self.MkThemeDir()

		for iconid in self.plist['Emoticons']:
			sourcefile = self.path + '/'+iconid
			iconname = self.plist['Emoticons'][iconid]['Name']
			eqvs='   '
			for eqv in self.plist['Emoticons'][iconid]['Equivalents']:
				if eqv == ":-)":
					mainicon = iconid
				eqvs+='    '+eqv
			resultfile = os.path.basename(sourcefile)
			icons.append(iconid+eqvs)
			shutil.copy(sourcefile, path+'/'+resultfile)
		themefilepath = path+'/'+'theme'
		
		print 'Saving theme in %s' % themefilepath
		res = []
		res.append('Name=%s'%name)
		res.append('Description=%s'%description)
		res.append('Icon=%s'%mainicon)
		res.append('Author=%s'%author)
		res+=['','[default]','']
		res+=icons
		###dirtyhack
		f = open(themefilepath,'w')
		for i in res:
			f.write(i+'\n')
		print res
		f.close()
		print('Done.')

class ConventerStatus(Conventer):
	###many work (((
	__convtable = {
'Generic Available':'pidgin-status-available',
'Free for Chat':'pidgin-status-chat',
'Available for Friends Only':'',
'Generic Away':'pidgin-status-away',
'Extended Away':'pidgin-status-xa',
'Away for Friends Only':'pidgin-status-away',
'DND':'pidgin-status-busy',
'Not Available':'pidgin-status-busy',
'Occupied':'pidgin-status-busy',
'BRB':'',
'Busy':'pidgin-status-busy',
'Phone':'pidgin-status-busy',
'Lunch':'pidgin-status-busy',
'Not At Home':'pidgin-status-xa',
'Not At Desk':'pidgin-status-xa',
'Not In Office':'pidgin-status-xa',
'Vacation':'pidgin-status-xa',
'Stepped Out':'pidgin-status-xa',
'Idle And Away':'pidgin-status-busy',
'Idle':'pidgin-status-busy',
'Invisible':'pidgin-status-invisible',
'Offline':'pidgin-status-offline',
'Unknown':'',
		}


	def GetPidginThemeDefaultDir(self):
		return os.path.expanduser('~/.purple/themes/'+self.themename+'/purple/status-icon')


	def SavePidginTheme(self,path):
		import xml.etree.ElementTree
		ET = xml.etree.ElementTree
		import datetime
		theme = ET.Element("theme")
		desk = ET.SubElement(theme, "description")
		desk.text = "Generated at %s in adium2pidgin theme convert" % \
				datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		theme.attrib = {"type":"pidgin status icon", "name":self.themename,\
				 'author':"adium2pidgin conventer"}
		icons = []
		if not path:
			path = self.MkThemeDir()
		try:
			os.mkdir(path+'/'+'16')
		except OSError:
                        print 'Cannot make dir %s , maybe already theme exist?' % path+'/'+'16'

		for iconid in self.plist['List']:
			try:
				if self.__convtable[iconid]!='':
					sourcefile = self.path + '/'+ self.plist['List'][iconid]
					resultfile = os.path.basename(sourcefile)
					icons.append(ET.SubElement(theme, "icon"))
					icons[-1].attrib={'id':self.__convtable[iconid],
							'file':resultfile}
					
					##dirty hack
					icons.append(ET.SubElement(theme, "icon"))
					icons[-1].attrib={'id':self.__convtable[iconid]+"-i",
							'file':resultfile}
					shutil.copy(sourcefile, path+'/16/'+resultfile)
				else:
					print ":( cannot find pidgin event for %s adium event" % iconid
			except KeyError:
				print "Unknow adium status icon id: %s" % iconid
		tree = ET.ElementTree(theme)
		xmlfilepath = path+'/'+'theme.xml'
		print 'Saving theme.xml in %s' % xmlfilepath
		tree.write(xmlfilepath)
		os.system("xmllint --format '%s' --output '%s'"%(xmlfilepath,xmlfilepath))		
	






Conventors = {'sound': [ConventerSound,  ['.adiumsoundset']],
		'emoticon': [ConventerEmoticon, ['.adiumemoticonset']],
		'status': [ConventerStatus, ['.adiumstatusicons', '.adiumstatusicon']],
		'dockbar': [ConventerDock, ['.adiumicon' ]]
		}





def Exit(message):
	global TMP_DIR_NAME
	try:
		if TMP_DIR_NAME!="":
			print "Remove temporary '%s' directory..." % TMP_DIR_NAME
			shutil.rmtree(TMP_DIR_NAME)
			print "Done."
	except:
		pass
	print message
	
	exit()


def Unpack(path):
	"""Unpack archive and return temp dir if it is arc, if path is dir return dir"""
	mimetypes.init()
	filetype = mimetypes.guess_type(path)
	print filetype

	if os.path.isfile(path):
		if filetype[0] == 'application/zip':
			print "Source is zip file, unpacking to tmp dir..."
			temp = tempfile.mkdtemp(prefix="adium2pidgin", suffix=os.path.basename(path))
			zip = zipfile.ZipFile(path)
			zip.extractall(temp)
			print "Source unpacked to '%s' directory" % temp
			global TMP_DIR_NAME
			TMP_DIR_NAME = temp
			for dir in os.listdir(temp):
				if dir!='__MACOSX' and os.path.isdir(temp+'/'+dir):
					resdir = temp+'/'+dir
			try:
				return resdir
			except:
				Exit("Can't found correct theme in zip archive!")
		else:
			Exit("Source file is not zip archive!")
	elif os.path.isdir(path):
		print "Source is dir, processing..."
		return os.path.normpath( path)
	else:
		Exit("Source path do not exist!")


def ParseArgs():
	parser = optparse.OptionParser(usage = "Usage: %prog [-o PATH] [-t auto|sound|status|emoticon] [-s aif|mp3|wav] source_adium_theme")
	
	parser.add_option("-o", "--output", dest="output",
                  help="write result Pidgin theme to PATH, default: ~/.purple/themes/$THEMENAME/", metavar="PATH")
	parser.add_option("-t", "--type", dest="type",
                  help="type of theme, may be: auto, sound, status or emoticon, default: auto", metavar="TYPE")
	parser.add_option("-s", "--sound-format", dest="sound_format",
                  help="convert sound to: aif, wav or mp3, default: mp3 ", metavar="SOUND_FORMAT")
	(options, args) = parser.parse_args()
	
	if len(args) > 1:
        	parser.error("No input file or directory")
	
	return (options, args[0])


def DetectType(path):
	(root, ext) = os.path.splitext(path)
	ext = ext.lower()
	for type in Conventors:
		if ext in Conventors[type][1]:
			return type
	Exit("Unable to detect type of theme, select it manual with --type option!")


if __name__ == "__main__":
	__TMP_DIR_NAME = ""
	(options,inputpath) = ParseArgs()
	print options
	if not ((options.type in ['dockbar','auto','sound','emoticon','status',None]) \
		and (options.sound_format in ['wav','aif','mp3',None])):
		Exit('Wrong --type or --sound-format parametres! Try --help option!')
	print inputpath
	source = Unpack(inputpath)
	print "Work with %s theme directory" % source
	if not options.type or options.type=='auto':
		options.type = DetectType(source)
		print "Auto-detect type of theme: %s" % options.type
	

	if not options.sound_format:
		options.sound_format = 'wav'

	conventer = Conventors[options.type][0](sourcepath=source, sound_format=options.sound_format)
	#conventer.LoadAdiumTheme(source)

	conventer.SavePidginTheme(options.output)
	
	Exit("Succsesful!")
