# 基于通道注意力UNet++模型和PyQt5的建筑物变化检测系统

## 项目说明

本项目是一个基于通道注意力UNet++模型的建筑物变化检测系统。系统自带的UNet++模型使用 PyTorch 进行搭建和训练，图形界面使用 PyQt5 开发，包管理和部署工具分别使用 UV 和 PyInstaller 。

应用程序能够根据用户上传的两幅不同时间拍摄的同一区域地表彩色影像，分析建筑物区域变化情况，输出建筑物区域变化二值图像并保存到本地。系统允许用户使用我们已经训练好的UNet++模型进行变化检测（默认模式），或使用用户本地的模型参数（以.pth文件形式上传）进行分析。

项目的文件结构如下：

##### [ building_change_detection ]
- icon               // 应用需要使用到的图标
- model              // 默认模型参数文件存放的位置
   - model.pth       // 默认选择的UNet++模型参数文件
- src                // 源代码存放位置
   - models          // 负责 **模型预测** 的源代码
   - ui              // 负责控制 **GUI界面样式** 和 **界面与模型交互** 的源代码
- test_image         // 测试图片存放位置
   - after           // 变化前图像
   - before          // 变化后图像
   - label           // 标签图像，用于评价检测效果

___

## 部署方法

### 1. 获取项目文件

在 CMD/Powershell/Bash 等 Shell 中输入：

`git clone https://github.com/DoctFaust/Building_change_detection_system.git {指定的文件夹路径}`

或使用网盘下载，网盘链接为：

`abcdefg`

### 2. 执行部署脚本

在 CMD/Powershell/Bash 等 Shell 中导航到第一步中指定的存储项目文件的文件夹，例如：

`cd C:/Users/admin/Building_change_detection_system`

然后执行dist文件夹下的部署脚本：

`./dist/deploy_app.ps1`

执行完毕后，在dist文件夹下可以找到main.exe，点击打开即可使用。