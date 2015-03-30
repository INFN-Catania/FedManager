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



SITE_URL = "SITE_URL"

OP_INIT_TRANSACTION = "OP_INIT_TRANSACTION"

"""Join/Request Federation"""
OP_SITE_JOIN_FEDERATION_REQUEST = "OP_SITE_JOIN_FEDERATION_REQUEST"
OP_FEDERATOR_JOIN_FEDERATION_SUCCESS = "OP_FEDERATOR_JOIN_FEDERATION_SUCCESS"
OP_FEDERATOR_JOIN_FEDERATION_FAIL = "OP_FEDERATOR_JOIN_FEDERATION_FAIL"
OP_SITE_JOIN_FEDERATION_SEND_INFO = "OP_SITE_JOIN_FEDERATION_SEND_INFO"

STATE_SITE_JOIN_REQUEST_SENT = "STATE_SITE_JOIN_REQUEST_SENT" #The site sent a Federation join Request Message and it is waiting for a Reply"""
STATE_SITE_JOIN_REQUEST_FAILED = "STATE_SITE_JOIN_REQUEST_FAILED" #The site has received a federation join fail from Federation Manager"""
STATE_FEDERATOR_JOIN_REQUEST_SUCCESS = "STATE_FEDERATOR_JOIN_REQUEST_SUCCESS" #The federator has received a federation join request and has replied with a SUCCESS response"""
STATE_FEDERATOR_JOIN_REQUEST_FAILED = "STATE_FEDERATOR_JOIN_REQUEST_FAILED" #The federator has received a federation join request and has replied with a FAILED response"""




"""Resource Request"""
OP_RESOURCE_REQ = "OP_RESOURCE_REQ"
OP_REGISTER_AGREEMENT = "OP_REGISTER_AGREEMENT"




STATE_RES_REQ_SENT = "STATE_RES_REQ_SENT" """The site sent a Resource Request Message and it is waiting for a Best Offer"""
STATE_RES_REQ_RECEIVED = "STATE_RES_REQ_RECEIVED"