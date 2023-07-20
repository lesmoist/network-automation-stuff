import subprocess
import venv
venv_name = "ansible"
venv_path = f"./{venv_name}"
builder = venv.EnvBuilder(with_pip=True)
builder.create(venv_path)
activate_path = f"{venv_path}/bin/activate"
try:
    subprocess.check_call(f"source {activate_path} && python3 -m pip install pip --upgrade", shell=True)
    print(f"activated virtual environment '{venv_name}'")
except subprocess.CalledProcessError as e:
    print(f"error activating virtual environment '{venv_name}': {e}")
commands = [
    "python3 -m pip install wheel",
    "python3 -m pip install ansible",
    "ansible-galaxy install git+https://github.com/Juniper/ansible-junos-stdlib.git,,Juniper.junospython --ignore-certs --force",
    "ansible-galaxy install juniper.junos --ignore-certs --force",
    "ansible-galaxy collection install junipernetworks.junos --ignore-certs --force",
    "ansible-galaxy collection install juniper.device --ignore-certs --force",
    "pip3 install junos-eznc",
    "pip3 install ncclient",
    "pip3 install jsnapy",
    "pip3 install ansible-pylibssh",
    "pip3 install jxmlease",
]

for command in commands:
    print(f"[RUNNING]>>> ")
    try:
        result = subprocess.run(command.split(), capture_output=True, check=True)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"[ERROR]>>> {e}")