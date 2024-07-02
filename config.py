############################# Appium #############################
boss_appPackage = 'com.hpbr.bosszhipin'
boss_appActivity = 'com.hpbr.bosszhipin.module.launcher.WelcomeActivity'

capabilities = dict(
    platformName='Android',
    platformVersion='9',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage=boss_appPackage,
    appActivity=boss_appActivity,
    noReset=True
)

appium_server_url = 'http://localhost:4723'
#device_name = '192.168.2.231:5555'
device_name = '6a29887'
adb = f'adb -s {device_name}'
############################# Appium #############################

############################ Paddle model ########################
# 这里吐槽一句，使用轻量版model，文本内容中有 某为 公司就TM文本检测到了
# 为此这里可选用高精度模型，但耗时更长了
# det_model_dir = './model/ch_PP-OCRv4_det_server_infer'
# rec_model_dir = './model/ch_PP-OCRv4_rec_server_infer'
############################ Paddle model ########################


#################################################################
# 职位过滤器
job_key = 'C++后端'
# ["综合排序","最新优先","匹配度优先"]
order_require = '匹配度优先'

# 文本分类的分隔关键字
job_area_element = '东莞'
job_company_element = ['人·', '人以上·']


# 图标定位所需的图片
img_path = './img'
more_img_path = f'{img_path}/more.png'
head_img_path = f'{img_path}/head.png'
chose_img_path = f'{img_path}/chose.png'
history_img_path = f'{img_path}/history.png'
home_search_button_img_path = f'{img_path}/home_search_button.png'
order_list_img_path = f'{img_path}/order_list.png'
collect_empty_img_path = f'{img_path}/collect_empty.png'
collect_full_img_path = f'{img_path}/collect_full.png'
share_button_img_path = f'{img_path}/share_button.png'
reload_button_img_path = f'{img_path}/reload_button.png'
retry_button_img_path = f'{img_path}/retry_button.png'

#################################################################


########################## button_location ##################################
# 计算方法
# 利用Appium-Inspector点击相应的元素位置，通过bounds计算中间值
# bounds [x1,y1][x2,y2]
# [0]: (x1+x2) / 2
# [1]: (y1+y2) / 2
# [x轴位置，y轴位置]
##################################### 界面按钮 #####################################

# 主页搜索框元素
home_search_button = [803,142]
# 顶栏返回按钮元素
back_button = [91,143]

##################################### 界面按钮 #####################################


##################################### 职位选择按钮 #####################################

#### 综合排序-排序按钮 ####
order_button = [287,391]
########################

############### 各按钮 #####################
# "距离优先"需要手动在地图上选择,这里不计入
order_button_method = {
    "综合排序": [143,1616],
    "最新优先": [143,1758],
    "匹配度优先": [165,2042]
}
##################################### 职位选择按钮 #####################################

##################################### 职位详情页 #####################################

# app职位详情页中`职位详情`标题的左上坐标
# [x轴偏移量为: -50,y轴偏移量为: 0]
resolution = [5,1256]

#### 详情页面-分享按钮-文件加一个箭头的图标 ####
# 主页最右边的按钮
three_point_button = [992,152]
center_point_button = [882,152]
# 点击分享图标后出现的分享链接按钮
share_button_link = [863,1832]
##########################################

##################################### 职位详情页 #####################################

########################## button_location ##################################