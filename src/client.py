
import requests

class S3Client():
    def __init__(self, api_url, api_key):
        """
        :param api_url: Deployed URL of the api
        :param api_key: API Key
        """
        self.api_url = api_url
        self.api_key = api_key

    def __headers(self):
        if self.api_key is None:
            raise Exception('API Key not found')
        return {'Content-Type': 'image/png',
                'x-api-key': self.api_key}
                 

    def _build_url(self, bucket_name, object_key):
        """
        Build the final URL to pass to requests

        :param bucket_name: S3 bucket name
        :param object_key: S3 object key
        """
        return f'{self.api_url}/{bucket_name}/{object_key}'


    def _request_success(self, r):
        """
        Check if the request is successful
        """
        return r.status_code == 200


    def upload_files(self, bucket_name, object_key, data):
        """
        Upload files to S3
        """
        url = self._build_url(bucket_name, object_key)
        r = requests.put(url,
                         data=data,
                         headers=self.__headers())

        if self._request_success(r):
            print(f'Successfully uploaded {object_key}')
        else:
            print(f'Failed to upload {object_key}')