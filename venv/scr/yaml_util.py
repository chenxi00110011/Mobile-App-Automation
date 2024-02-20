import yaml
import os


class YamlUtil:
    file_name = ''

    def __init__(self, file_name):
        # 初始化yaml文件名称和文件路径
        self.file_name = file_name
        self.file_path = os.getcwd() + f'/{file_name}'

    # 读取yaml文件
    def read_yaml(self):
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value

    # 写入yaml文件
    def write_yaml(self, data):
        with open(self.file_path, mode='a', encoding='utf-8') as f:
            yaml.dump(data=data, stream=f)

    # 清除yaml文件
    def clear_yaml(self):
        with open(self.file_path, mode='w', encoding='utf-8') as f:
            f.truncate()


if __name__ == '__main__':
    # data = {'name': {'q': '123'}}
    # YamlUtil(file_name='devicesList.yml').write_yaml(data=data)
    # value = YamlUtil(file_name='devicesList.yml').read_yaml()['name']
    # print(value['q'])
    # YamlUtil(file_name='devicesList.yml').clear_yaml()
    res = YamlUtil(file_name='..\\data\\sheetName.yaml').read_yaml()
    print(res)
