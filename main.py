from datetime import datetime, timezone, timedelta
import requests
import os


PUSH_KEY = os.getenv("PUSH_KEY")
KEY_WORD = '查询时间暂未开放'
SSCJCX_URL = "https://gsas.fudan.edu.cn/sscjcx/index"
SSCJCX_B_URL = 'https://gsas.fudan.edu.cn/sscjcx/28198B369067E88DAB9FEFE85484DBF4'

def get_session(_url):
    _session = requests.Session()
    _session.headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x17001229) NetType/WIFI Language/zh_CN miniProgram"

    _response = _session.get(_url)
    _response.encoding = 'utf-8'

    return _response.text


def sscjcx_status():
    if KEY_WORD not in get_session(SSCJCX_URL):
        return 1
    elif KEY_WORD not in get_session(SSCJCX_B_URL):
        return 1
    else:
        return 0


def notify(_title, _message=None):
    if not PUSH_KEY:
        print("未配置PUSH_KEY！")
        return

    if not _message:
        _message = _title

    _response = requests.post(
        f"https://sc.ftqq.com/{PUSH_KEY}.send", {"text": _title, "desp": _message})

    if _response.status_code == 200:
        print(f"发送通知状态：{_response.content.decode('utf-8')}")
    else:
        print(f"发送通知失败：{_response.status_code}")


def main():
    _tz = timezone(+timedelta(hours=8))
    today = datetime.now(_tz).strftime("%Y-%m-%d")
    print(datetime.now(_tz).strftime("%Y-%m-%d %H:%M"))

    if sscjcx_status():
        notify("复旦初始成绩查询开启提示", "已开启查询通道")
    else:
        print("复旦初始成绩查询尚未开启")


if __name__ == "__main__":
    main()
