from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import datetime

def check_root_password(host, user, passwd, encrypted_password, pre_root_pending, pre_root_updated, errors):
    try:
        dev = Device(host=host, user=user, password=passwd)
        dev.open()
        try:
            response = dev.cli("show configuration system root-authentication encrypted-password")
            dev.close()
            comparator_root = response[(response.find('"') + 1):(response.find('";'))]
            if comparator_root != encrypted_password:
                pre_root_pending.append(host)
            elif comparator_root == encrypted_password:
                pre_root_updated.append(host)
            else:
                print("error generating scope")
                error = str(e)
                errors.append(error)
        except Exception as e:
            print(f"error sending command to {host}")
            error = str(e)
            errors.append(error)
    except Exception as e:
        print(f"error opening netconf session for {host}")
        error = str(e)
        errors.append(error)

def check_admin_password(host, user, passwd, encrypted_password, admin_pending, admin_updated, errors):
    try:
        dev = Device(host=host, user=user, password=passwd)
        dev.open()
        try:
            response = dev.cli("show configuration system login user admin authentication encrypted-password")
            dev.close()
            comparator_admin = response[(response.find('"') +1):(response.find('";'))]
            if comparator_admin != encrypted_password:
                admin_pending.append(host)
            elif comparator_admin == encrypted_password:
                admin_updated.append(host)
        except Exception as e:
            print(f"error sending command to {host}")
            error = str(e)
            errors.append(error)
    except Exception as e:
        print(f"error opening netconf session for {host}")
        error = str(e)
        errors.append(error)

def update_root_password(host, user, encrypted_password, passwd, root_updated, bad, errors):
    try:
        dev = Device(host=host, user=user, password=passwd)
        dev.open()
        try:
            with Config(dev, mode='private') as cu:
                set_root = f"set system root-authentication encrypted-password {encrypted_password}"
                cu.load(set_root, format="set")
                cu.commit()
            try:
                response = dev.cli("show configuration system root-authentication encrypted-password")
                dev.close()
                comparator_updated_root = response[(response.find('"') +1):(response.find('";'))]
                if comparator_updated_root == encrypted_password:
                    root_updated.append(host)
                elif comparator_updated_root != encrypted_password:
                    bad.append(host)
                else:
                    error = (f"error verifying root password update on {host}")
                    print(error)
                    errors.append(error)
            except Exception as e:
                dev.close()
                print(f"error sending show command to {host}")
                error = str(e)
                errors.append(error)
        except Exception as e:
            dev.close()
            print(f"error sending set command to {host}")
            error = str(e)
            errors.append(error)
    except Exception as e:
        print(f"error opening netconf session for {host}")
        error = str(e)
        errors.append(error)

def update_admin_password(host, user, passwd, encrypted_password, bad, admin_updated, errors):
    try:
        dev = Device(host=host, user=user, password=passwd)
        dev.open()
        try:
            with Config(dev, mode='private') as cu:
                set_admin = f"set system login user admin authentication encrypted-password {encrypted_password}"
                cu.load(set_admin, format="set")
                cu.commit()
            try:
                response = dev.cli("show configuration system login user admin authentication encrypted-password")
                dev.close()
                comparator_updated_admin = response[(response.find('"') + 1):(response.find('";'))]
                if comparator_updated_admin == encrypted_password:
                    admin_updated.append(host)
                elif comparator_updated_admin != encrypted_password:
                    bad.append(host)
                else:
                    error = (f"error verifying admin password on {host}")
                    print(error)
                    errors.append(error)
            except Exception as e:
                dev.close()
                print(f"error sending show command to {host}")
                error = str(e)
                errors.append(error)
        except Exception as e:
            dev.close()
            print(f"error sending set command to {host}")
            error = str(e)
            errors.append(error)
    except Exception as e:
        print(f"error opening netconf session for {host}")
        error = str(e)
        errors.append(error)

def logging(errors):
    with open('log', 'a') as file:
        for item in errors:
            current_time = datetime.datetime.now()
            format_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            file.write("[" + format_time + "]" + item + "\n")

def update():
    root_pending = []
    root_updated = []
    admin_pending = []
    admin_updated = []
    bad = []
    errors = []

    user = input("username: ")
    passwd = getpass("password: ")

    encrypted_password = input("password hash: ")
    if encrypted_password.startswith("$6$"):
        with open('staging', 'r') as file:
            hosts = [line.strip() for line in file.readlines()]
        print("\n==================================================\n=[+]  pre check - root - create update scope  [+]=\n==================================================\n")
        for host in hosts:
            check_root_password(host, user, passwd, encrypted_password, root_pending, root_updated, errors)
        print("\n[*] done [*]\n")
        print("\n===================================================\n=[+]  pre check - admin - create update scope  [+]=\n===================================================\n")
        for host in hosts:
            check_admin_password(host, user, passwd, encrypted_password, admin_pending, admin_updated, errors)
        print("\n[*] done [*]\n")
        print("\n======================================\n=[+]  successfully created scope  [+]=\n======================================")
        print("\nroot password change hosts:")
        for update_root_host in root_pending:
            print(update_root_host)
        print("\nadmin password change hosts:")
        for update_admin_host in admin_pending:
            print(update_admin_host)
        print("\n=============================================\n=[+]  running - root - password updates  [+]=\n=============================================\n")
        for host in root_pending:
            update_root_password(host, user, encrypted_password, passwd, root_updated, bad, errors)
        print("\n[*] done [*]\n")
        print("\n==============================================\n=[+]  running - admin - password updates  [+]=\n==============================================\n")
        for host in admin_pending:
            update_admin_password(host, user, passwd, encrypted_password, bad, admin_updated,errors)
        print("\n[*] done [*]\n")
        print("\n========================================\n=[+]  post script - root - summary  [+]=\n========================================\n")
        for root_line in root_updated:
            print(root_line + ": updated & verified")
        print("\n=========================================\n=[+]  post script - admin - summary  [+]=\n=========================================\n")
        for admin_line in admin_updated:
            print(admin_line + ": updated & verified")
        print("\n=====================================\n=[+]  post script summary errors [+]=\n=====================================\n")
        for line in bad:
            print(line)
        error_count = len(errors)
        if error_count == 0:
            print("script finished with no errors returned")
        elif error_count == 1:
            logging(errors)
            print(f"script finished with {error_count} error returned\nsee log file for details")
        else:
            logging(errors)
            print(f"script finished with {error_count} errors returned\nsee log file for details")
    else:
        print("check hash, missing string $6$")
        error = "incorrect hash format provided"
        errors.append(error)
        logging(errors)
update()
