import rclpy
from rclpy.node import Node
from xela_server_ros2.msg import SensStream
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D 


class DiffPrinter(Node):
    def __init__(self):
        super().__init__('z_diff_printer')
        self.subscription = self.create_subscription(
            SensStream,
            '/xServTopic',
            self.callback,
            10
        )
        self.prev_x_values = None
        self.prev_y_values = None
        self.prev_z_values = None

        self.cumulative_dx = [0.0]*16
        self.cumulative_dy = [0.0]*16
        self.cumulative_dz = [0.0]*16

        ######## 시간 변화 2D 시각화 코드 ##########

        self.cumulative_x_history = [[] for _ in range(16)]  # 각 센서 x값 히스토리
        self.cumulative_y_history = [[] for _ in range(16)]  # 각 센서 y값 히스토리  
        self.cumulative_z_history = [[] for _ in range(16)]  # 각 센서 Z값 히스토리

        # 실시간 선 그래프 설정
        self.fig_x, self.ax_x = plt.subplots()
        self.lines_x = [self.ax_x.plot([], [], label=f"Sensor {i}", linewidth=1)[0] for i in range(16)]
        self.ax_x.set_title("Z Value over Time (16 Sensors)")
        self.ax_x.set_xlabel("Time Step")
        self.ax_x.set_ylabel("Z Value")
        self.ax_x.grid(True)
        self.ax_x.legend(loc='upper right', fontsize='x-small')

        # self.fig_y, self.ax_y = plt.subplots()
        # self.lines_y = [self.ax_y.plot([], [], label=f"Sensor {i}", linewidth=1)[0] for i in range(16)]
        # self.ax_y.set_title("Z Value over Time (16 Sensors)")
        # self.ax_y.set_xlabel("Time Step")
        # self.ax_y.set_ylabel("Z Value")
        # self.ax_y.grid(True)
        # self.ax_y.legend(loc='upper right', fontsize='x-small')

        self.fig_z, self.ax_z = plt.subplots()
        self.lines_z = [self.ax_z.plot([], [], label=f"Sensor {i}", linewidth=1)[0] for i in range(16)]
        self.ax_z.set_title("Z Value over Time (16 Sensors)")
        self.ax_z.set_xlabel("Time Step")
        self.ax_z.set_ylabel("Z Value")
        self.ax_z.grid(True)
        self.ax_z.legend(loc='upper right', fontsize='x-small')

        plt.ion()
        plt.show()

        self.get_logger().info('DiffPrinter 노드 실행 중 (/xServTopic 구독).')


    def callback(self, msg):
        try:
            # 첫 번째 센서 기준 taxel 리스트
            x_values = [taxel.x for taxel in msg.sensors[0].taxels]
            y_values = [taxel.y for taxel in msg.sensors[0].taxels]
            z_values = [taxel.z for taxel in msg.sensors[0].taxels]


            if self.prev_x_values is not None:
                diffs_x = [curr - prev for curr, prev in zip(x_values, self.prev_x_values)]

                for i in range(16):
                    self.cumulative_dx[i] += diffs_x[i]
                    self.cumulative_x_history[i].append(self.cumulative_dx[i])
                    if len(self.cumulative_x_history[i]) > 200:
                        self.cumulative_x_history[i].pop(0)

            if self.prev_y_values is not None:
                diffs_y = [curr - prev for curr, prev in zip(y_values, self.prev_y_values)]

                for i in range(16):
                    self.cumulative_dy[i] += diffs_y[i]
                    self.cumulative_y_history[i].append(self.cumulative_dy[i])
                    if len(self.cumulative_y_history[i]) > 200:
                        self.cumulative_y_history[i].pop(0)


                # 선 그래프 갱신
                self.ax_x.clear()
                for i in range(16):
                    x_arr = np.array(self.cumulative_x_history[i], dtype=float)
                    y_arr = np.array(self.cumulative_y_history[i], dtype=float)
                    self.ax_x.plot(np.sqrt( (x_arr)**2 + (y_arr)**2 ), label=f"Sensor {i}", linewidth=1)

                self.ax_x.set_title("XY Value over Time (16 Sensors)")
                self.ax_x.set_xlabel("Time Step")
                self.ax_x.set_ylabel("XY Value")
                self.ax_x.grid(True)
                self.ax_x.legend(loc='upper right', fontsize='x-small')

            self.prev_x_values = x_values  # 저장
            self.prev_y_values = y_values  # 저장

            # if self.prev_y_values is not None:
            #     diffs_y = [curr - prev for curr, prev in zip(y_values, self.prev_y_values)]

            #     for i in range(16):
            #         self.cumulative_dy[i] += diffs_y[i]
            #         self.cumulative_y_history[i].append(self.cumulative_dy[i])
            #         if len(self.cumulative_y_history[i]) > 100:
            #             self.cumulative_y_history[i].pop(0)

            #     # 선 그래프 갱신
            #     self.ax_y.clear()
            #     for i in range(16):
            #         self.ax_y.plot(self.cumulative_y_history[i], label=f"Sensor {i}", linewidth=1)

            #     self.ax_y.set_title("Z Value over Time (16 Sensors)")
            #     self.ax_y.set_xlabel("Time Step")
            #     self.ax_y.set_ylabel("Z Value")
            #     self.ax_y.grid(True)
            #     self.ax_y.legend(loc='upper right', fontsize='x-small')

            # self.prev_y_values = y_values  # 저장

            if self.prev_z_values is not None:
                diffs_z = [curr - prev for curr, prev in zip(z_values, self.prev_z_values)]

                for i in range(16):
                    self.cumulative_dz[i] += diffs_z[i]
                    self.cumulative_z_history[i].append(self.cumulative_dz[i])
                    if len(self.cumulative_z_history[i]) > 200:
                        self.cumulative_z_history[i].pop(0)

                # 선 그래프 갱신
                self.ax_z.clear()
                for i in range(16):
                    self.ax_z.plot(self.cumulative_z_history[i], label=f"Sensor {i}", linewidth=1)

                self.ax_z.set_title("Z Value over Time (16 Sensors)")
                self.ax_z.set_xlabel("Time Step")
                self.ax_z.set_ylabel("Z Value")
                self.ax_z.grid(True)
                self.ax_z.legend(loc='upper right', fontsize='x-small')

            self.prev_z_values = z_values  # 저장


            self.fig_x.canvas.draw()
            self.fig_x.canvas.flush_events()
            # self.fig_y.canvas.draw()
            # self.fig_y.canvas.flush_events()
            self.fig_z.canvas.draw()
            self.fig_z.canvas.flush_events()


        except Exception as e:
            self.get_logger().error(f"파싱 오류: {e}")
   

def main(args=None):
    rclpy.init(args=args)
    node = DiffPrinter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
