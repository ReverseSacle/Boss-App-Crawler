from config import boss_appPackage, boss_appActivity, job_key, order_require, \
    job_area_element, job_company_element, head_img_path, chose_img_path, \
    order_list_img_path, more_img_path, collect_empty_img_path, share_button_img_path, \
    reload_button_img_path, collect_full_img_path, home_search_button_img_path, history_img_path, \
    retry_button_img_path, home_search_button, order_button, order_button_method, \
    share_button_link, three_point_button, center_point_button, back_button
from tool.adb_event import stop_app, open_app, tap, edge_scroll, input_text, screenshot, get_clipboard, \
    switch_to_clipper, switch_to_adbkey, switch_off_adbkey, connect_device, horizon_swipe, switch_off_clipper
from tool.image_event import element_match, wait_for_element, tap_until
from paddleocr import PaddleOCR
from scr.save_to_excel import SaveToExcel

from PIL import Image
import numpy as np

"""
加载等待
误触处理
元素等待
文本分隔
重复文本去除

经测试，以下可能是Boss的反自动化爬取：
网络通畅的情况下加载超时，要求点击重试
"""
class BossProcess:
    def __init__(self,auto_close=True):
        self.auto_close = auto_close
        self.ocr = PaddleOCR(
            use_angle_clse=True,
            use_gpu=False,
            lang='ch',
            ir_optim=False
        )

        connect_device()
        switch_to_clipper()
        switch_to_adbkey()

        stop_app(boss_appPackage)
        open_app(boss_appPackage, boss_appActivity)
        self.save_to_excel = SaveToExcel()

    def __del__(self):
        if self.auto_close: stop_app(boss_appPackage)
        switch_off_adbkey()
        switch_off_clipper()
        return True

    def __exit__(self):
        if self.auto_close: stop_app(boss_appPackage)
        switch_off_adbkey()
        switch_off_clipper()
        return True

    def switch_to_search(self):
        wait_for_element(head_img_path)
        tap_until(home_search_button_img_path, home_search_button)

        search_button = element_match(home_search_button_img_path)
        tap(search_button[0] - 100,search_button[1])

        wait_for_element(history_img_path)
        input_text(job_key)
        tap(search_button[0],search_button[1])
        wait_for_element(chose_img_path)

    def choose_condition(self):
        tap(order_button[0], order_button[1])
        wait_for_element(order_list_img_path)

        order_method = order_button_method[order_require]
        tap(order_method[0], order_method[1])
        edge_scroll(y=-100, slow_down=True)

    def check_if_in_page(self):
        if element_match(collect_empty_img_path)[2] < 0.7 and \
                element_match(collect_full_img_path)[2] < 0.7:
            tap(back_button[0], back_button[1])

    """
    经判断，文本是有固定长度的，
    为此先向下滑动两次，当遇见`查看更多`字眼时便会点击，之后滑动到顶部。
    接着就是利用OCR获取文字。
    """
    def image_recognize(self):
        print('BossProcess::image_recognize event => ....')
        # 查找`查看更多`
        count = 2
        while count:
            edge_scroll(y=-700, slow_down=True, duration=600)
            more_button = element_match(more_img_path)
            if more_button[2] > 0.7:
                tap(more_button[0], more_button[1])
                break
            self.check_if_in_page()

            count -= 1
        edge_scroll(y=1000, slow_down=True, duration=50)
        self.check_if_in_page()

        screenshot()
        img_path = np.array(Image.open('./screenshot.png'),dtype='float32')
        result = self.ocr.ocr(img_path, cls=False)
        del img_path

        job_name = ''
        length = len(result[0]) - 2
        i = 0

        job_salary = ''
        # 职位与薪资
        while i < length and job_area_element not in result[0][i][1][0]:
            text = result[0][i][1][0]
            i += 1
            if '客户公司' in text: break
            if '-' in text: job_salary = text
            else: job_name = f'{job_name}{text}'

        # 工作地区及岗位标签
        job_tags = ''
        while i < length:
            text = result[0][i][1][0]
            job_tags = f'{job_tags}/{text}'
            if '职位详情' == text: break
            i += 1

        job_content = ''
        while i < length:
            text = result[0][i][1][0]
            job_content = f'{job_content}{text}\n'
            i += 1

        job_company = ''
        job_company_tags = ''

        last_content = result[0][length - 1][1][0]
        switcher = True
        while True:
            if switcher:
                edge_scroll(y=-700, slow_down=True, duration=300)
                edge_scroll(y=400, slow_down=True, duration=400)
            else: edge_scroll(y=400, slow_down=True, duration=400)
            self.check_if_in_page()

            screenshot()
            img_path = np.array(Image.open('./screenshot.png'),dtype='float32')
            result = self.ocr.ocr(img_path, cls=False)
            del img_path

            length = len(result[0]) - 2
            i = length
            idx = -1
            cache = ''
            while i > 2:
                text = result[0][i][1][0]
                if last_content == text: break
                if '' == job_company and any(each in text for each in job_company_element):
                    job_company = result[0][i - 1][1][0]
                    job_company_tags = text
                    idx = i + 1
                    i -= 1
                else: cache = f'{text}\n{cache}'
                i -= 1

            job_content = f'{job_content}{cache}'
            if -1 != idx:
                while idx < length:
                    job_company_tags = f'{job_company_tags}/{result[0][idx][1][0]}'
                    idx += 1
                break
            last_content = result[0][length - 1][1][0]
            if '你的竞争力分析' in job_content or '添加住址' in job_content:
                switcher = False

        return [
            job_name,
            job_salary,
            job_tags,
            job_company,
            job_company_tags,
            job_content
        ]

    def content_crawl(self):
        print('BossProcess::content_crawl event => ....')
        unlimited_button = element_match(chose_img_path)
        tap_until(
            collect_empty_img_path,
            [unlimited_button[0],element_match(chose_img_path)[1] + 100]
        )
        count_crawl = 0
        while True:
            while element_match(collect_empty_img_path)[2] < 0.7 and \
                element_match(collect_full_img_path)[2] < 0.7:
                retry_button = element_match(retry_button_img_path)
                if retry_button[2] >= 0.7: tap(retry_button[0],retry_button[1])

            tap(three_point_button[0],three_point_button[1])
            if element_match(share_button_img_path)[2] < 0.7:
                tap(three_point_button[0], three_point_button[1])
                tap(center_point_button[0], center_point_button[1])
            tap(share_button_link[0], share_button_link[1])
            job_link = get_clipboard()

            job_box = self.image_recognize()
            job_name = job_box[0]
            job_salary = job_box[1]
            job_tags = job_box[2]
            job_company = job_box[3]
            job_company_tags = job_box[4]
            job_content = job_box[5]

            count_crawl += 1
            print('\n------------------------------------------------------------------------------------')
            print(f'职位：{job_name},薪资：{job_salary}\n,工作地区及岗位标签：{job_tags},\n,公司名：{job_company}\n,公司标签：{job_company_tags}\n,工作详情页：\n{job_content}\n,职位沟通链接：{job_link},\n已获取：{count_crawl}')
            print('------------------------------------------------------------------------------------\n')
            self.save_to_excel.save(
                job_name,
                job_salary,
                job_tags,
                job_company,
                job_company_tags,
                job_content,
                job_link
            )

            horizon_swipe()
            reload_button = element_match(reload_button_img_path)
            if reload_button[2] >= 0.7:
                raise ValueError('Reload button checked reach. Fail Crawl')
