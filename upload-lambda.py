import zipfile
import boto3
import mimetypes
import os
import tempfile

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    with tempfile.TemporaryDirectory() as tmpdir:
        s3.download_file('portfolio-build-blanchlu',
                    'buildPortfolio', os.path.join(tmpdir, 'buildPortfolio.zip'))
        os.chdir(tmpdir)
        with zipfile.ZipFile('buildPortfolio.zip', 'r') as myzip:
            myzip.extractall()
            for nm in myzip.namelist():
                s3.upload_file(nm, 'serverless-practice-blanchlu', nm,
                              ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                s3.put_object_acl(Bucket='serverless-practice-blanchlu',
                                  Key=nm, ACL='public-read')