import os
import paramiko
from stat import S_ISDIR

def create_sftp_connection(hostname, username, key_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, key_filename=key_file)
    return ssh.open_sftp()

def copy_files(sftp, remote_path, local_path):
    for filename in sftp.listdir(remote_path):
        try:
            remote_filepath = os.path.join(remote_path, filename)
            local_filepath = os.path.join(local_path, filename)

            if is_directory(sftp, remote_filepath):
                os.makedirs(local_filepath, exist_ok=True)
                copy_files(sftp, remote_filepath, local_filepath)
            else:
                sftp.get(remote_filepath, local_filepath)
        except Exception as e:
            print(f"Error downloading {remote_filepath}: {e}")


def is_directory(sftp, path):
    try:
        return S_ISDIR(sftp.stat(path).st_mode)
    except IOError:
        # Path does not exist, so it's not a directory
        return False

def main():
    servers = {
        "Server 1 Location": "0.0.0.0",
        "Server 2 Location": "0.0.0.0",
        "Server 3 Location": "0.0.0.0"



    }
    paths = {
        "Server 1 Path": "/location/of/stuff",
        "Server 2 Path": "/Location/of/Stuff",
        "Server 3 Path": "/Location of Stuff"


    }
    username = "iaes"
    key_file = "/location/of/key/file"

    for server_name, ip in servers.items():
        sftp = create_sftp_connection(ip, username, key_file)
        local_path = os.path.join(os.getcwd(), server_name)
        os.makedirs(local_path, exist_ok=True)
        copy_files(sftp, paths[server_name], local_path)
        sftp.close()

if __name__ == "__main__":
    main()
