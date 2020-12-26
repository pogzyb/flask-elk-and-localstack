import os
import zipfile


lambda_file_name = "./py/consumer.py"
lambda_zip_file_name = "py-handler.zip"
output_path = os.path.join(os.getcwd(), "..", "aws/lambda-files/", lambda_zip_file_name)


def zip_and_move_lambda():
    """
    zips the python lambda function script and moves it into `<project_home>/aws/lambda-files`

    :return:
    """
    with zipfile.ZipFile(lambda_zip_file_name, 'w') as zipped:
        zipped.write(lambda_file_name)

    os.rename(lambda_zip_file_name, output_path)
    return


if __name__ == '__main__':
    zip_and_move_lambda()
