import argparse
import os
import zipfile


def zip_and_move_lambda(src_path: str, dst_path: str):
    """
    zips the python lambda function script and moves it into `<project_home>/aws/lambda-files`
    """
    if not os.path.isfile(dst_path):
        dst_file = os.path.split(dst_path)[-1]
    else:
        dst_file = dst_path

    with zipfile.ZipFile(dst_file, 'w') as zipped:
        zipped.write(src_path)

    os.replace(dst_file, dst_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Python Lambda Zipper")
    parser.add_argument('--src', type=str, help='The .py lambda filepath')
    parser.add_argument('--dst', type=str, help='The .zip filepath')
    args = parser.parse_args()
    zip_and_move_lambda(args.src, args.dst)
