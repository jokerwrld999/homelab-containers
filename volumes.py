import os
import yaml
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from dotenv import load_dotenv

colorama_init()
load_dotenv()

VOLUME_PATH = os.getenv('VOLUME_PATH')

def create_volume_folders(compose_file_path, base_path):
    base_path = os.path.expanduser(base_path)

    # Load Docker Compose file
    with open(compose_file_path, 'r') as file:
        compose_data = yaml.safe_load(file)

    if 'volumes' in compose_data:
        for volume in compose_data['volumes']:
            if 'driver_opts' in compose_data['volumes'][volume] and 'device' in compose_data['volumes'][volume]['driver_opts']:
                volume_path = compose_data['volumes'][volume]['driver_opts']['device']
                volume_path = volume_path.replace('$VOLUME_PATH', base_path)
                if not os.path.exists(volume_path):
                    print(f"{Fore.BLUE}Creating folder for volume '{volume}': {volume_path} {Style.RESET_ALL}")
                    os.makedirs(volume_path)
                else:
                    print(f"{Fore.GREEN}Volume '{volume}': {volume_path} already exists{Style.RESET_ALL}")
    else:
        print(f"{Fore.MAGENTA}No 'volumes' key found in the Docker Compose file.{Style.RESET_ALL}")

if __name__ == "__main__":
    compose_file_path = "./docker-compose.yml"
    base_path = VOLUME_PATH
    create_volume_folders(compose_file_path, base_path)
