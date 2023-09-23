import boto3
from botocore.exceptions import NoCredentialsError
from constants import BUCKET_NAME
from decouple import config
import tempfile

from pathlib import Path

CLIENT = boto3.client(
    's3',
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY")
)


def upload_chat_history_to_s3(chat_key: str, chat_history: list[tuple]) -> None:
    formatted_chat_history = _format_chat_history(chat_history)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / "chat_history.txt"
        tmp_file.write_text(formatted_chat_history)
        try:
            CLIENT.upload_file(
                str(tmp_file),
                BUCKET_NAME,
                chat_key,
                ExtraArgs={
                    'ContentType': 'text/plain',
                    'ContentDisposition': 'inline',
                }
            )
        except FileNotFoundError:
            print(f'The file {chat_key} was not found.')
        except NoCredentialsError:
            print('Credentials not available.')


def _format_chat_history(chat_history: list[tuple]) -> str:
    result = []
    for timestamp, participant, message in chat_history:
        result.append(
            "---\n"
            + f"{participant} at {timestamp}\n\n"
            + message
        )
    return "\n".join(result)
