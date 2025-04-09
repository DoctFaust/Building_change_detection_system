# 基于通道注意力UNet++模型和PyQt5的建筑物变化检测系统

## 项目说明

本项目是一个 **基于通道注意力UNet++模型的建筑物变化检测系统**。系统自带的UNet++模型使用 `PyTorch` 进行搭建和训练，图形界面使用 `PyQt5` 开发，包管理和部署工具分别使用 `UV` 和 `PyInstaller` 。

应用程序能够根据用户上传的两幅不同时间拍摄的同一区域地表彩色影像，分析建筑物区域变化情况，输出建筑物区域变化二值图像并保存到本地。系统允许用户使用我们已经训练好的UNet++模型进行变化检测（默认模式），或使用用户本地的模型参数（以 `.pth`文件形式上传）进行分析。

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

_注：用户可以直接使用打包好的 `main.exe` 来使用本系统。不过请注意，如果直接使用，而非从源码构建，系统中的 **“默认模型”** 这一模式无法使用。这一问题的解决办法是，用户可以在系统中使用 **“自定义模型”** 模式，在文件管理器中导航到项目源码文件夹下的 `model/model.pth` 这一文件路径，这个模型参数文件正是系统默认使用的模型参数。用户只需选用该模型来进行分析，即可获得和“默认模型”模式下完全一致的结果。_

从项目源码构建二进制文件的步骤如下：

### 1. 获取项目文件

在 `Powershell/Bash/CMD` 等 `Shell` 中输入：

`git clone https://github.com/DoctFaust/Building_change_detection_system.git {指定的文件夹路径}`

或使用网盘下载，网盘链接为：

`https://pan.baidu.com/s/1XBup7v6yHH2rK-ZOinPf0g 提取码: 1053`

### 2. 虚拟环境创建和激活

在 `Powershell/Bash/CMD` 等 `Shell` 中导航到第一步中指定的存储项目文件的文件夹，例如：

`cd C:/Users/admin/Building_change_detection_system`

然后在此目录下进行虚拟环境的创建和激活。这里以我们开发过程中使用工具 `uv` 的操作步骤为例，它能够方便地进行Python项目包管理和虚拟环境管理。

**⚠️⚠️⚠️注意： 本项目使用的pip和依赖包版本均与Python 3.9配套，因此用户需要安装Python 3.9版本。如果在Windows系统下进行构建，还需要手动配置Python 3.9的系统环境变量，然后进行下一步操作。**

首先使用 `pip` 下载 `uv` ：

`pip install uv`

然后使用 `uv` 创建虚拟环境，注意在后面指定使用的 `Python` 解释器版本，避免使用错误版本：

`uv venv venv1 --python 3.9 (venv1可替换为其它名称)`

最后激活虚拟环境 `venv1` ：

`venv1/Scripts/activate`

### 3. 安装依赖和构建工具

在激活的虚拟环境下，使用 `pip` 根据项目的 `requirements.txt` 安装依赖：

`uv pip install -r requirements.txt`

安装完成后再继续安装构建工具 `build` 和 `pyinstaller`：

`uv pip install pyinstaller`

### 4. 构建二进制文件

使用 `pyinstaller` 构建 `main.exe`：

`pyinstaller --onefile --windowed src/main.py`

构建完成的 `main.exe` 可执行文件位于项目根目录的 `dist` 文件夹下，用户点击打开即可使用。