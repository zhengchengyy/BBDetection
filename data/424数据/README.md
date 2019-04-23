## 数据说明

### 人员分类

PersonA：

PersonB：

### 动作分类

静止(1min)：still

连贯动作(1min)：(坐下躺下起身站起)sit_lay

大动作(2min)：翻身(turn_over)、腿部伸展(legs_stretch)、手部伸展(hands_stretch)；

小动作(1min)：腿部抽搐(legs_twitch)、手部抽搐(hands_twitch)、头部微小移动(head_move)；

剧烈动作(1min)：抓握(grasp)、踢踹(kick)

### 设备分布

总共五个设备，床头两侧两个，床尾两侧两个，床脚一个。详细请看设备分布图。

### 代码部分

可以从json中读取数据并画图详见代码：/server/drawWithJson.py

可以从数据库中读取数据并画图详见代码：/server/drawWithDB.py