# Introduction

### This is mainly to be used privately, so I can not guarantee that it will work flawlessly.
This small bot can be used to check for vaccination appointments. It uses Selenium as its webbrowser.

# Installation

1. `git clone https://github.com/paddison/appointment.git`
2. If PIP is not installed: `https://pip.pypa.io/en/stable/installing/`
3. Install Selenium `pip install -U selenium`

# Usage

## getAccessCode.py
This will help you get the access codes (Vermittlungscode) to start looking for appointments. 

If run the first time it will read zip codes from the `data/allPlz.txt` file.

You will be asked to enter your email adress and phone number and age.

**When entering the phone number don't enter the leading zero or any spaces, meaning 0170 123456 will become 170123456.**
This is because the country code is already set it the form.

If you find yourself in a lot of waiting rooms, you might try other values for the SUBSERVER_LESS list (check SUBSERVER_MORE for all possible values).

If you're lucky and get a notification with a 6 digit code, the program will ask you to enter it in the form of xxx-xxx.

## checkAppointments.py
After you received an access code (Vermittlungscode) you can use this script to check if there are any appointments available.

First create `data/accessCodes.txt` and enter the link you received in the email sent to you, e.g.:
(alternatively you can run checkAppointments.py and it will create the file for you)

`https://003-iz.impfterminservice.de/impftermine/suche/ABCD-EFGH-IJKL/12345/`

 Make sure to always end with a new line, or else the file might be parsed wrong.
 
 As soon as it finds an appointment it will halt the process and wait until you entered your user data.

 # Notes
 Make sure to use a proxi and change your IP adress regularly, because the server will block you after a while.
