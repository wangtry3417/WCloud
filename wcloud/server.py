import docker

class createServer:
    def __init__(self, host="0.0.0.0", port=3550):
        self.client = docker.from_env()
        self.container = self._create_container(host, port)

    def _create_container(self, host, port):
        try:
            self.client.volumes.create(f"wcloud-uploads-{id(self)}")
        except docker.errors.APIError as e:
            print("Error: docker has error : ", str(e))

        container = self.client.containers.run(
            "python:3.9-slim",
            command="python -m http.server 3550",
            ports={f"{port}/tcp": port},
            volumes={
                f"wcloud-uploads-{id(self)}": {"bind": "/uploaded_files", "mode": "rw"}
            },
            environment={
                "HOST": host,
                "PORT": port
            },
            detach=True
        )
        print(f"Serving at {host}:{port}")
        return container

    def run_command(self, cmds: str):
        try:
            container = self.client.containers.run(
                "python:3.9-slim",
                command=cmds,
                ports={f"{port}/tcp": port},
                volumes={
                    f"wcloud-uploads-{id(self)}": {"bind": "/uploaded_files", "mode": "rw"}
                },
                detach=True
            )
            print(str(container))
            return container
        except docker.errors.DockerException as e:
            print(f"Error running command: {e}")
            return None

    def upload(self, local_file_path, remote_file_path):
        try:
            with open(local_file_path, "rb") as file:
                self.container.put_archive("/uploaded_files", file.read())
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

    def stop_container(self):
        if self.container:
            self.container.stop()

    def remove_container(self):
        if self.container:
            self.container.remove(force=True)
