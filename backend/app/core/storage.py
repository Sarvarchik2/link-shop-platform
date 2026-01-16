from minio import Minio
from io import BytesIO
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MinioStorage:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._bucket_ensured = False

    def _ensure_bucket(self):
        if self._bucket_ensured:
            return
        try:
            # Set a very short timeout for bucket check if it's the first time
            # But the minio client doesn't easily expose this per call without complex config
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                # Set public policy for the bucket so images can be accessed directly
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": ["*"]},
                            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                            "Resource": [f"arn:aws:s3:::{self.bucket_name}"],
                        },
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": ["*"]},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"],
                        },
                    ],
                }
                import json
                self.client.set_bucket_policy(self.bucket_name, json.dumps(policy))
                logger.info(f"Created Minio bucket: {self.bucket_name}")
            self._bucket_ensured = True
        except Exception as e:
            logger.error(f"Error ensuring Minio bucket: {e}")
            self._bucket_ensured = False # Try again next time if it failed due to network

    def upload_file(self, filename: str, content: bytes, content_type: str) -> str:
        self._ensure_bucket()
        try:
            self.client.put_object(
                self.bucket_name,
                filename,
                BytesIO(content),
                length=len(content),
                content_type=content_type
            )
            # Construct the public URL
            protocol = "https" if settings.MINIO_SECURE else "http"
            return f"{protocol}://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{filename}"
        except Exception as e:
            logger.error(f"Error uploading file to Minio: {e}")
            raise e

storage = MinioStorage()
