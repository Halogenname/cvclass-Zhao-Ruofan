import bagpy
from bagpy import bagreader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import struct

print("=" * 60)
print("激光雷达点云数据处理")
print("=" * 60)

# 读取 bag 文件
bag = bagreader('rotation.bag')

# 读取点云数据
points_csv = bag.message_by_topic('/points_raw')
df = pd.read_csv(points_csv)

print(f"\n✅ 读取到 {len(df)} 帧点云数据")
print(f"point_step: {df['point_step'].iloc[0]}")  # 每个点的字节数
print(f"width: {df['width'].iloc[0]}")  # 点数

def parse_pointcloud2(data_bytes, point_step, width):
    """解析 PointCloud2 二进制数据"""
    # 移除 b' 和 ' 以及转义字符
    if isinstance(data_bytes, bytes):
        data = data_bytes
    else:
        # 从字符串解析
        data_str = str(data_bytes)
        if data_str.startswith("b'") or data_str.startswith('b"'):
            data_str = data_str[2:-1]
        # 使用 eval 来正确解析转义序列
        try:
            data = eval(f"b'{data_str}'")
        except:
            return None
    
    points = []
    # 每个点通常是 16 字节: x(4) y(4) z(4) intensity(4)
    for i in range(width):
        offset = i * point_step
        if offset + 12 <= len(data):
            # 解析 x, y, z (float32)
            x = struct.unpack('f', data[offset:offset+4])[0]
            y = struct.unpack('f', data[offset+4:offset+8])[0]
            z = struct.unpack('f', data[offset+8:offset+12])[0]
            
            # 过滤无效值
            if not (np.isnan(x) or np.isnan(y) or np.isnan(z) or 
                    np.isinf(x) or np.isinf(y) or np.isinf(z)):
                points.append([x, y, z])
    
    return np.array(points) if points else None

# 解析所有帧
print("\n开始解析点云数据...")
all_frames = []
for idx, row in df.iterrows():
    points = parse_pointcloud2(
        row['data'], 
        int(row['point_step']), 
        int(row['width'])
    )
    if points is not None and len(points) > 0:
        all_frames.append(points)
        if (idx + 1) % 50 == 0:
            print(f"  已解析 {idx + 1}/{len(df)} 帧...")

print(f"\n✅ 成功解析 {len(all_frames)} 帧点云")
if len(all_frames) > 0:
    print(f"   平均每帧 {np.mean([len(f) for f in all_frames]):.0f} 个点")
    print(f"   总共 {sum([len(f) for f in all_frames])} 个点")

# 询问用户选择
print("\n" + "=" * 60)
print("选择处理方式:")
print("  1. 保存为 PLY 文件 (用 MeshLab 查看)")
print("  2. Python 动画可视化")
print("  3. 同时进行")
print("=" * 60)
choice = input("请输入选项 (1/2/3): ").strip()

# 方案1：保存为 PLY 文件
if choice in ['1', '3']:
    print("\n正在保存 PLY 文件...")
    
    # 保存每一帧
    for idx, points in enumerate(all_frames[:10]):  # 先保存前10帧
        filename = f'pointcloud_frame_{idx:04d}.ply'
        with open(filename, 'w') as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(points)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write("end_header\n")
            for p in points:
                f.write(f"{p[0]} {p[1]} {p[2]}\n")
        print(f"  ✅ 保存: {filename}")
    
    # 合并所有点保存为一个文件
    all_points = np.vstack(all_frames)
    filename = 'pointcloud_all.ply'
    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(all_points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        for p in all_points:
            f.write(f"{p[0]} {p[1]} {p[2]}\n")
    print(f"\n  ✅ 保存合并文件: {filename}")
    print(f"  📊 包含 {len(all_points)} 个点")
    print("\n👉 现在可以用 MeshLab 打开这些 .ply 文件！")

# 方案2：Python 可视化
if choice in ['2', '3']:
    print("\n开始 Python 可视化...")
    
    # 创建图形
    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)
    fig.suptitle('激光雷达点云数据可视化 (rotation.bag)', 
                fontsize=16, weight='bold')
    
    # 采样显示（太多帧会很慢）
    display_frames = all_frames[::max(1, len(all_frames)//50)]  # 最多显示50帧
    print(f"显示 {len(display_frames)} 帧动画")
    
    def update(frame_idx):
        points = display_frames[frame_idx]
        x, y, z = points[:, 0], points[:, 1], points[:, 2]
        
        # 3D 视图
        ax1.clear()
        scatter = ax1.scatter(x, y, z, c=z, cmap='viridis', s=0.5)
        ax1.set_xlabel('X (米)')
        ax1.set_ylabel('Y (米)')
        ax1.set_zlabel('Z (米)')
        ax1.set_title(f'3D 点云 (帧 {frame_idx+1}/{len(display_frames)})')
        ax1.view_init(elev=20, azim=45)
        
        # 俯视图 (X-Y)
        ax2.clear()
        ax2.scatter(x, y, c=z, cmap='viridis', s=1)
        ax2.plot(0, 0, 'ro', markersize=8, label='雷达')
        ax2.set_xlabel('X (米)')
        ax2.set_ylabel('Y (米)')
        ax2.set_title('俯视图 (X-Y)')
        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 侧视图 (X-Z)
        ax3.clear()
        ax3.scatter(x, z, c=z, cmap='viridis', s=1)
        ax3.set_xlabel('X (米)')
        ax3.set_ylabel('Z (米)')
        ax3.set_title('侧视图 (X-Z)')
        ax3.grid(True, alpha=0.3)
        
        # 统一坐标范围
        max_range = max(np.abs(x).max(), np.abs(y).max(), np.abs(z).max())
        ax1.set_xlim(-max_range, max_range)
        ax1.set_ylim(-max_range, max_range)
        ax1.set_zlim(-max_range, max_range)
    
    # 创建动画
    if len(display_frames) > 1:
        anim = FuncAnimation(fig, update, frames=len(display_frames),
                           interval=100, repeat=True)
    else:
        update(0)
    
    plt.tight_layout()
    plt.show()

print("\n程序结束")