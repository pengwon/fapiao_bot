import imapclient
import email


class EmailClient:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = imapclient.IMAPClient(self.server, ssl=True)
            self.client.login(self.username, self.password)
            self.client.id_({"name": "IMAPClient", "version": "1.0.0"})
            return True
        except Exception as e:
            print(f"Failed to connect to the email server: {e}")
            return False

    def list_folders(self):
        if not self.client:
            print("Not connected to the email server. Call 'connect' method first.")
            return []

        folder_list = self.client.list_folders()
        return [folder_info[2] for folder_info in folder_list]

    def fapiao_folder_exists(self):
        if "发票" in self.list_folders():
            return True
        else:
            print("'发票'文件夹不存在，正在创建...")
            self.client.create_folder("发票")
            print("已创建'发票'文件夹，请登录邮箱创建收信规则。")
            return False

    def get_fapiao_emails(self, search_criteria=["UNSEEN"]):
        fapiao_emails = []

        if not self.client:
            print("Not connected to the email server. Call 'connect' method first.")
            return []

        self.client.select_folder("发票")
        email_ids = self.client.search(search_criteria)

        for email_id in email_ids:
            email_message = self.fetch_email_content(email_id)
            decoded_subject = email.header.decode_header(email_message["Subject"])

            # 初始化一个空字符串来存储解码后的主题文本
            subject_text = ""

            # 遍历解码结果
            for part, encoding in decoded_subject:
                # 如果编码为None，则假定使用UTF-8编码
                if encoding is None:
                    subject_text += part
                else:
                    # 使用指定编码解码部分
                    subject_text += part.decode(encoding, errors="ignore")

            # 检查解码后的主题文本是否包含"发票"
            if "发票" in subject_text:
                fapiao_emails.append([email_id, email_message])
            else:
                print(f"邮件主题不包含'发票'，已标记'未读'，请登录邮箱检查")
                print(f"email_id: {email_id}")
                print(f"email_subject: {subject_text}")
                print("-" * 80)
                self.set_email_unread(email_id)

        return fapiao_emails

    def fetch_email_content(self, email_id):
        if not self.client:
            print("Not connected to the email server. Call 'connect' method first.")
            return None

        raw_message_data = self.client.fetch([email_id], ["BODY[]", "FLAGS"])
        message_data = raw_message_data[email_id]
        email_message = email.message_from_bytes(message_data[b"BODY[]"])

        return email_message
    
    def set_email_unread(self, email_id):
        if not self.client:
            print("Not connected to the email server. Call 'connect' method first.")
            return None

        self.client.set_flags(email_id, [b"UNSEEN"])
