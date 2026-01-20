import subprocess
import os
from utils import file_path

def run_git_update():
    bat_script = file_path("run_git_update.bat")

    if not os.path.exists(bat_script):
        print(f"오류: '{bat_script}' 파일을 찾을 수 없습니다.")
        return

    # 이 파일 기준 프로젝트 루트
    project_root = os.path.dirname(os.path.abspath(__file__))

    subprocess.run(
        ["cmd.exe", "/c", bat_script],
        cwd=project_root,
        shell=True
    )
