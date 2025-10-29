from storages.backends.s3boto3 import S3Boto3Storage

# สำหรับ static files (CSS, JS, etc.)
class StaticStorage(S3Boto3Storage):
    location = 'static'

# สำหรับ media files (user uploads)
class MediaStorage(S3Boto3Storage):
    location = 'media'
