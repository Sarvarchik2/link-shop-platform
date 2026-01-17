import time
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
        self._last_fail_time = 0
        self._fail_cooldown = 60 # 1 minute cooldown before trying Minio again if it failed

    def _ensure_bucket(self):
        if self._bucket_ensured:
            return
        
        # Don't try if we recently failed
        if time.time() - self._last_fail_time < self._fail_cooldown:
            raise Exception("Minio is in cooldown period after failure")

        try:
            # Check if bucket exists
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
            # Only log as warning once per cooldown to avoid spamming logs
            if time.time() - self._last_fail_time > self._fail_cooldown:
                logger.warning(f"Minio not available, using local storage fallback. Error: {e}")
            self._last_fail_time = time.time()
            self._bucket_ensured = False
            raise e

    def upload_file(self, filename: str, content: bytes, content_type: str) -> str:
        try:
            self._ensure_bucket()
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
            # Suppress logging if it's just a cooldown message
            if "cooldown" not in str(e).lower() and time.time() - self._last_fail_time > self._fail_cooldown:
                logger.debug(f"Minio upload failed, using local storage")
            raise e

storage = MinioStorage()
