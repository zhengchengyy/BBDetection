from transitions import Machine

'''
以下全局数组以及字典用于配置每个状态机以及状态的识别
'''
# 状态机的状态
states1 = ['lying', 'leg_swing', 'hand_swing', 'bent_leg']
states2 = ['lying_hand_swing', 'leg_swing', 'bent_leg']
states3 = ['lying', 'hand_swing_leg_swing', 'bent_leg']

# 转换规则
transitions1 = [
            {'trigger': 'lying', 'source': '*', 'dest': 'lying'},
            {'trigger': 'leg_swing', 'source': '*', 'dest': 'leg_swing'},
            {'trigger': 'hand_swing', 'source': '*', 'dest': 'hand_swing'},
            {'trigger': 'bent_leg', 'source': '*', 'dest': 'bent_leg'}]

transitions2 = [
            {'trigger': 'lying_hand_swing', 'source': '*', 'dest': 'lying_hand_swing'},
            {'trigger': 'leg_swing', 'source': '*', 'dest': 'leg_swing'},
            {'trigger': 'bent_leg', 'source': '*', 'dest': 'bent_leg'}]

transitions3 = [
            {'trigger': 'lying', 'source': '*', 'dest': 'lying'},
            {'trigger': 'hand_swing_leg_swing', 'source': '*', 'dest': 'hand_swing_leg_swing'},
            {'trigger': 'bent_leg', 'source': '*', 'dest': 'bent_leg'}]

# 用于定义每个状态机的状态，转移函数，起始状态
machineStateData = [
                    {'states': states1, 'transitions': transitions1, 'initial': states1[0]},
                    {'states': states2, 'transitions': transitions2, 'initial': states2[0]},
                    {'states': states3, 'transitions': transitions3, 'initial': states3[0]}]

# 动作模式定义
actions = {
            ('lying', 'lying_hand_swing', 'lying'): 'lying',
            ('leg_swing', 'lying_hand_swing', 'lying'): 'lying',
            ('hand_swing', 'lying_hand_swing', 'hand_swing_leg_swing'): 'hand swing',
            ('bent_leg', 'lying_hand_swing', 'hand_swing_leg_swing'): 'hand swing',
            ('lying', 'leg_swing', 'hand_swing_leg_swing'): 'leg swing',
            ('hand_swing', 'leg_swing', 'hand_swing_leg_swing'): 'leg swing',
            ('leg_swing', 'leg_swing', 'hand_swing_leg_swing'): 'leg swing',
            ('bent_leg', 'bent_leg', 'bent_leg'): 'bent leg',
            ('hand_swing', 'bent_leg', 'bent_leg'): 'bent leg',
            ('bent_leg', 'bent_leg', 'hand_swing_leg_swing'): 'bent leg',
            ('hand_swing', 'bent_leg', 'hand_swing_leg_swing'): 'bent leg'}

class Matter:
    pass


class Action:
    """
    通过对每一个传感器维护一个状态机，接受每个传感器的分析数据，记录状态变化，
    根据三个状态机的状态来决定实现的动作
    """

    def __init__(self, msd, ac):
        # 建立状态机数组
        num = len(msd)
        self.actions = ac
        self.matters = [Matter() for i in range(num)]
        self.machines = [
                        Machine(model=self.matters[i],
                                states=msd[i]['states'],
                                transitions=msd[i]['transitions'],
                                initial=msd[i]['initial'])
                        for i in range(num)]

    # 接受消息，改变状态
    def record(self, no, st):
        self.matters[int(no) - 1].trigger(st)
        self.checkMode()

    # 进行动作识别
    def checkMode(self):
        acMo = [i.state for i in self.matters]
        action = self.actions.get(tuple(acMo))
        if action != None:
            print('The action is', action)
        # print('keep recording...')


ac = Action(machineStateData, actions)

if __name__ == '__main__':
    import random
    from time import sleep
    mes = ['stl', 'sok']
    while True:
        no = random.randint(1, 3)
        ind = random.randint(0, 1)
        ac.record(no, mes[ind])
        sleep(0.5)


