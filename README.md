# 摄影测量与计算机视觉课程作业

**课程教师：** 谢东海  
**学生姓名：** 赵若凡

---

## 📋 项目简介

本仓库包含摄影测量与计算机视觉课程的实验代码，涵盖图像处理、特征检测、相机标定等计算机视觉基础算法的实现。所有代码均使用 Python 和 Jupyter Notebook 编写。

---

## 📂 项目结构

```
cvclass-Zhao-Ruofan/
├── photos/                          # 实验图像数据
├── DSC00480.JPG                     # 测试图像1
├── DSC00481.JPG                     # 测试图像2
├── Harris赵若凡.ipynb                # Harris角点检测实验
├── Laplace赵若凡.ipynb               # Laplace边缘检测实验
├── SIFT点定位与可视化_赵若凡.ipynb      # SIFT特征点检测与可视化
├── camera_calibration.npz           # 相机标定参数数据
├── canny赵若凡.ipynb                 # Canny边缘检测实验
├── sobel赵若凡.ipynb                 # Sobel边缘检测实验
├── 本质矩阵赵若凡.ipynb               # 本质矩阵计算实验
├── 特征点匹配赵若凡.ipynb             # 特征点匹配实验
└── 相机标定函数赵若凡.ipynb           # 相机标定实验
```

---

## 🔬 实验内容

### 1. 边缘检测算法
- **Sobel边缘检测** (`sobel赵若凡.ipynb`)
  - 实现Sobel算子进行图像边缘检测
  - 水平和垂直方向梯度计算
  
- **Laplace边缘检测** (`Laplace赵若凡.ipynb`)
  - 基于二阶导数的边缘检测
  - Laplacian算子的实现与应用

- **Canny边缘检测** (`canny赵若凡.ipynb`)
  - 多级边缘检测算法
  - 包含高斯滤波、梯度计算、非极大值抑制、双阈值检测

### 2. 特征检测与匹配
- **Harris角点检测** (`Harris赵若凡.ipynb`)
  - Harris角点检测算法实现
  - 角点响应函数计算与可视化

- **SIFT特征检测** (`SIFT点定位与可视化_赵若凡.ipynb`)
  - 尺度不变特征变换(SIFT)算法
  - 特征点检测与描述子生成
  - 特征点可视化

- **特征点匹配** (`特征点匹配赵若凡.ipynb`)
  - 基于特征描述子的图像匹配
  - 匹配算法实现与结果可视化

### 3. 相机标定与几何
- **相机标定** (`相机标定函数赵若凡.ipynb`)
  - 相机内参和外参标定
  - 畸变参数估计
  - 标定结果保存在 `camera_calibration.npz`

- **本质矩阵计算** (`本质矩阵赵若凡.ipynb`)
  - 双视图几何中本质矩阵的估计
  - 相机相对位姿恢复

---

## 🛠️ 技术栈

- **编程语言：** Python 3.x
- **主要库：**
  - OpenCV - 计算机视觉库
  - NumPy - 数值计算
  - Matplotlib - 数据可视化
  - Jupyter Notebook - 交互式开发环境

---

## 🚀 运行环境

### 环境要求
```bash
Python >= 3.7
opencv-python >= 4.0
numpy >= 1.19
matplotlib >= 3.0
jupyter notebook
```

### 安装依赖
```bash
pip install opencv-python numpy matplotlib jupyter
```

### 运行方式
1. 克隆仓库
```bash
git clone https://github.com/Halogenname/cvclass-Zhao-Ruofan.git
cd cvclass-Zhao-Ruofan
```

2. 启动 Jupyter Notebook
```bash
jupyter notebook
```

3. 在浏览器中打开对应的 `.ipynb` 文件运行实验

---

## 📊 实验数据

- `photos/` 文件夹包含实验用的图像数据
- `DSC00480.JPG` 和 `DSC00481.JPG` 为立体视觉实验的图像对
- `camera_calibration.npz` 包含相机标定后的参数矩阵

---

## 📝 笔记说明

每个 Notebook 文件包含：
- 算法原理说明
- 完整的代码实现
- 实验结果可视化
- 参数调整与分析

---

## 👨‍🎓 作者信息

- **姓名：** 赵若凡
- **课程：** 摄影测量与计算机视觉
- **指导教师：** 谢东海

---

## 📄 许可证

本项目仅用于课程学习和研究目的。

---

## 🙏 致谢

感谢谢东海老师的悉心指导！