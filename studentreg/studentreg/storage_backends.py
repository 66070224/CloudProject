from storages.backends.s3boto3 import S3Boto3Storage

# สำหรับ static files (CSS, JS, etc.)
class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = None

# สำหรับ media files (user uploads)
class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = None