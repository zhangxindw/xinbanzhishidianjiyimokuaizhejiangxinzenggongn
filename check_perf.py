import paramiko
import time

host = '154.201.94.140'
port = 22
username = 'root'
password = '6dwic8N532a7'

def execute_command(client, cmd, timeout=60):
    print(f'Executing: {cmd}')
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
    time.sleep(2)

    output = ''
    error = ''
    exit_status = 0

    try:
        while True:
            if stdout.channel.recv_ready():
                chunk = stdout.read(2048).decode()
                if chunk:
                    output += chunk
                else:
                    break
            if stdout.channel.exit_status_ready():
                exit_status = stdout.channel.recv_exit_status()
                break
            time.sleep(0.5)
    except Exception as e:
        print(f'Read error: {e}')

    try:
        while True:
            if stderr.channel.recv_ready():
                chunk = stderr.read(2048).decode()
                if chunk:
                    error += chunk
                else:
                    break
            if stderr.channel.exit_status_ready():
                break
            time.sleep(0.5)
    except:
        pass

    if output:
        print(f'Output: {output}')
    if error:
        print(f'Error: {error}')
    print(f'Exit status: {exit_status}')
    return exit_status, output, error

try:
    print(f'Connecting to {host}...')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=username, password=password, timeout=30)
    transport = client.get_transport()
    transport.set_keepalive(30)

    print('Connected!')

    # Check if debug mode is on
    print('=== Checking Flask Debug Mode ===')
    exit_status, output, error = execute_command(client, 'grep -n "debug\|Debug\|DEBUG\|reloader\|use_reloader" /root/ruankaoshuati/backend/app.py | head -10')

    # Test sequential practice API (chapter 1 has id=2)
    print('=== Testing Sequential Practice API ===')
    stdin, stdout, stderr = client.exec_command('time curl -s -X POST http://127.0.0.1:5000/api/practice/sequential -H "Content-Type: application/json" -d \'{"chapter_ids": [2]}\' -o /tmp/seq_response.json 2>&1', get_pty=True)
    time.sleep(10)
    output = stdout.read().decode()
    error = stderr.read().decode()
    print('Output:', output)
    print('Error:', error)

    # Check response size
    exit_status, output, error = execute_command(client, 'ls -la /tmp/seq_response.json && head -c 500 /tmp/seq_response.json')

    print('=== Done ===')
    client.close()

except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
