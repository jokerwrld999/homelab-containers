import os
import yaml
import shutil
import subprocess

def create_volume_folders(compose_file_path, base_path):
    # Expand the tilde (~) to the user's home directory
    base_path = os.path.expanduser(base_path)

    # Clean create: delete base_path if it exists
    if os.path.exists(base_path):
        print(f"Deleting existing base path: {base_path}")
        shutil.rmtree(base_path)

    # Load Docker Compose file
    with open(compose_file_path, 'r') as file:
        compose_data = yaml.safe_load(file)

    # Check if 'volumes' key exists in the Compose file
    if 'volumes' in compose_data:
        # Iterate through volumes and create folders
        for volume in compose_data['volumes']:
            if 'driver_opts' in compose_data['volumes'][volume] and 'device' in compose_data['volumes'][volume]['driver_opts']:
                volume_path = compose_data['volumes'][volume]['driver_opts']['device']

                # Replace $VOLUME_PATH with the base_path variable
                volume_path = volume_path.replace('$VOLUME_PATH', base_path)

                if not os.path.exists(volume_path):
                    print(f"Creating folder for volume '{volume}': {volume_path}")
                    os.makedirs(volume_path)

    else:
        print("No 'volumes' key found in the Docker Compose file.")

    # Use rsync to sync the contents of the 'dashy' folder to the created base path
    dashy_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashy')
    if os.path.exists(dashy_folder_path):
        print(f"Syncing 'dashy' folder to {base_path}")
        subprocess.run(['rsync', '-r', dashy_folder_path, base_path])

if __name__ == "__main__":
    compose_file_path = "./docker-compose.yml"
    base_path = "~/homelab-containers"  # Set your base path here
    create_volume_folders(compose_file_path, base_path)
