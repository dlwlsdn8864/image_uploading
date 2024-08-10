from flask import Flask, send_file, request
import requests
import os
import subprocess

app = Flask(__name__)

# 사진을 저장할 경로 설정
IMAGE_FOLDER = '/home/raspberrypi/Desktop/uploadimg/static'

def get_next_image_path():
    # 이미지 파일 이름 목록 가져오기
    existing_files = [f for f in os.listdir(IMAGE_FOLDER) if f.startswith('image') and f.endswith('.jpg')]
    if not existing_files:
        return os.path.join(IMAGE_FOLDER, 'image1.jpg')
    
    # 파일 이름에서 숫자 추출하여 가장 큰 숫자 찾기
    max_num = max([int(f[len('image'):-len('.jpg')]) for f in existing_files])
    next_num = max_num + 1
    return os.path.join(IMAGE_FOLDER, f'image{next_num}.jpg')

@app.route('/')
def index():
    # 웹캠으로 사진 찍기
    image_path = capture_image()
    image_name = os.path.basename(image_path)
    return f'<a href="/download/{image_name}">사진 다운로드</a>'

@app.route('/test', methods=["GET"])
def test():
    res = requests.get("아이피가림:5001/getList");
    print(res);
    return "";

@app.route('/download/<filename>')
def download(filename):
    # 클릭 시 사진 다운로드 링크
    return send_file(os.path.join(IMAGE_FOLDER, filename), as_attachment=True)

def capture_image():
    # 사진을 저장할 폴더가 없으면 생성
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    # 다음 이미지 파일 경로 가져오기
    image_path = get_next_image_path()
    # fswebcam 명령어를 사용하여 사진 찍기
    subprocess.run(['fswebcam', '-r', '2592x1944', '--jpeg', '85', '-D', '1', image_path])
    return image_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
