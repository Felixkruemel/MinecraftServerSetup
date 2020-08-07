import os
import getpass

currentUser=getpass.getuser()

if (currentUser!='root'):
    print('To install packages we need root access, please run this script with \"sudo python3 setup.py\"')
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

# print("""
# Specify a directory for the Server installation or press enter for the default value""")
# serverDirectory = input("""Default: /home/MinecraftServer/ 
# -> """)
# if serverDirectory=='':
#     serverDirectory=('/home/MinecraftServer/')
# print("Chosen Directory: " + serverDirectory)
serverDirectory = ('/home/'+targetUser+'/MinecraftServer/')


mcversion='a'
print("""
Select the Server version you want:
    a - 1.16.1
    b - 1.15.2
    c - 1.14.4
""")
mcversion = input("Default: a  -> ")
if mcversion=='':
    mcversion='a'
if not (mcversion=='a' or mcversion=='b' or mcversion=='c'):
    print("Wrong Input!")
    raise SystemExit(0)

print('Gib ein Passwort für den rcon Dienst ein:')
rconpw = input("Default: \"nots3cur3\"  -> ")
if rconpw=='':
    rconpw='nots3cur3'

#------ Inputs finished -----------

# os.system('sudo adduser ' + targetUser + ' --disabled-login --disabled-password --gecos \"\"')
os.system('useradd -r -m -U '+ targetUser)
os.system('sudo mkdir ' + serverDirectory)
os.system('sudo apt update')
os.system('sudo apt dist-upgrade -y')
os.system('sudo apt install openjdk-8-jre git build-essential -y')

if (mcversion=='a'):
    os.system('wget https://launcher.mojang.com/v1/objects/a412fd69db1f81db3f511c1463fd304675244077/server.jar -P ' + serverDirectory)
elif (mcversion=='b'):
    os.system('wget https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar -P ' + serverDirectory)
elif (mcversion=='c'):
    os.system('wget https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar -P ' + serverDirectory)

os.system('git clone https://github.com/Tiiffi/mcrcon.git '+ serverDirectory + 'mrcon')
print('gcc -std=gnu11 -pedantic -Wall -Wextra -O2 -s -o ' + serverDirectory + 'mcrcon '+ serverDirectory + 'mrcon/mcrcon.c')
os.system('gcc -std=gnu11 -pedantic -Wall -Wextra -O2 -s -o ' + serverDirectory + 'mcrcon '+ serverDirectory + 'mrcon/mcrcon.c')
os.system('echo \"eula=true\" >> '+ serverDirectory + 'eula.txt')
file = open(serverDirectory + "server.properties","w")
rcontext=('rcon.password='+rconpw)
file.write("""
    view-distance=10
    max-build-height=256
    server-ip=
    level-seed=
    gamemode=0
    server-port=25565
    enable-command-block=false
    allow-nether=true
    op-permission-level=4
    enable-query=false
    prevent-proxy-connections=false
    generator-settings=
    resource-pack=
    player-idle-timeout=0
    level-name=world
    motd=A Minecraft Server
    force-gamemode=false
    hardcore=false
    white-list=false
    broadcast-console-to-ops=true
    pvp=true
    spawn-npcs=true
    generate-structures=true
    spawn-animals=true
    snooper-enabled=true
    difficulty=1
    network-compression-threshold=256
    level-type=DEFAULT
    spawn-monsters=true
    max-tick-time=60000
    max-players=20
    enforce-whitelist=false
    resource-pack-sha1=
    online-mode=true
    allow-flight=false
    max-world-size=29999984
    function-permission-level=2
    rate-limit=0
    enable-rcon=true
""" + rcontext)

systemdfile = open('/etc/systemd/system/MinecraftServer.service','w')
Directorysetting = ('WorkingDirectory='+serverDirectory)
Stopsetting = ('ExecStop='+serverDirectory + 'mcrcon -H 127.0.0.1 -P 25575 -p '+ rconpw + ' stop')
Usersetting = ('User='+targetUser)
systemdfile.write("""
[Unit]
Description=Minecraft Server
After=network.target

[Service]
""" +
Usersetting + """
Nice=1
KillMode=none
"""
+ Directorysetting + """
ExecStart=/usr/bin/java -Xmx1024M -Xms1024M -jar server.jar nogui
""" 
+ Stopsetting + """
[Install]
WantedBy=multi-user.target """
)

os.system('systemctl daemon-reload')
os.system('chown -R '+ targetUser +':'+ targetUser + ' ' + serverDirectory)
# os.system('systemctl start MinecraftServer')



print("""

---------------------------------
Der Server wurde erstellt Der aktuelle Status ist mit dem Befehl \"sudo systemctl status MinecraftServer\" abfragbar
Generelle Infos:
Zum Starten des Servers: \"sudo systemctl start MinecraftServer\"
Zum Stoppen des Servers: \"sudo systemctl stop MinecraftServer\"
Zum Einloggen in die Admin Konsole: \"""" + serverDirectory + 'mcrcon -H 127.0.0.1 -P 25575 -p your-entered-password -t' + """
Um den Server automatisch beim Systemstart zu starten: \"sudo systemctl enable MinecraftServer\"
----------------------------------

""")
