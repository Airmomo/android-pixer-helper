# android-pixer-helper
基于PyQt5和android-auto-helper开发的安卓图色助手，是一个模拟器截图、图色记录辅助工具
# 运行
部署完成后，启动模拟器设备，直接运行`main.py`
# 功能
- 打开本地图片/加载模拟器截屏
- 保存区域截图
- 像素点坐标、RGB色彩查看和快捷记录
- 多点找色字符串生成及复制
- 更多功能可以自己Fork本项目进行添加
# 项目优缺点
## 优点
- 跨平台：支持windows/mac/linux，只需选择对应系统的adb初始化，不需要修改源码
- 自动兼容设备分辨率：对于不同分辨率的设备，可以自动进行兼容，无需修改坐标数据
## 缺点
- 本项目在Mac平台开发，Windows/Linux平台暂未测试
- 由于adb调试桥的事件操作命令最高只支持到安卓7.0（api24），如果安卓系统版本过高，可能得不到预期的效果
# 开发环境
- 操作系统：mac系统（M1 Pro）
- Python：python 3.9
- 安卓设备：安卓模拟器（Android Studio Virtual Device）
- 安卓系统：Android 7.0 (api24、arm64)
# 项目依赖
可以通过命令`pip install -r requirements.txt`来安装以下依赖
- easyocr==1.6.2
- imutils==0.5.4
- numpy==1.21.5
- opencv_python==4.6.0.66
- Pillow==9.2.0
- PyQt5==5.15.7
**注意：PyQt5在Mac平台安装复杂、以及对Python3.7以上都不太兼容，直接通过pip安装可能会报错，需要自行搜索正确的安装方法，这里就不冗述了**
# 跨平台实现
**本项目与安卓设备的交互主要通过adb实现，只需要在初始化安卓对象时选择对应系统的adb文件即可**
adb文件存在目录`tools/platform-tools-*`下，也可以自行到官网下载->[传送门](https://developer.android.com/studio/command-line/adb)
- platform-tools-linux
- platform-tools-mac
- platform-tools-windows

**如果使用的是第三方的安卓模拟器，建议复制其模拟器源文件目录下的adb文件来调用**