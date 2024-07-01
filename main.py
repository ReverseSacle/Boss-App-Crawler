from scr.boss import BossProcess

"""
用手动试了下，1s一条这样刷，
大概在80条左右就被暂时封禁了，
也就是说就是你是真人都容易被封。

推荐USB连接，WIFI连接经常device offline.
开启手机的开发者模式，将动画关掉。
先手动打开app并搜索一次职位，再选择筛选条件，
并关闭红棕色横幅，不要清除历史搜索。

如果电脑没有NVIDIA显卡，就默认使用CPU，需设置电脑的虚拟内存，
电脑打开文件资源管理器 → 高级系统设置 → 性能 → 设置 → 高级 → 虚拟内存 → 更改 →
取消勾选自动管理所有驱动器的分页文件大小 → 选择一个非系统盘 → 自定义 → 
（16G物理内存，1.5倍虚拟内存）初始大小24576，最大值40960 → 设置 → 确定 → 重启电脑
"""
if __name__ == '__main__':
    ################### 必要组键 ###################
    # 一个一个装
    # 装完adbkeyboard就注释
    # adbkeyboard_install()

    # 取消下面的注释，安装clipper()
    # 并手动在手机设置里取消clipper软件的电池策略(智能省电)
    # clipper_install()
    ################### 必要组键 ###################

    bp = BossProcess(auto_close=True)
    bp.switch_to_search()
    bp.choose_condition()
    bp.content_crawl()
