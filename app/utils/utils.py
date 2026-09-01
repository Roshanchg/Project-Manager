from pwdlib import PasswordHash


_pwd_config=None
def getPwdConfig():
    global _pwd_config
    if _pwd_config==None:
        pwdConfig=PasswordHash.recommended()
        _pwd_config=pwdConfig
    return _pwd_config

def hashString(string:str)->str:
    pwdConfig=getPwdConfig()
    return pwdConfig.hash(string)

def matchHash(cipher:str,string:str)->bool:
    pwdConfig=getPwdConfig()
    return pwdConfig.verify(string,cipher)


