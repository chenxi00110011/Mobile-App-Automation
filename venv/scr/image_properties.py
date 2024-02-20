import os
import shutil
import cv2
import pytesseract
import subprocess
import ntp_util


def get_image_properties_opencv(image_file):
    """
    使用 OpenCV 库读取图片属性。返回一个包含图片属性的字典。

    Args:
        image_file: 图片文件路径

    Returns:
        包含图片属性的字典
    """
    image = cv2.imread(image_file)
    height, width, channels = image.shape

    properties = {
        "size": (width, height),
        "channels": channels
    }

    return properties


def get_all_image_properties(folder):
    """
    获取指定文件夹中所有图片的大小。

    Args:
        folder: 文件夹路径

    Returns:
        包含图片文件名和大小的字典列表
    """
    image_properties = []

    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            file_path = os.path.join(folder, filename)
            properties = get_image_properties_opencv(file_path)
            properties["filename"] = filename
            image_properties.append(properties)

    return image_properties


def recognize_text(image_path, crop_ratio: tuple):
    """输入直播图片，返回画面中的时间戳"""
    # 读取图片
    img = cv2.imread(image_path)
    # 获取图片宽度、高度
    height, width, channels = img.shape
    # 裁剪图片
    cropped = img[int(height * crop_ratio[0]):int(height * crop_ratio[1]),
              int(width * crop_ratio[2]):int(width * crop_ratio[3])]
    # cropped = img[0:int(height*0.089), 0:int(width*0.31)]
    cv2.imwrite('cropped.jpg', cropped)
    # 灰度化处理
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # 二值化处理
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # OCR识别
    data = pytesseract.image_to_data(thresh, lang='eng', config='--psm 6', output_type=pytesseract.Output.DICT)
    text_coords = {}
    for i, text in enumerate(data['text']):
        if text == '':
            continue
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        center_x, center_y = x + w // 2, y + h // 2
        text_coords[text] = (center_x, center_y)

    # 返回识别结果及对应的中心坐标
    print(text_coords)
    return text_coords


def video_to_frames0(video_path, output_path):
    # 如果文件夹存在，则清空文件夹；否则创建一个新的空文件夹
    if os.path.exists(output_path):
        shutil.rmtree(output_path)  # 递归删除文件夹中的所有文件
    os.mkdir(output_path)  # 创建一个新的空文件夹
    # 读取视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频帧率和总帧数
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 读取视频帧并输出为单帧图片
    for i in range(total_frames):
        # 读取一帧视频
        ret, frame = cap.read()
        if ret:
            # 写入单帧图片
            cv2.imwrite(output_path + f'frame_{i}.jpg', frame)
        else:
            break

    # 释放视频和输出文件系统
    cap.release()
    cv2.destroyAllWindows()


def extract_frames(video_path, output_dir, fps=1):
    """
    将输入的视频文件转换为单独的图像文件
    :param video_path: 输入视频的文件路径
    :param output_dir: 图像输出目录
    :param fps: 每秒钟多少帧
    """
    # 执行命令
    cmd = "ffmpeg -i {} -vf fps={} {}/frame_%d.jpg".format(video_path, fps, output_dir)
    subprocess.run(cmd, shell=True, check=True)


def image_timestamp(filePath):
    """下载睿博士截图，识别图片中的时间OSD，并输出时间戳"""
    result = []
    for fileName in os.listdir(filePath):
        url = filePath + fileName
        text_list = recognize_text(url, (0, 0.089, 0, 0.31)).keys()
        text_list = list(text_list)
        time_text = text_list[0] + ' ' +text_list[1]

        time_stamp = ntp_util.str_time_to_timestamp(time_text)
        result.append(time_stamp)
    return result


def color_check(startPoint, endPoint, precision=10):
    """判断SD回放进度条颜色，返回字典"""
    pixel_info = dict()
    for x in range(startPoint, endPoint, precision):
        pixel_info[(x, 80)] = get_pixel_color('cropped.jpg', (x, 80))
    return pixel_info


def get_pixel_color(image_path, position):
    """获取指定坐标的像素颜色"""
    # 读取图片
    img = cv2.imread(image_path)
    # 获取指定坐标的像素颜色值
    x, y = position
    color_bgr = img[y, x]
    # 将 BGR 颜色值转换成 RGB 颜色值
    color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
    # 返回像素颜色值（RGB格式）
    return color_rgb



if __name__ == '__main__':
    # # url = 'C:\\Users\\Administrator\\Desktop\\video\\screenshot\\IOTDBB-065896-UXLYD_2023_06_07_17_43_01_CH_1_imageNametest_dev.jpg'
    # # url = 'C:\\Users\\Administrator\\Desktop\\video\\videos\\9E52C023-E5F3-4f81-BFB3-D0CEB65AEC4B.png'
    # # # print(recognize_text(url, (0, 0.089, 0, 0.31)))
    # # print(recognize_text(url, (0, 1, 0, 1)))
    video_path = 'C:\\Users\\Administrator\\Desktop\\20230819075253-20230819080256.mp4'
    output_path = 'C:\\Users\\Administrator\\Desktop\\video\\videos\\'
    # # print(extract_frames(video_path, output_path))
    # # os.system(xrs_adb.command_dict['下载睿博士截图'])
    # # time_stamp_list = image_timestamp(environment_variable.adb_download +'screenshot\\')
    # # print(time_stamp_list)
    # text_coords = recognize_text('C:\\Users\\Administrator\\Desktop\\video\\Screenshots\\1.jpg', (0.44, 0.52, 0, 1))
    # pixel_info = dict()
    # for x in range(0,1080,10):
    #     pixel_info[(x, 80)] = get_pixel_color('cropped.jpg', (x, 80))
    #
    # print(pixel_info)
    extract_frames(video_path, output_path, fps=1)