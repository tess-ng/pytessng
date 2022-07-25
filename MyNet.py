from PySide2.QtGui import QVector3D
from Tessng import PyCustomerNet, tngIFace, m2p


# 用户插件子类，代表用户自定义与路网相关的实现逻辑，继承自MyCustomerNet
class MyNet(PyCustomerNet):
    def __init__(self):
        super(MyNet, self).__init__()

    # 创建路网
    def createNet(self):
        iface = tngIFace()

        # 代表TESS NG的接口
        # iface = tngIFace()
        # 代表TESS NG的路网子接口
        netiface = iface.netInterface()

        def get_coo_list(vertices):
            list1 = []
            x_move, y_move = 0, 0 #sum(self.xy_limit[:2]) / 2, sum(self.xy_limit[2:]) / 2 if self.xy_limit else (0, 0)
            for index in range(0, len(vertices), 1):
                vertice = vertices[index]
                list1.append(QVector3D(m2p((vertice[0] - x_move)), m2p(-(vertice[1] - y_move)), m2p(vertice[2])))
            if len(list1) < 2:
                raise 3
            return list1
        link_point = [(i, 0, 0) for i in range(1000)]
        lane_points = {
            'right': [(i, 0, 0) for i in range(1000)],
            'center': [(i, 100, 0) for i in range(1000)],
            'left': [(i, 200, 0) for i in range(1000)],
        }
        lCenterLinePoint = get_coo_list(link_point)
        lanesWithPoints = [
            {
                'left': get_coo_list(lane['left']),
                'center': get_coo_list(lane['center']),
                'right': get_coo_list(lane['right']),
            } for lane in [lane_points]
        ]
        netiface.createLink3DWithLanePoints(lCenterLinePoint, lanesWithPoints,
                                          f"_right")
        pass

    def afterLoadNet(self):
        # 代表TESS NG的接口
        iface = tngIFace()
        # 代表TESS NG的路网子接口
        netiface = iface.netInterface()
        # 设置场景大小
        netiface.setSceneSize(10000, 10000)  # 测试数据
        # netiface.setSceneSize(4000, 1000)  # 华为路网
        # netiface.setSceneSize(10000, 3000)  # 深圳路网
        # 获取路段数
        count = netiface.linkCount()
        netiface.createNet("S32路网", "OPENDRIVE")

        # if (count == 0):
        #     self.createNet()