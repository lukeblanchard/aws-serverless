import zipfile
import boto3
import mimetypes

s3 = boto3.client('s3')
s3.download_file('portfolio-build-blanchlu',
                 'buildPortfolio', './buildPortfolio.zip')

with zipfile.ZipFile('./buildPortfolio.zip') as myzip:
    for nm in myzip.namelist():
        s3.upload_file(nm, 'serverless-practice-blanchlu', nm,
                       ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        s3.put_object_acl(Bucket='serverless-practice-blanchlu',
                          Key=nm, ACL='public-read')
