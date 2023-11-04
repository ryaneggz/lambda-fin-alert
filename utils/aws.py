import boto3
from config import Config

####################################################################
## File to object storage
####################################################################
def upload_to_s3(img_bytes, file_name, bucket, prefix=None, presigned=True, expiration=3600):
    # Create an S3 client
    s3 = boto3.client(
        's3',
        region_name=Config.AWS_S3_REGION.value,  # Specify your region
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID.value,
        aws_secret_access_key=Config.AWS_SECRET_KEY.value,
        config=boto3.session.Config(signature_version='s3v4')
    )

    # Construct the file path with an optional prefix
    file_path = f"{prefix}/{file_name}" if prefix else file_name

    # Upload the image bytes to S3
    s3.put_object(Bucket=bucket, Key=file_path, Body=img_bytes)

    if presigned:
        # Generate a presigned URL for the uploaded image
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': file_path},
            ExpiresIn=expiration  # URL expires in 1 hour
        )
        return presigned_url

    # Return the public URL of the uploaded image
    img_url = f"https://{bucket}.s3.amazonaws.com/{file_path}"
    return img_url