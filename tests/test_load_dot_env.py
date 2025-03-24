# Copyright 2024 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# type: ignore

import os
import subprocess
from pathlib import Path

from quickstart import load_dotenv


def get_bash_env(env_content: str, var_name: str, tmp_path: Path) -> str:
    """Run the env file through bash and get a variable's value"""
    # Create a shell script that sources our env file and prints the variable
    script = f'source .env && echo "${var_name}"'

    # Run it in bash
    result = subprocess.run(
        ["bash", "-c", script],
        input=env_content.encode(),
        capture_output=True,
        cwd=str(tmp_path),
    )
    return result.stdout.decode().strip()


def test_against_bash(tmp_path):
    env_content = """
SINGLE=value
QUOTED="quoted value"
COMMENT=value # with comment
MULTI='first line
second line
third line'
AFTER=normal_value
"""
    env_path = tmp_path / ".env"
    env_path.write_text(env_content)

    # Get our implementation's results
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        env_vars = load_dotenv()
    finally:
        os.chdir(old_cwd)

    # Compare with bash for each variable
    assert env_vars["SINGLE"] == get_bash_env(env_content, "SINGLE", tmp_path)
    assert env_vars["QUOTED"] == get_bash_env(env_content, "QUOTED", tmp_path)
    assert env_vars["COMMENT"] == get_bash_env(env_content, "COMMENT", tmp_path)
    assert env_vars["MULTI"] == get_bash_env(env_content, "MULTI", tmp_path)
    assert env_vars["AFTER"] == get_bash_env(env_content, "AFTER", tmp_path)


def test_multiline_bash(tmp_path):
    env_content = """SPACE_MULTI='
  spaces
'"""
    env_path = tmp_path / ".env"
    env_path.write_text(env_content)

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = load_dotenv()
    finally:
        os.chdir(old_cwd)

    bash_value = get_bash_env(env_content, "SPACE_MULTI", tmp_path)
    assert result["SPACE_MULTI"] == bash_value


def test_comment_handling_bash(tmp_path):
    env_content = """
WITH_COMMENT=value # comment
WITH_HASH=value#not_a_comment
MULTI='value with # not a comment
second line # still not a comment'
"""
    env_path = tmp_path / ".env"
    env_path.write_text(env_content)

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        env_vars = load_dotenv()
    finally:
        os.chdir(old_cwd)

    for var in ["WITH_COMMENT", "WITH_HASH", "MULTI"]:
        assert env_vars[var] == get_bash_env(env_content, var, tmp_path)


def test_multiple_comments(tmp_path):
    env_content = """
# A comment

# another comment
KEY1=VALUE1

# another comment
KEY2='
    MULTILINEVALUE1
    MULTILINEVALUE2
'
KEY3='
# MULTILINEVALUE1
    
    MULTILINEVALUE2
'
"""
    env_path = tmp_path / ".env"
    env_path.write_text(env_content)

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        env_vars = load_dotenv()
    finally:
        os.chdir(old_cwd)
    print(env_vars)
    for var in ["KEY1", "KEY2", "KEY3"]:
        assert env_vars[var] == get_bash_env(env_content, var, tmp_path)


def test_google_service_acc_env(tmp_path):
    env_content = """
GOOGLE_SERVICE_ACCOUNT='{
  "type": "service_account",
  "private_key_id": "abc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDY3E8o1NEFcjMM\nHW/5ZfFJw29/8NEqpViNjQIx95Xx5KDtJ+nWn9+OW0uqsSqKlKGhAdAo+Q6bjx2c\nuXVsXTu7XrZUY5Kltvj94DvUa1wjNXs606r/RxWTJ58bfdC+gLLxBfGnB6CwK0YQ\nxnfpjNbkUfVVzO0MQD7UP0Hl5ZcY0Puvxd/yHuONQn/rIAieTHH1pqgW+zrH/y3c\n59IGThC9PPtugI9ea8RSnVj3PWz1bX2UkCDpy9IRh9LzJLaYYX9RUd7++dULUlat\nAaXBh1U6emUDzhrIsgApjDVtimOPbmQWmX1S60mqQikRpVYZ8u+NDD+LNw+/Eovn\nxCj2Y3z1AgMBAAECggEAWDBzoqO1IvVXjBA2lqId10T6hXmN3j1ifyH+aAqK+FVl\nGjyWjDj0xWQcJ9ync7bQ6fSeTeNGzP0M6kzDU1+w6FgyZqwdmXWI2VmEizRjwk+/\n/uLQUcL7I55Dxn7KUoZs/rZPmQDxmGLoue60Gg6z3yLzVcKiDc7cnhzhdBgDc8vd\nQorNAlqGPRnm3EqKQ6VQp6fyQmCAxrr45kspRXNLddat3AMsuqImDkqGKBmF3Q1y\nxWGe81LphUiRqvqbyUlh6cdSZ8pLBpc9m0c3qWPKs9paqBIvgUPlvOZMqec6x4S6\nChbdkkTRLnbsRr0Yg/nDeEPlkhRBhasXpxpMUBgPywKBgQDs2axNkFjbU94uXvd5\nznUhDVxPFBuxyUHtsJNqW4p/ujLNimGet5E/YthCnQeC2P3Ym7c3fiz68amM6hiA\nOnW7HYPZ+jKFnefpAtjyOOs46AkftEg07T9XjwWNPt8+8l0DYawPoJgbM5iE0L2O\nx8TU1Vs4mXc+ql9F90GzI0x3VwKBgQDqZOOqWw3hTnNT07Ixqnmd3dugV9S7eW6o\nU9OoUgJB4rYTpG+yFqNqbRT8bkx37iKBMEReppqonOqGm4wtuRR6LSLlgcIU9Iwx\nyfH12UWqVmFSHsgZFqM/cK3wGev38h1WBIOx3/djKn7BdlKVh8kWyx6uC8bmV+E6\nOoK0vJD6kwKBgHAySOnROBZlqzkiKW8c+uU2VATtzJSydrWm0J4wUPJifNBa/hVW\ndcqmAzXC9xznt5AVa3wxHBOfyKaE+ig8CSsjNyNZ3vbmr0X04FoV1m91k2TeXNod\njMTobkPThaNm4eLJMN2SQJuaHGTGERWC0l3T18t+/zrDMDCPiSLX1NAvAoGBAN1T\nVLJYdjvIMxf1bm59VYcepbK7HLHFkRq6xMJMZbtG0ryraZjUzYvB4q4VjHk2UDiC\nlhx13tXWDZH7MJtABzjyg+AI7XWSEQs2cBXACos0M4Myc6lU+eL+iA+OuoUOhmrh\nqmT8YYGu76/IBWUSqWuvcpHPpwl7871i4Ga/I3qnAoGBANNkKAcMoeAbJQK7a/Rn\nwPEJB+dPgNDIaboAsh1nZhVhN5cvdvCWuEYgOGCPQLYQF0zmTLcM+sVxOYgfy8mV\nfbNgPgsP5xmu6dw2COBKdtozw0HrWSRjACd1N4yGu75+wPCcX/gQarcjRcXXZeEa\nNtBLSfcqPULqD+h7br9lEJio\n-----END PRIVATE KEY-----\n",
  "client_email": "123-abc@developer.gserviceaccount.com",
  "client_id": "123-abc.apps.googleusercontent.com",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "http://localhost:8080/token"
}'
"""
    env_path = tmp_path / ".env"
    env_path.write_text(env_content)

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        env_vars = load_dotenv()
    finally:
        os.chdir(old_cwd)

    for var in ["GOOGLE_SERVICE_ACCOUNT"]:
        assert env_vars[var] == get_bash_env(env_content, var, tmp_path)
