# MIT License
# 
# Copyright (c) 2023 OpsMx Corp.  All rights reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
  CLI module for MCP (Managed Cloud Platform).
"""
import argparse
import functools
import json
import os
import time

from ..helper import api
from ..helper import utils

# -----------------------------------------------------------------------------
# Setup logging configuration
# -----------------------------------------------------------------------------
# Usage: in some other module, say mymodule.py, do this:
# 
#   import logging
#   logger = logging.getLogger(__name__)
#
# In func of that mymodule, use logger.debug('Some message to be logged')
#
# Single place to setup logging for all modules
# Typically place this in either __init__.py or in this main cli.py
import logging

_DEFAULT_LOG_LEVEL = logging.DEBUG
_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(level=_DEFAULT_LOG_LEVEL, format=_DEFAULT_LOG_FORMAT)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
_DEFAULT_MAX_ATTEMPTS = 3
_DEFAULT_RETRY_WAIT_IN_SEC = 3
token = None

class CLI:
    """
    Command Line Interface class.
    """

    def __init__(self):
        self.base_url = api.get_base_url()

    def login(self, username: str, password: str) -> str:
        """
        Logs into the MCP.

        :param username: MCP username
        :param password: MCP password
        :return: Authentication token
        """
        global token
        for attempt in range(_DEFAULT_MAX_ATTEMPTS):
            try:
                response = api.login(self.base_url, username, password)
                if response.status_code == 200:
                    token = response.json()['token']
                    logging.info("Login successful.")
                    return token
                else:
                    logging.warning(f"Login failed: {response.content}")
            except Exception as e:
                logging.error(f"Login attempt {attempt + 1} failed: {e}")
                time.sleep(_DEFAULT_RETRY_WAIT_IN_SEC)
        raise Exception("Maximum login attempts exceeded.")

    def logout(self):
        """
        Logs out of the MCP and clears the token.
        """
        global token
        try:
            response = api.logout(self.base_url, token)
            if response.status_code == 200:
                logging.info("Logout successful.")
            else:
                logging.warning(f"Logout failed: {response.content}")
        except Exception as e:
            logging.error(f"Logout failed: {e}")
        finally:
            token = None

    def get_profile(self):
        """
        Fetches the profile data for the authenticated user.
        """
        try:
            response = api.get_profile(self.base_url, token)
            if response.status_code == 200:
                logging.info("Profile fetch successful.")
                return response.json()
            else:
                logging.warning(f"Profile fetch failed: {response.content}")
        except Exception as e:
            logging.error(f"Failed to fetch profile: {e}")

    def get_services(self):
        """
        Fetches the service list from the MCP.
        """
        try:
            response = api.get_services(self.base_url, token)
            if response.status_code == 200:
                logging.info("Services fetch successful.")
                return response.json()
            else:
                logging.warning(f"Services fetch failed: {response.content}")
        except Exception as e:
            logging.error(f"Failed to fetch services: {e}")

    def create_service(self, service_name: str, configuration: dict):
        """
        Creates a new service in the MCP.

        :param service_name: Name of the service
        :param configuration: Configuration for the service
        """
        try:
            response = api.create_service(self.base_url, token, service_name, configuration)
            if response.status_code == 201:
                logging.info("Service creation successful.")
                return response.json()
            else:
                logging.warning(f"Service creation failed: {response.content}")
        except Exception as e:
            logging.error(f"Failed to create service: {e}")
