import telnetlib
import paramiko

# Define common variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
enable_password = 'class123!'
ssh_username = 'cisco'
ssh_password = 'cisco123!'
output_file = 'running_config.txt'  # Name of the local file to save the configuration

# Telnet session using telnetlib
try:
    tn = telnetlib.Telnet(ip_address, timeout=5)
    tn.read_until(b'Username: ', timeout=5)
    tn.write(username.encode('utf-8') + b'\n')
    tn.read_until(b'Password: ', timeout=5)
    tn.write(password.encode('utf-8') + b'\n')
    tn.read_until(b'#', timeout=5)

    # Send a command to output the running configuration
    tn.write(b'show running-config\n')
    running_config = tn.read_until(b'#', timeout=5).decode('utf-8')

    # Save the running configuration to a local file
    with open(output_file, 'w') as file:
        file.write(running_config)

    print('Telnet Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print('Running configuration saved to', output_file)
    print('------------------------------------------------------')

    # Close Telnet session
    tn.write(b'quit\n')
    tn.close()
except Exception as e:
    print(f'Telnet Session Failed: {e}')

# SSH session using paramiko
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=ssh_username, password=ssh_password, look_for_keys=False, allow_agent=False)
    ssh_shell = ssh.invoke_shell()

    # Enter enable mode
    ssh_shell.send('enable\n')
    ssh_shell.send(enable_password + '\n')
    output = ssh_shell.recv(1000)

    # Send a command to output the running configuration
    ssh_shell.send('show running-config\n')
    running_config = ssh_shell.recv(65535).decode('utf-8')

    # Save the running configuration to a local file
    with open(output_file, 'w') as file:
        file.write(running_config)

    # Exit enable mode
    ssh_shell.send('exit\n')

    # Print success message for SSH
    print('SSH Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {ssh_username}')
    print(f'Password: {ssh_password}')
    print(f'Enable Password: {enable_password}')
    print('Running configuration saved to', output_file)
    print('------------------------------------------------------')

    # Close SSH session
    ssh.close()
except Exception as e:
    print(f'SSH Session Failed: {e}')
