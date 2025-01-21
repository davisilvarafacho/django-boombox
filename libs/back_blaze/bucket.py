from django.core.cache import cache

from b2sdk.v2 import AuthInfoCache, B2Api, DoNothingProgressListener, InMemoryAccountInfo

from utils.env import get_env_var


class BackBlazeB2Handler:
    def __init__(self):
        application_key_id = get_env_var("BACKBLAZE_APPLICATION_ID")
        application_key = get_env_var("BACKBLAZE_APPLICATION_KEY")
        bucket_name = get_env_var("BACKBLAZE_BUCKET_NAME")

        info = InMemoryAccountInfo()

        self.b2_api = B2Api(info, cache=AuthInfoCache(info))
        self.b2_api.authorize_account("production", application_key_id, application_key)
        self.bucket = self.b2_api.get_bucket_by_name(bucket_name)

    def upload(self, bytes_arquivo, path, metadata=None):
        if metadata is None:
            metadata = {}

        back_blaze_file = self.bucket.upload_bytes(
            data_bytes=bytes_arquivo,
            file_name=path,
            file_info=metadata,
        )

        return back_blaze_file

    def download(self, file_id):
        cache_image = cache.get(file_id)
        if cache_image:
            return cache_image

        try:
            progress_listener = DoNothingProgressListener()
            downloaded_file = self.b2_api.download_file_by_id(file_id, progress_listener)
        except Exception:
            return None

        cache.set(file_id, downloaded_file, 60 * 60 * 24)

        return downloaded_file
