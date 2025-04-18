from pathlib import Path
import json
from json import JSONDecodeError

import allure
import curlify
from allure_commons.types import AttachmentType
from requests import Response
from jinja2 import Environment, FileSystemLoader, select_autoescape

templates_path = Path(__file__).parent.parent / 'resources'
new_env = Environment(loader=FileSystemLoader(templates_path), autoescape=select_autoescape())
request_template = new_env.get_template('request.tpl')
response_template = new_env.get_template('response.tpl')


def allure_attach_request(function):
    def wrapper(*args, **kwargs):
        if len(args) > 2:
            method, url = args[1], args[2]

        else:
            method = kwargs.get('method', 'UNKNOWN')
            url = kwargs.get('url', 'UNKNOWN')

        with allure.step(f"{method} {url}"):
            response: Response = function(*args, **kwargs)
            curl = curlify.to_curl(response.request)
            request_data = {'request': response.request, 'curl': curl}
            request_html = request_template.render(request_data)

            allure.attach(
                body=request_html,
                name=f"Request {response.status_code}",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )

            try:
                response_json = response.json()
                response_body = json.dumps(response_json, indent=4)
                allure.attach(
                    body=response_body.encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )

            except (JSONDecodeError, TypeError, ValueError):
                response_body = response.text
                allure.attach(
                    body=response_body.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt"
                )

            response_data = {
                'data': {
                    'responseCode': response.status_code,
                    'url': response.url,
                    'body': response_body,
                    'headers': dict(response.headers),
                    'cookies': dict(response.cookies)
                }
            }

            response_html = response_template.render(response_data)

            allure.attach(
                body=response_html,
                name=f"Response {response.status_code}",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )

        return response

    return wrapper


def attach_sql(cursor, statement, parameters, context):
    statement_with_params = statement % parameters
    name = statement.split(" ")[0] + " " + context.engine.url.database
    allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)
