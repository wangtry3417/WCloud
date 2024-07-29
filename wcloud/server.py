import docker,os

class createServer:
    def __init__(self, host="0.0.0.0", port=3550):
        self.host = host
        self.port = port
        self.client = docker.from_env()
        self.container = self._create_container()

    def _create_container(self):
        try:
            self.client.volumes.create("wcloud-uploads")
        except docker.errors.APIError as e:
            print("Error: docker has error : ", str(e))

        container = self.client.containers.run(
            "ubuntu:latest",
            command="/bin/bash -c 'apt-get update && apt-get install -y python3 && python3 -m http.server 3550'",
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
            result = self.container.exec_run(cmds)
            return result
        except docker.errors.DockerException as e:
            print(f"運行指令錯誤: {e}")
            return None

    def upload(self, local_file_path, remote_file_path):
        try:
            with open(local_file_path, "rb") as file:
                self.container.put_archive("/uploaded_files", file.read())
        except (IOError, docker.errors.DockerException) as e:
            print(f"上載檔案錯誤: {e}")

    def download(self, remote_file_path, local_file_path):
        try:
            stream, _ = self.container.get_archive(remote_file_path)
            with open(local_file_path, "wb") as file:
                for chunk in stream:
                    file.write(chunk)
        except (IOError, docker.errors.DockerException) as e:
            print(f"下載檔案錯誤: {e}")

    def stop_container(self):
        self.container.stop()

    def remove_container(self):
        self.container.remove()
