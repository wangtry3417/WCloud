import os
import subprocess
from .server import createServer

class WcloudRunner(createServer):
    def __init__(self, host="0.0.0.0", port=3550):
        super().__init__(host, port)

    def run_script(self, script_path):
        script_name = os.path.basename(script_path)
        remote_script_path = f"/uploaded_files/{script_name}"
        self.upload(script_path, remote_script_path)

        command = ["docker", "exec", self.container.id, "python", remote_script_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
