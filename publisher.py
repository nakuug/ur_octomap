import rclpy
from rclpy.node import Node
import sensor_msgs.msg as sensor_msgs
import std_msgs.msg as std_msgs
import open3d

import numpy as np


class PCDPublisher(Node):

    def __init__(self):
        super().__init__('pcd_publisher_node')
        pcd = open3d.io.read_point_cloud("bun.pcd")
        self.points = np.array(pcd.points)
        #self.points = np.array([[1, 1, 1]])
        print(self.points.shape)
        self.pcd_publisher = self.create_publisher(sensor_msgs.PointCloud2, 'pub_pcd', 10)
        timer_period = 1/ 30.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.pcd = point_cloud(self.points, 'pcd')
        self.pcd_publisher.publish(self.pcd)


def point_cloud(points, parent_frame):
    """ Creates a point cloud message.
    Args:
        points: Nx3 array of xyz positions.
        parent_frame: frame in which the point cloud is defined
    Returns:
        sensor_msgs/PointCloud2 message
    Code source:
        https://gist.github.com/pgorczak/5c717baa44479fa064eb8d33ea4587e0
    """
    ros_dtype = sensor_msgs.PointField.FLOAT32
    dtype = np.float32
    itemsize = np.dtype(dtype).itemsize  # A 32-bit float takes 4 bytes.

    data = points.astype(dtype).tobytes()
    fields = [sensor_msgs.PointField(
        name=n, offset=i * itemsize, datatype=ros_dtype, count=1)
        for i, n in enumerate('xyz')]
    header = std_msgs.Header(frame_id=parent_frame)

    return sensor_msgs.PointCloud2(
        header=header,
        height=1,
        width=points.shape[0],
        is_dense=False,
        is_bigendian=False,
        fields=fields,
        point_step=(itemsize * 3),  # Every point consists of three float32s.
        row_step=(itemsize * 3 * points.shape[0]),
        data=data
    )


def main(args=None):
    rclpy.init(args=args)
    pcd_publisher = PCDPublisher()
    rclpy.spin(pcd_publisher)


if __name__ == '__main__':
    main()
