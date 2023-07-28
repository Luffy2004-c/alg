from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = "AKIDMZYBaliRwDG5f2C97wZy84lEUXMyMirm"  # 替换为用户的 secretId
secret_key = "lKfnjRwEH6h3B5uVs0ua2GG2a0FUYO0O"  # 替换为用户的 secretKey
region = "ap-chengdu"  # 替换为用户的 Region
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

 # 上传文件对象
def upload_obj_avatar(user, file_obj): 
    filetype = file_obj.name.rsplit(".")[-1]  # 获取文件后缀
    response = client.upload_file_from_buffer(
        Bucket="algserver-md-img-1252510405",
        Body=file_obj,  # 需要上传的文件对象
        Key="user_avatar/{}_avatar.{}".format(user.username, filetype),  # 上传到桶之后的文件名
    )


road = "user_avatar/"  # 文件夹的路径

#获取用户头像URL
def get_avatar(user):
    file_key = "user_avatar/"
    response = client.list_objects(
        Bucket="algserver-md-img-1252510405", Prefix="user_avatar"
    )
    for content in response["Contents"]:
        user_avatar = content["Key"].split("/")[-1].split(".")[0]  # 去除文件后缀，获取纯文件名
        avatar_name = "{}_avatar".format(user.username)
        if user_avatar == avatar_name:
            avatar_url = (
                "https://algserver-md-img-1252510405.cos.ap-chengdu.myqcloud.com/"
                + content["Key"]
            )
            return avatar_url


#创建新的存储桶
def create_buc():
    response = client.create_bucket(
        Bucket="test-1251317460",  # 创建桶名称
        ACL="public-read",  # private  /  public-read / public-read-write
    )
