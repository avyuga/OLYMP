import pyzed.sl as sl

def set_camera_parameters(camera: sl.Camera):
    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode (default fps: 60)
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP  # Use a right-handed Y-up coordinate system
    init_params.coordinate_units = sl.UNIT.METER  # Set units in meters

    mapping_parameters = sl.SpatialMappingParameters()
    mapping_parameters.range_meter = 1  # Set maximum depth mapping range to 1m
    # mapping_parameters.range_meter = mapping_parameters.get_range_preset(sl.MAPPING_RANGE.NEAR)
    # Set mapping with mesh output
    # mapping_parameters.map_type = sl.SPATIAL_MAP_TYPE.MESH
    # or select point cloud output
    mapping_parameters.map_type = sl.SPATIAL_MAP_TYPE.FUSED_POINT_CLOUD
    return mapping_parameters

def save(camera: sl.Camera, mesh: sl.Mesh):
    print("Extracting Point Cloud...\n")
    err = camera.extract_whole_spatial_map(mesh)
    print(repr(err))
    # print("Filtering Mesh...\n")
    # py_mesh.filter(sl.MeshFilterParameters())  # Filter the mesh (remove unnecessary vertices and faces)
    print("Saving Point Cloud...\n")
    mesh.save("files/mesh.obj")

def disable(camera: sl.Camera):
    # Disable spatial mapping, positional tracking and close the camera
    camera.disable_spatial_mapping()
    camera.disable_tracking()
    camera.close()


def grab_once(camera: sl.Camera):

    # Enable tracking and mapping
    tracking_parameters = sl.TrackingParameters()
    camera.enable_tracking(tracking_parameters)

    mapping_parameters = set_camera_parameters(camera)
    camera.enable_spatial_mapping(mapping_parameters)

    mesh = sl.Mesh()  # Create a mesh object
    timer = 0

    # Grab 500 frames and stop
    while timer < 500:
        if camera.grab() == sl.ERROR_CODE.SUCCESS:
            # When grab() = SUCCESS, a new image, depth and pose is available.
            # Spatial mapping automatically ingests the new data to build the mesh.
            timer += 1

    save(camera, mesh)
    disable(camera)

def grab(camera: sl.Camera):

    # Enable tracking and mapping
    tracking_parameters = sl.TrackingParameters()
    camera.enable_tracking(tracking_parameters)

    mapping_parameters = set_camera_parameters(camera)
    camera.enable_spatial_mapping(mapping_parameters)

    # Request an updated spatial map every 0.5s
    mesh = sl.Mesh()  # Create a Mesh object or FusedPointCloud
    timer = 0
    print("Start extracting data...")
    time = 20
    while 1:
        if camera.grab() == sl.ERROR_CODE.SUCCESS:

            # Request an update of the spatial map every 30 frames (0.5s in HD720 mode)
            if timer % 30 == 0:
                camera.request_spatial_map_async()
            if timer % 60 == 0:
                print(f"{timer%60 + 1} out of {time} seconds passed...")

            # Retrieve spatial_map when ready
            if camera.get_spatial_map_request_status_async() == sl.ERROR_CODE.SUCCESS and timer > 0:
                camera.retrieve_spatial_map_async(mesh)

            timer += 1
        # 60 frames per 1 second
        if timer == 60 * time: break

    save(camera, mesh)
    disable(camera)
