import click
import boto3
import os

actions = ['create', 'upload', 'delete', 'delete_all', 'delete_file', 'list_buckets', 'list_objects']

os.environ['AWS_PROFILE'] = "pyuser"
os.environ['AWS_DEFAULT_REGION'] = "ap-south-1"

s3 = boto3.resource('s3')
s3client = boto3.client('s3')

def create_bucket(bucket_name):
    """Creates a bucket"""
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})

def bucket_list():
    """Lists the bucket created by the account"""
    response = s3client.list_buckets()
    print('List of the buckets: ')
    for bucket in response["Buckets"]:
        print(bucket['Name'])

def upload_object(source_filename, bucket_name, target_filename):
    """Uploads an object in a bucket."""
    s3client.upload_file(source_filename, bucket_name, target_filename)

def delete_bucket(bucket_name):
    """Deletes a bucket."""
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        obj.delete()
    bucket.delete()

def delete_all_objects(bucket_name):
    """Deletes objects in a bucket."""
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        obj.delete()

def list_all_objects(bucket_name):
    """lists all objects in a bucket."""
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        print(obj.key)

def delete_object(bucket_name, target_filename):
    """deletes a file in a bucket if name matches"""
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        if target_filename == obj.key:
            obj.delete()
            print('{} is deleted from the bucket {}'.format(target_filename, bucket_name))
        else:
            print('{} is not found in the bucket {}'.format(target_filename, bucket_name))

def no_action_picked():
    print("Please select an action:\n{}\ne.g. buckgo list_buckets".format(actions))

@click.command()
@click.argument('action')
@click.option('--bucket_name', '-b', help='Enter bucket name: -b <bucket_name>')
@click.option('--source_filename', '-sf', help='Enter filename: -sf <filepath>')
@click.option('--target_filename', '-tf', help='Enter filename: -tf <filepath>')
def main(action, bucket_name, source_filename, target_filename):
    action_dict = {
        'create' : lambda : create_bucket(bucket_name),
        'upload' : lambda : upload_object(source_filename, bucket_name, target_filename),
        'list_buckets' : lambda : bucket_list(),
        'delete' : lambda : delete_bucket(bucket_name),
        'delete_all' : lambda : delete_all_objects(bucket_name),
        'delete_file' : lambda : delete_object(bucket_name, target_filename),
        'list_objects' : lambda : list_all_objects(bucket_name)
    }
    def default():
        no_action_picked()
    
    action_run = action_dict.get(action, default)
    action_run()

if __name__ == '__main__':
    main()