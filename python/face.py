import os
import face_recognition
import cv2

gril_names=['Gril','gril']

# 读取到数据库中的人名和面部特征
    # 1.准备工作
face_databases_dir='face_databases'
user_names=[] # 存用户名
user_faces_encodings=[] # 存用户面部特征向量

    # 2.得到face_databases_dir文件夹下所有的文件名
files=os.listdir(face_databases_dir)

    # 2.2循环读取文件名进行进一步的处理
for image_shot_name in files:

    # 截取文件前面部分用作name
    user_name,_=os.path.splitext(image_shot_name)
    user_names.append(user_name)

    # 读取文件面部信息存储到user_faces_encodings 中
    image_file_name=os.path.join(face_databases_dir,image_shot_name)
    image_file=face_recognition.load_image_file(image_file_name)
    face_encodin=face_recognition.face_encodings(image_file)[0]
    user_faces_encodings.append(face_encodin)

# 1.打开摄像头，获取摄像头对象
vide_capture = cv2.VideoCapture(0)  # 0代表打开第一个摄像头

# 2.循环不停的去获取摄像头拍摄到的画面 并做处理
while True:

    # 2.1获取摄像头拍摄到的画面
    ret, frame = vide_capture.read()  # frame 是摄像头拍摄的画面

    # 2.2从拍摄到的画面中提取人的脸所在区域
    face_locations = face_recognition.face_locations(frame)

    # 2.21从所有人的头像所在区域提取脸部特征
    face_encodings=face_recognition.face_encodings(frame,face_locations)

    # 2.22定义用于存储拍摄到的用户姓名和列表
    names = []
    # 遍历face_encodings，和之前数据库中面部特征做匹配
    for face_encoding in face_encodings:
        # compare_faces(['面部特征1', '面部特征2', '面部特征3' ... ], 未知的面部特征)
        # compare_faces返回结果
        # 假如 未知的面部特征 和 面部特征1 匹配， 和 面部特征2 面部特征3 不匹配
        # [True, False, False]

        # 假如 未知的面部特征 和 面部特征2 匹配， 和 面部特征1 面部特征3 不匹配
        # [False, True, False ]

        matchs = face_recognition.compare_faces(user_faces_encodings, face_encoding)
        # user_names
        # ['第一个人的姓名'，'第二个人的姓名'， '第三个人的姓名' ...]
        name = "UnKnown"

        for index,is_match in enumerate(matchs):

            if is_match:
                name=user_names[index]
                break

        names.append(name)


    # 2.3循环遍历人的脸部所在区域 并画框
    for (top, right, bottom, left),name in zip(face_locations,names):

        color=(0, 255, 0)
        if name in gril_names:
            color=(0, 0, 255)
        # 人像所在区域画框
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), (1))

        font=cv2.FONT_HERSHEY_DUPLEX

        cv2.putText(frame,name,(left,top-10),font,0.5,(0, 255, 0),1)


    # 2.4通过OpenCV把画面展现出来
    cv2.imshow('video', frame)

    # 2.5设定按q退出while循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 3.退出程序的时候 释放摄像头或其他资源
vide_capture.release()
cv2.destroyWindow()