import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import sensor_msgs.msg as sensor_msgs
from example_interfaces.srv import SetBool


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            sensor_msgs.PointCloud2,
            'pub_pcd',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(sensor_msgs.PointCloud2, 'pcd', 10)
        self.srv = self.create_service(SetBool, 'trigger', self.trigger)

    def trigger(self, request, response):
        self.pub_msg = self.save_data
        response.success = True
        response.message = "trigger"
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        return response

    def listener_callback(self, msg):
        self.save_data = msg

    def timer_callback(self):
        #self.pcd = point_cloud(self.pub_msg, 'pcd')
        self.publisher_.publish(self.pub_msg)
    

#def point_cloud(points, parent_frame):
#    """ Creates a point cloud message.
#    Args:
#        points: Nx3 array of xyz positions.
#        parent_frame: frame in which the point cloud is defined
#    Returns:
#        sensor_msgs/PointCloud2 message
#    Code source:
#        https://gist.github.com/pgorczak/5c717baa44479fa064eb8d33ea4587e0
#    """
#    ros_dtype = sensor_msgs.PointField.FLOAT32
#    dtype = np.float32
#    itemsize = np.dtype(dtype).itemsize  # A 32-bit float takes 4 bytes.
#
#    data = points.astype(dtype).tobytes()
#    fields = [sensor_msgs.PointField(
#        name=n, offset=i * itemsize, datatype=ros_dtype, count=1)
#        for i, n in enumerate('xyz')]
#    header = std_msgs.Header(frame_id=parent_frame)
#
#    return sensor_msgs.PointCloud2(
#        header=header,
#        height=1,
#        width=points.shape[0],
#        is_dense=False,
#        is_bigendian=False,
#        fields=fields,
#        point_step=(itemsize * 3),  # Every point consists of three float32s.
#        row_step=(itemsize * 3 * points.shape[0]),
#        data=data
#    )

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
