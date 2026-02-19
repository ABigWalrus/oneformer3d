import numpy as np
import open3d as o3d

vert_npy = np.load("data/scannet/scannet_instance_data/scene0217_00_vert.npy")
sem_label = np.load("data/scannet/scannet_instance_data/scene0217_00_sem_label.npy")

# print(sem_label.shape)

def save_point_cloud(points, labels, file_path):

    pc = o3d.t.geometry.PointCloud()
    pc.point["positions"] = o3d.core.Tensor(points[:, :3])
    pc.point["colors"] = o3d.core.Tensor(points[:, 3:]/255.0)
    pc.point["labels"] = o3d.core.Tensor(labels.reshape(-1, 1).astype(np.uint8))
    o3d.t.io.write_point_cloud(file_path, pc)
    
    
save_point_cloud(vert_npy, sem_label, "0217_00_noisy_labels.ply")