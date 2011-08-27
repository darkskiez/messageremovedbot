#!/usr/bin/python2.6
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import time
import Skype4Py
import Levenshtein

originals = {}

class MessageRemovedBot:

    def __init__(self):
        self.Connect()
        self.LoadRecentHistory()

    def Connect(self):
        self.skype = Skype4Py.Skype(Events=self)
        if not 'OnMessageEdited' in dir(self.skype):
            raise Exception('Patched Skype4Py is not installed, see README.txt')
        self.skype.FriendlyName='MessageRemovedBot'
        self.skype.Attach()

    def LoadRecentHistory(self):
        print 'Loading Recent History'
        for Chat in self.skype.RecentChats:
            #print chat
            #print dir(chat)
            for Message in Chat._GetRecentMessages():
                originals[Message.Id] = Message.Body
        print 'Loading Complete'


    ## Skype Events

    def UserStatus(self, Status):
        print 'The status of the user changed', Status
    
    def MessageEdited(self, Message):
        #print 'Message Edited', Message
        if Message.Id in originals:
            print 'Original: ', Message.FromDisplayName, ":", originals[Message.Id]
            print 'New     : ', Message.FromDisplayName, ":", Message.Body

            if Message.Body.find(";")>=0:
                print   'Semicolon escape'
                return

            # prefixes allowed
            if (Message.Body.startswith(originals[Message.Id])):
                print   'Prefix escape'
                originals[Message.Id] = Message.Body
                return

            changechars = Levenshtein.distance(originals[Message.Id], Message.Body)
            if (Message.Body!='' and changechars <= 5):
                print 'Typo fix: ',changechars
                return

            if Message.Body == '':
                action = 'Removed'
            else:
                action = 'Changed'

            if Message.EditedBy == Message.FromHandle and Message.EditedBy != self.skype.CurrentUser.Handle:
#                try:
#                    Message.Body = originals[Message.Id]
#                except:
                    #print ""
                    #skype._GetCurrentUserProfile().FullName = Message.FromDisplayName
                    Message.Chat.SendMessage("["+action+"] "+Message.FromDisplayName+" : "+originals[Message.Id])
                    #skype._GetCurrentUserProfile().FullName = fullname

            originals[Message.Id] = Message.Body


    def MessageHistory(self, Message):
        print 'User ', Message, ' Changed history'

    def MessageStatus(self, Message, Status):
        #print 'MessageStatus ', Message, 'Status', Status
        #print dir(Message)
        if Message.Id not in originals:
            originals[Message.Id] = Message.Body



bot = MessageRemovedBot();

while True:
    time.sleep(60)

