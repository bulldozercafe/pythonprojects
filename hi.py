from PIL import Image
import matplotlib.pyplot as plt


# PGM 파일 열기
def display_pgm(file_path):
    try:
        # PIL 이미지로 열기
        img = Image.open(file_path)

        # 이미지 정보 출력
        print(f"Format: {img.format}")
        print(f"Size: {img.size}")
        print(f"Mode: {img.mode}")

        # 이미지 표시
        plt.imshow(img, cmap='gray')
        plt.axis('off')  # 축 숨기기
        plt.title("PGM Image Viewer")
        plt.show()
    except Exception as e:
        print(f"Error: {e}")


# PGM 파일 경로 지정
pgm_file = '1718890194_sample_640×426.pgm'  # 여기에 PGM 파일 경로를 입력하세요.
display_pgm(pgm_file)
