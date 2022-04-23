from zed.Cyber_vision import cyber_vision, get_image
from zed.Point_cloud import get_point_cloud, process
import cv2
import open3d as o3d
import pyzed.sl as sl

'''initiating camera'''
# zed = sl.Camera()
# init_params = sl.InitParameters()
# init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
# init_params.camera_fps = 30
#
# init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
# init_params.coordinate_units = sl.UNIT.MILLIMETER
#
# err = zed.open(init_params)
# if err != sl.ERROR_CODE.SUCCESS:
#     print(err)
#     zed.close()
#     exit(1)


''' Getting point cloud'''
# get_point_cloud(zed)
# cloud = o3d.io.read_point_cloud("files/test.ply")
# o3d.visualization.draw_geometries([cloud])

# process(r'C:\Users\Anastasia\PycharmProjects\OLYMP\files\test.ply')
process(r'C:\Users\Anastasia\PycharmProjects\nti_irs_2021\zed_camera\cloud2.ply')

# img = get_image(zed)
# cyber_vision(img)

'''Close the camera'''
# zed.close()
