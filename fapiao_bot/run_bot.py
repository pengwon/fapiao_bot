import json
from email_client import EmailClient
from fapiao_downloader import FapiaoDownloader

if __name__ == "__main__":

    with open("./config.json", "r") as config_file:
        config = json.load(config_file)
    
    email_client = EmailClient(
        server=config["email"]["server"],
        username=config["email"]["username"],
        password=config["email"]["password"],
    )
    email_client.connect()
    fapiao_emails = email_client.get_fapiao_emails()

    # 创建 FapiaoDownloader 实例
    downloader = FapiaoDownloader()
    fapiao_pdfs = downloader.download_fapiao(fapiao_emails)
    for fapiao_pdf in fapiao_pdfs:
        if not fapiao_pdf[1]:
            email_client.set_email_unread(fapiao_pdf[0])
            