import docker
from io import BytesIO

class createServer:
    _instances = {}

    def __init__(self, host="0.0.0.0", port=3550):
        self.host = host
        self.port = port
        self.client = docker.from_env()
        self.container = None
        self.volume_name = f"wcloud-uploads-{id(self)}"

        if self.volume_name not in self._instances:
            self.container = self._create_container()
            self._instances[self.volume_name] = self
        else:
            self.container = self._instances[self.volume_name].container

    def _create_container(self):
        try:
            self.client.volumes.create(self.volume_name)
        except docker.errors.APIError as e:
            print("Error: docker has error : ", str(e))

        container = self.client.containers.run(
            "python:3.9-slim",
            command="python -m http.server 3550",
            ports={f"{self.port}/tcp": self.port},
            volumes={
                self.volume_name: {"bind": "/uploaded_files", "mode": "rw"}
            },
            environment={
                "HOST": self.host,
                "PORT": self.port
            },
            detach=True
        )
        print(f"Serving at {self.host}:{self.port}")
        return container

    def run_command(self, cmds: str):
        try:
            container = self.client.containers.run(
                "python:3.9-slim",
                command=cmds,
                volumes={
                    self.volume_name: {"bind": "/uploaded_files", "mode": "rw"}
                },
                detach=True
            )
            print(str(container))
            return container
        except docker.errors.DockerException as e:
            print(f"Error running command: {e}")
            return None
    def upload(self, remote_file_path, local_file_path):
        try:
            with open(local_file_path, "rb") as f:
                file_data = f.read()
            self.container.put_archive(
                os.path.dirname(remote_file_path),
                {"remote_file.txt": file_data}
            )
            print(f"File uploaded to {remote_file_path}")
        except (IOError, docker.errors.DockerException) as e:
            print(f"Error uploading file: {e}")
    def download(self, remote_file_path, local_file_path):
        try:
            stream, _ = self.container.get_archive(remote_file_path)
            with open(local_file_path, "wb") as file:
                for chunk in stream:
                    file.write(chunk)
        except (IOError, docker.errors.DockerException) as e:
            print(f"Error downloading file: {e}")
