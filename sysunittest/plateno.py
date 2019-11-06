import random

def newplate():
    # 生成省份
    provinces = ['津', '渝', '晋', '吉', '苏', '皖', '赣', '豫', '湘',
                 '琼', '贵', '陕', '青', '桂', '宁', '京', '沪', '冀',
                 '辽', '黑', '浙', '闽', '鲁', '鄂', '粤', '川', '云',
                 '甘', '藏', '蒙', '新']
    a = random.choice(provinces)

    # 生成区字母
    plateb = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    b = random.choice(plateb)

    # 生成车牌后5位
    c = []
    platec = '1234567890ABCDEFGHJKLMNPQRSTUVWXYZ'
    for i in range(5):
        c.append(random.choice(platec))

    # 组合车牌
    # plateNo = (a + b + ','.join(c)).replace(',', '')
    plateNo = (a + b + ''.join(c))

    return (plateNo)