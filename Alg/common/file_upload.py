from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = "AKIDMZYBaliRwDG5f2C97wZy84lEUXMyMirm"  # 替换为用户的 secretId
secret_key = "lKfnjRwEH6h3B5uVs0ua2GG2a0FUYO0O"  # 替换为用户的 secretKey
region = "ap-chengdu"  # 替换为用户的 Region
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)


def upload_obj_avatar(user, file_obj):  # 上传文件对象
    filetype = file_obj.name.rsplit(".")[-1]  # 获取文件后缀
    response = client.upload_file_from_buffer(
        Bucket="algserver-md-img-1252510405",
        Body=file_obj,  # 需要上传的文件对象
        Key="user_avatar/{}_avatar.{}".format(user.username, filetype),  # 上传到桶之后的文件名
    )


road = "user_avatar/"  # 文件夹的路径


def get_avatar(user):
    file_key = "user_avatar/"
    response = client.list_objects(
        Bucket="algserver-md-img-1252510405", Prefix="user_avatar"
    )
    for content in response["Contents"]:
        print(content)
        file_name = content["Key"].split("/")[-1]  # 获取文件名部分（带文件后缀）
        file_name_without_extension = file_name.split(".")[0]  # 去除文件后缀，获取纯文件名
        # if file_name_without_extension == user.username:
        #     return content


class cencloud:
    def __init__(self, secret_id, secret_key, region):
        self.config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        self.client = CosS3Client(self.config)

    # --------------------上传文件的方法--------------

    def upload(self):
        response = self.client.upload_file(
            Bucket="algserver-md-img-1252510405",
            LocalFilePath=r"day16\app01\static\js\echarts.js",  # 本地文件的路径
            # "r"前缀用于定义一个原始字符串，其中的反斜杠不需要进行额外的转义
            Key="{}".format("username"),  # 上传到桶之后的文件名
        )
        print(response["ETag"])

    def upload_obj(self, img_obj):  # 上传文件对象
        response = self.client.upload_file_from_buffer(
            Bucket="algserver-md-img-1252510405",
            Body=img_obj,  # 需要上传的文件对象
            Key="p1.png",  # 上传到桶之后的文件名
        )

    # --------------创建存储桶的方法--------------

    def create_buc(self):
        response = self.client.create_bucket(
            Bucket="test-1251317460",  # 创建桶名称
            ACL="public-read",  # private  /  public-read / public-read-write
        )


if __name__ == "__main__":
    get_avatar(1)
