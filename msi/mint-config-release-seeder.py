import boto3
import re
import os
import sys
import json

sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), "/home/pauls/deltarisk/backend/src"))

from accommon.config_manager import conf_man

# Initialize S3 client
s3 = boto3.client('s3')

# Source and destination buckets
source_bucket = "activeeye-build-artifacts-aerss-config"
destination_bucket = "activeeye-build-artifacts-aerss-config-mint-test"
temp_dir = "/tmp"

def move_files():
    conf_man.aws_session(profile='hawk')
    session = conf_man.aws_session()
    s3_client = session.client("s3")
    try:
        count = 0
        # List all objects in the source bucket
        response = s3_client.list_objects_v2(Bucket=source_bucket)
        if 'Contents' not in response:
            print("No files found in the source bucket.")
            return

        for obj in response['Contents']:
            key = obj['Key']
            # Check if the file matches the pattern "container_versions.txt-*"
            match = re.match(r"container_versions\.txt-(.+)", key)
            if match:
                suffix = match.group(1)  # Extract the suffix from the filename
                if suffix.startswith("config.v3.0."):
                    # New key for the destination bucket
                    new_key = f"{suffix}-container_versions.txt"

                    # Local file path for temporary download
                    local_file_path = os.path.join(temp_dir, new_key)

                    print(f"Downloading file: {key} from bucket: {source_bucket}")
                    # Download the file to the local temp directory
                    s3_client.download_file(source_bucket, key, local_file_path)

                    print(f"Uploading file: {local_file_path} to bucket: {destination_bucket} with new key: {new_key}")
                    # Upload the file to the destination bucket with the new name
                    # conf_man.aws_session(profile='mint-test')
                    # session = conf_man.aws_session()
                    # s3_client = session.client("s3")
                    # s3_client.upload_file(local_file_path, destination_bucket, new_key)


                    print(f"File moved successfully: {key} -> {new_key}")
                    # Remove the local file after upload
                    # os.remove(local_file_path)
                    # break
                    count += 1
            else:
                pass
                # print(f"Skipping file: {key}. Does not match the pattern.")
        print(f"{count} items moved.")
    except Exception as e:
        print(f"Error: {e}")

# Run the function
if __name__ == "__main__":
    move_files()
