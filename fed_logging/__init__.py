"""
  Copyright 2015 INFN (Italy)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""
__author__ = 'maurizio'
import logging, logging.config
import StringIO
import pprint

class PrettyDictionary(dict):
    def __str__(self):
        out = StringIO.StringIO()
        pprint.pprint(self,out)
        return out.getvalue()



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s --- applicant %(applicant)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s --- %(args)s'
        },
    },
    'filters': {

    },
    'handlers': {

        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        }

    },
    'loggers': {
       'federation.core.federator': {
            'handlers': ['console'],
            'level': 'DEBUG',

        }
    }
}

logging.config.dictConfig(LOGGING)

