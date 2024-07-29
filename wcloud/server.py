import docker,os

class createServer:
    def __init__(self, host="0.0.0.0", port=3550):
        self.host = host
        self.port = port
        self.client = docker.from_env()
        self.container = None

    def get_container(self):
        if not self.container:
            self.container = self._create_container()
        return self.container

    def _create_container(self):
        try:
            self.client.volumes.create("wcloud-uploads")
        except docker.errors.APIError as e:
            print("Error: docker has error : ", str(e))

        container = self.client.containers.run(
            "python:3.9-slim",
            command="python -m http.server 3550",
            ports={f"{self.port}/tcp": self.port},
            volumes={
                "wcloud-uploads": {"bind": "/uploaded_files", "mode": "rw"}
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
            container = self.get_container()
            result = container.exec_run(cmds)
            return result
        except docker.errors.DockerException as e:
            print(f"Error running command: {e}")
            return None

    def upload(self, local_file_path, remote_file_path):
        try:
            container = self.get_container()
            with open(local_file_path, "rb") as file:
                container.put_archive("/uploaded_files", file.read())
        except (IOError, docker.errors.DockerException) as e:
            print(f"Error uploading file: {e}")

    def download(self, remote_file_path, local_file_path):
        try:
            container = self.get_container()
            stream, _ = container.get_archive(remote_file_path)
            with open(local_file_path, "wb") as file:
                for chunk in stream:
                    file.write(chunk)
        except (IOError, docker.errors.DockerException) as e:
            print(f"Error downloading file: {e}")

    def stop_container(self):
        if self.container:
            self.container.stop()

    def remove_container(self):
        if self.container:
            self.container.remove(force=True)
