import platform
import subprocess
import sys

def check_docker_env():
    """
    檢查用戶是否有 Docker 環境,並在沒有時自動下載和安裝 Docker。
    """
    try:
        # 嘗試運行 Docker 命令來檢查是否安裝
        subprocess.check_output(['docker', 'info'])
        return True
    except (subprocess.CalledProcessError, OSError):
        # 如果運行 Docker 命令失敗,則說明沒有安裝 Docker
        pass

    # 根據用戶的操作系統運行相應的 Docker 安裝命令
    system = platform.system()
    if system == 'Windows':
        print("正在為 Windows 安裝 Docker...")
        # 在 Windows 上下載並安裝 Docker Desktop
        subprocess.run(['powershell', '-Command', 'Invoke-WebRequest -UseBasicParsing -Uri https://docker.com/get-docker -OutFile get-docker.ps1 ; .\get-docker.ps1 | Out-Null'], shell=True)
    elif system == 'Darwin':
        print("正在為 macOS 安裝 Docker...")
        # 在 macOS 上下載並安裝 Docker Desktop
        subprocess.run(['brew', 'install', 'docker'], check=True)
    elif system == 'Linux':
        print("正在為 Linux 安裝 Docker...")
        # 在 Linux 上根據發行版安裝 Docker
        if 'Ubuntu' in platform.linux_distribution()[0]:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker.io'], check=True)
        elif 'CentOS' in platform.linux_distribution()[0] or 'Red Hat' in platform.linux_distribution()[0]:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True)
        else:
            print("不支持的 Linux 發行版,請手動安裝 Docker引擎。")
            return False
    else:
        print("不支持的操作系統,請手動安裝 Docker。")
        return False

    print("Docker 環境安裝完成。")
    return True
