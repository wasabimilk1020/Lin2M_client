import subprocess
import os

def run_bat_as_admin():
    """배치 스크립트를 관리자 권한으로 실행하는 함수"""
    bat_script = os.path.abspath("C:/Users/eunsu/Documents/Lineage2M_client/computer_restart/run_as_admin.bat")  # 절대 경로 변환

    if not os.path.exists(bat_script):  # 파일이 실제로 존재하는지 확인
        print(f"오류: '{bat_script}' 파일을 찾을 수 없습니다.")
        return

    subprocess.run(["cmd.exe", "/c", "start", bat_script], shell=True)  # ✅ bat_script 사용




