import docker

class connectServer:
    def __init__(self, host="0.0.0.0", port=3550):
        self.host = host
        self.port = port
        self.client = docker.from_env()
        self.container = self._connect_to_container()

    def _connect_to_container(self):
        try:
            containers = self.client.containers.list(filters={"status": "running"})
            for container in containers:
                if container.ports.get(f"{self.port}/tcp"):
                    return container
            print(f"No running container found on port {self.port}")
            return None
        except docker.errors.DockerException as e:
            print(f"Error connecting to container: {e}")
            return None

    def run_command(self, cmds: str):
        try:
            if self.container:
                result = self.container.exec_run(cmds)
                return result
            else:
                print("No container connected")
                return None
        except docker.errors.DockerException as e:
            print(f"Error running command: {e}")
            return None

    def upload(self, local_file_path, remote_file_path):
        try:
            if self.container:
                with open(local_file_path, "rb") as file:
                    self.container.put_archive("/uploaded_files", file.read())
            else:
                print("No container connected")
        except (IOError, docker.errors.DockerException) as e:
            print(f"Error uploading file: {e}")

    def download(self, remote_file_path, local_file_path):
        try:
            if self.container:
                stream, _ = self.container.get_archive(remote_file_path)
                with open(local_file_path, "wb") as file:
                    for chunk in stream:
                        file.write(chunk)
            else:
                print("No container connected")
        except (IOError, docker.errors.DockerException) as e:
            print(f"Error downloading file: {e}")
    def stop_container(self):
        if self.container:
            self.container.stop()

    def remove_container(self):
        if self.container:
            self.container.remove(force=True)
