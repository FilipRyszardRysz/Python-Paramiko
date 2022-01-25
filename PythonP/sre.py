from __future__ import print_function
import select
import yaml
import paramiko

def main():
    
    with open('config.yaml', 'r') as f:
        credentials = yaml.safe_load(f)

    with open('adresyip.yaml', 'r') as f:
        ipaddress = yaml.safe_load(f)
    
    username = credentials["usernames"]
    password = credentials["passwords"]
    length = len(username)
    bobo = []

    for host in ipaddress["hostname"]:
        hostname = host
        print("[>] Attempting Connection to: {}".format(hostname))
        for i in range(length):
            try:
                print(hostname, username[i], password[i])
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                client.connect(hostname, username=username[i], password=password[i])


            except paramiko.AuthenticationException as error:
                bobo.append(f'Host: {hostname} | Username: {username[i]}')
            
            except Exception as e:
                print(e)

            finally:
                client.close()
                print("[>] Client of session to : {} closed".format(hostname))

        with open("wrongcreds.yaml", "a") as f:
            yaml.dump(bobo, f)
            bobo.clear()

 
if __name__ == '__main__':
    main()

