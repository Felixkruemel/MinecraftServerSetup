import os
import getpass

currentUser=getpass.getuser()

if (currentUser!='root'):
    print('To install packages we need root access, please run this script with \"sudo python setup.py\"')
    raise SystemExit(0)
else:
    print('You are running this script as ' + currentUser)


#------------ All inputs ----------
print("""
Please insert the desired non-root username for Server setup.
The Setup will create the user.""")
targetUser = input("Default: mcserver  -> ")
if targetUser=='':
    targetUser=('mcserver')
print("Chosen user: " + targetUser)

print("""
Specify a directory for the Server installation or press enter for the default value""")
serverDirectory = input("""Default: /home/MinecraftServer/ 
-> """)
if serverDirectory=='':
    serverDirectory=('/home/MinecraftServer/')
print("Chosen Directory: " + serverDirectory)


mcversion='a'
print("""
Select the Server version you want:
    a - 1.16.1
    b - 1.15.2
    c - 1.14.4
""")
mcversion = input("Default a  -> ")
if mcversion=='':
    mcversion='a'
if not (mcversion=='a' or mcversion=='b' or mcversion=='c'):
    print("Wrong Input!")
    raise SystemExit(0)

#------ Inputs finished -----------

os.system('sudo adduser ' + targetUser + ' --disabled-login --disabled-password --no-create-home --gecos \"\"')
os.system('sudo mkdir ' + serverDirectory)
os.system('sudo apt update')
os.system('sudo apt dist-upgrade -y')
os.system('sudo apt install openjdk-8-jre -y')

if (mcversion=='a'):
    os.system('wget https://launcher.mojang.com/v1/objects/a412fd69db1f81db3f511c1463fd304675244077/server.jar -P ' + serverDirectory)
elif (mcversion=='b'):
    os.system('wget https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar -P ' + serverDirectory)
elif (mcversion=='c'):
    os.system('wget https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar -P ' + serverDirectory)

