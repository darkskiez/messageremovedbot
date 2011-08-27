
MessageRemovedBot

(c) 2011 - Mark Bryars - messageremovedbot@darkskiez.co.uk

-----------------------------------------------------------

Overview:

    Annoyed at seeing a message from someone on skype to find:
        "Message has been removed"
    or that they've edited some abuse to be nice?
    
    Protect yourself with MessageRemovedBot!

    No other communication medium supports changing or 
    removing communications in the way skype does and I find it
    to be most distruptive, thus this bot was born.

    This bot will allow small typo fixes (up to 5 chars) 
    without triggering, and it will allow edits which are just 
    appended to the last line.


Licence: 

    GPLv3 or higher - see gpl.txt

Requirements:
    Requires Python Levenshtein and Skype4Py libraries

    eg. sudo apt-get install python-levenshtein python-skype

    You will need to patch your Skype4Py to add support for edit notifcations.

    eg. patch -p0 < skype4py.patch


Usage:
    ./messageremovedbot.py

    ctrl-c to quit

