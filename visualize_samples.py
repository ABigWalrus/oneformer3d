import numpy as np
import open3d as o3d

vert_npy = np.load("data/scannet/scannet_instance_data/scene0568_00_sp_label.npy")
# sem_label = np.load("data/scannet/scannet_instance_data/scene0568_00_sem_label.npy")

# print(sem_label.shape)
print(vert_npy.shape)
print(vert_npy)

# def save_point_cloud(points, file_path):

#     pc = o3d.t.geometry.PointCloud()
#     pc.point["positions"] = o3d.core.Tensor(points[:, :3])
#     pc.point["colors"] = o3d.core.Tensor(points[:, 3:]/255.0)
#     # pc.point["labels"] = o3d.core.Tensor(labels.reshape(-1, 1).astype(np.uint8))
#     o3d.t.io.write_point_cloud(file_path, pc)
    
    
# save_point_cloud(vert_npy, "sp_labels_pc.ply")