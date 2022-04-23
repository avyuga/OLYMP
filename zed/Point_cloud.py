import numpy as np
import pyzed.sl as sl
import open3d as o3d
import matplotlib.pyplot as plt

def get_point_cloud(camera: sl.Camera):
    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.FILL

    err = camera.grab(runtime)
    if err == sl.ERROR_CODE.SUCCESS:
        print("Saving Point Cloud...")
        tmp = sl.Mat()
        camera.retrieve_measure(tmp, sl.MEASURE.XYZRGBA, sl.MEM.CPU)
        tmp.get_data()
        saved = (tmp.write("files/test.ply") == sl.ERROR_CODE.SUCCESS)
        if saved:
            print("Done")
        else:
            print("Failed... Please check that you have permissions to write on disk")

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                      width=720, height=540)

def process(cloud_path):
    cloud = o3d.io.read_point_cloud(cloud_path)
    print(type(cloud))
    # fixme почему оно так? мб ошибка в классах
    # <class 'open3d.cpu.pybind.geometry.PointCloud'> != <open3d.geometry.PointCloud>
    cloud = o3d.geometry.PointCloud(cloud)

    cloud = o3d.geometry.PointCloud(cloud.voxel_down_sample(voxel_size=0.005))
    colors = np.asarray(cloud.colors)
    cloud = cloud.select_by_index(np.where(colors[:, 0] > 0.7)[0])
    o3d.visualization.draw_geometries([cloud], width=720, height=540)

    cloud = o3d.geometry.PointCloud(cloud)
    # print("Statistical outlier removal")
    # cloud_clean, ind = cloud.remove_statistical_outlier(nb_neighbors=10, std_ratio=10)
    print("Radius outlier removal")
    cloud_clean, ind = cloud.remove_radius_outlier(nb_points=30, radius=0.04)
    display_inlier_outlier(cloud, ind)

    o3d.visualization.draw_geometries([cloud_clean], width=720, height=540)

    labels = np.array(
        cloud_clean.cluster_dbscan(eps=0.1, min_points=10, print_progress=True))
    max_label = labels.max()
    print("Cloud has %d clusters" % (max_label + 1))

    # выбираем цвета для выделения кластеров
    colour_map = plt.get_cmap("tab20")
    colors = colour_map(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0  # если шум, то labels=-1
    cloud_clean.colors = o3d.utility.Vector3dVector(colors[:, :3])
    o3d.visualization.draw_geometries([cloud_clean], width=720, height=540)


