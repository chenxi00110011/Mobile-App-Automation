# -*- coding: utf-8 -*-
from xrs_app import MobieProject, get_element_data
from environment_variable import cmri_excel_element_dict
import yaml_util
import easygui


class AppElement:
    def __init__(self, appName):
        self.app_info = yaml_util.YamlUtil(file_name='..\\data\\app_info.yaml').read_yaml()
        self.appName = appName
        self.sheetName = None

    def save_element_to_excel(self):
        # 存储每个页面的元素到excel，用于判断当前所属页面
        app = MobieProject(self.appName)
        # 获取 app 页面元素列表
        test_list = ["修改设备名称", "绑定结果"]
        while True:
            if not easygui.ccbox('是否开始', '提示', ['开始', '退出']):
                break
            easygui.msgbox("请检查excel文件是否关闭 !", "提示", "已关闭")
            vex1 = easygui.enterbox(msg='输入当前页面名称：', title='APP页面名称', default='')
            elements = app.driver.find_elements("//*")
            # 输出元素数量
            print("页面元素数量为：", len(elements))
            if easygui.ccbox('是否保存到excel文件中', '页面元素保存', ['保存', '取消']):
                continue
            # 保存到excel
            for element in elements:
                try:
                    if element.text:
                        if self.sheetName is None:
                            sheetName = easygui.enterbox(msg='输入保存到excel的页名：', title='保存页', default='')
                            self.sheetName = sheetName
                        get_element_data(element, cmri_excel_element_dict, str(vex1), sheetName=self.sheetName)
                except Exception as e:
                    print(e)
                    continue


def test_pwd():
    app = MobieProject('和家亲')
    while True:
        print(app.pwd())
        input('请按回车继续：')


if __name__ == '__main__':
    AppElement('和家亲').save_element_to_excel()
