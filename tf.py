import rclpy
from rclpy.node import Node
import tf2_ros
import geometry_msgs.msg

class TfBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        # 定期的にTFをブロードキャスト
        self.timer = self.create_timer(0.1, self.broadcast_transform)

    def broadcast_transform(self):
        t = geometry_msgs.msg.TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'pcd'
        
        t.transform.translation.x = 0.5
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.5
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    broadcaster = TfBroadcaster()
    rclpy.spin(broadcaster)
    broadcaster.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

