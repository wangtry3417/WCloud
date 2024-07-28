import docker

class createServer:
    def __init__(self, host="0.0.0.0", port=3550):
        self.client = docker.from_env()
        self.container = self._create_container(host, port)

    def _create_container(self, host, port):
        try:
            self.client.volumes.create("wcloud-uploads")
        except docker.errors.APIError:
            pass

        container = self.client.containers.run(
            "python:3.9-slim",
            command="python -m http.server 3550",
            ports={f"{port}/tcp": port},
            volumes={
                "wcloud-uploads": {"bind": "/uploaded_files", "mode": "rw"}
            },
            detach=True,
        )
        print(f"Serving at {host}:{port}")
        return container

    def upload(self, local_file_path, remote_file_path):
        with open(local_file_path, "rb") as file:
            self.container.put_archive("/uploaded_files", file.read())

    def download(self, remote_file_path, local_file_path):
        stream, _ = self.container.get_archive(remote_file_path)
        with open(local_file_path, "wb") as file:
            for chunk in stream:
                file.write(chunk)
