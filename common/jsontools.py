'''
  @Description      
  @auther         leizi
'''
from flask import jsonify
from typing import Union
def reponse(*, code=1,data: Union[list, dict, str]=None, message="message"):
    return jsonify({
            'code': code,
            'message': message,
            'data': data,
        }
    )
