import json
from typing import NoReturn

import requests
import logging

logger = logging.getLogger(__name__)


def parse_output(r: requests.Response, key: str = None) -> str:
    logger.info("api response: status_code:'%d':", r.status_code)

    complete_output = ''

    for line in r.iter_lines():
        body = json.loads(line)
        if 'error' in body:
            raise Exception(body['error'])

        if key:
            complete_output += body[key]
        else:
            logger.info(body)
        if body.get('done', False):
            if complete_output:
                logger.info("response:\n%s", complete_output)
                return complete_output
            return body['context']
