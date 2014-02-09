import sys
import boto
import StringIO
from optparse import OptionParser

AWS_KEY='AWS-KEY'
AWS_SECRET='AWS-SECRET'

def die(e): raise Exception(e)

parser = OptionParser()

parser.add_option('-k', '--key', dest='awskey',
                  help='AWS API key', default=AWS_KEY)

parser.add_option('-s', '--secret', dest='awssecret',
                  help='AWS secret key', default=AWS_SECRET)

parser.add_option('-b', '--bucket', dest='bucket',
                  help='Destination bucket')

parser.add_option('-f', '--filename', dest='filename',
                  help='Destination filename', type='string')

parser.add_option('-p', '--partsize', dest='partsize',
                  help='Size of each part', type='int', default=1024*1024*1024)

(options, args) = parser.parse_args()

FILE_NAME  = options.filename or die('Filename Required -f')
S3_BUCKET  = options.bucket or die('Bucket Required -b') 
AWS_KEY    = options.awskey or die('AWS Key required -k')
AWS_SECRET = options.awssecret or die('AWS Secret required -s')
FILE_SIZE  = options.partsize

s3 = boto.connect_s3(AWS_KEY, AWS_SECRET)

b = s3.get_bucket(S3_BUCKET)

mp = b.initiate_multipart_upload(FILE_NAME)

chunk = FILE_SIZE
i = 1
while 1:
    data = sys.stdin.read(chunk)
    if not data:
        break
    fplike = StringIO.StringIO(data)
    print 'uploading part %d' % i
    mp.upload_part_from_file(fplike, i)
    i += 1
    fplike.close()


print 'Finilizing Upload... ',
mp.complete_upload()
print ' Done.'

