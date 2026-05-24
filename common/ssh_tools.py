'''
  @Description      
  @auther         leizi
  @create          2020-05-08 15:26
'''
import paramiko


class Sshtool(object):
    def __init__(self, ip: str, port: int, username: str, password: str):
        self.ip = ip
        self.port = port
        self.usernmae = username
        self.password = password

    def command(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, self.port, self.usernmae, self.password)
        ssh.exec_command(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        ssh.close()
        return stdin, stdout, stderr
