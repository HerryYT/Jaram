# Jaram
# A MC:BE Software
# https://github.com/SFWTeam/Jaram
# By SFW-Team
# And GianC-Dev
# -------------------------------

from src.main.Jaram.VersionInfo import version
from src.main.Jaram.server.Server import players

from src.main.Jaram.server.Server import playersip


class player:
    pass


class playerLogin:
    def __init__(self, name, ip, ver):
        self.p = players
        self.pip = playersip
        self.name = name
        self.ip = ip
        self.ver = ver
        if self.ver > version[1]:
            print('Logined {}' + self.name)
            players.append('{}' + self.name)
