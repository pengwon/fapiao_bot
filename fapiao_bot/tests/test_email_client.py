# test_email_client.py

import sys
import os

import pytest
import json

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录到 Python 解释器的路径中
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

from email_client import EmailClient  # 使用相对路径导入 EmailClient 类

# 从 config.json 文件中读取配置
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# 使用pytest的fixture来初始化EmailClient实例
@pytest.fixture
def email_client():
    return EmailClient(server=config['email']['server'], username=config['email']['username'], password=config['email']['password'])

def test_connect(email_client):
    # 测试连接到邮箱服务器是否成功
    assert email_client.connect() == True

def test_get_unread_emails(email_client):
    # 测试获取未读邮件
    email_client.connect()  # 先连接到邮箱服务器
    unread_emails = email_client.get_unread_emails()
    assert isinstance(unread_emails, list)

def test_fetch_email_content(email_client):
    # 测试获取邮件内容
    email_client.connect()  # 先连接到邮箱服务器
    unread_emails = email_client.get_unread_emails()
    if unread_emails:
        email_id = unread_emails[0]
        email_message = email_client.fetch_email_content(email_id)
        assert email_message is not None

if __name__ == '__main__':
    pytest.main()
