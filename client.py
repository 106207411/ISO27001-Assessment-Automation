import os
import requests

class S3Client(object):
    def __init__(self,
                 api_url='https://el4y3cbugi.execute-api.ap-northeast-1.amazonaws.com/v1',
                 headers={'Content-Type': 'image/png',
                          'x-api-key': '8uy0YGL5GJ5wUJwtHGibL1ab0XzNYNdeakCrCvw5'},
                 ):
        """
        :param api_url: Deployed URL of the api
        :type api_url: str
        :param headers: Headers to pass to requests
        :type headers: dict
        """
        self.api_url = api_url
        self.headers = headers


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


    def upload_files(self, bucket_name):
        """
        Upload files to S3
        """
        img_dir = os.popen("hostname").read().strip()

        if os.path.exists(img_dir):
            for fname in os.listdir(img_dir):
                if fname.endswith('.png'):
                    fpath = os.path.join(img_dir, fname)
                    data = open(fpath, 'rb').read()

                    url = self._build_url(bucket_name, f'{img_dir}%2F{fname}')
                    r = requests.put(url,
                                     data=data,
                                     headers=self.headers)

                    if self._request_success(r):
                        print(f'Successfully uploaded {fname}')
                    else:
                        print(f'Failed to upload {fname}')