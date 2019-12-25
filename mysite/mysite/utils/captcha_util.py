#!/usr/bin/env python3
# !-*-coding:utf-8 -*-

# 验证码需要导入的模块
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# 创建验证码
def build_captcha():
    hash_key = CaptchaStore.generate_key()   # 验证码答案
    image_url = captcha_image_url(hash_key)  # 验证码地址
    captcha = {'hash_key': hash_key, 'image_url': image_url}
    return captcha


def judge_captcha(captcha_str, captcha_hash_key):
    if captcha_str and captcha_hash_key:
        try:
            # 获取根据hash_key获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captcha_hash_key)
            if get_captcha.response == captcha_str.lower():     # 如果验证码匹配
                return True
        except Exception as e:
            return False
    else:
        return False