# By Martin v1.0.0
# Automatic request sending
# Main(协议,报文内容,替换点,替换内容)
# return value  (URL,Stat_code,content,respon_header)
import re
import requests

class Processing_messages():
    def __init__(self):
        self.__Header = dict()

    def Main(self,protocol,note,tag='',payload='',log=True):
        try:
            note=note.replace(tag,payload)
            method = re.findall(r'(.*?) /', note)[0].lower()
            host = re.findall(r'Host:(.*?)\n', note)[0].strip()
            dir = re.findall(r' (/.*?) ', note)[0]
            body = note.split('\n\n')[-1]
            note = note.split('\n')
        except Exception:
            if log:
                print("The message has errors or the format is correct!")
            return (None,None,None,None)
        else:
            for item in note:
                if ':' in item and 'host' not in item.lower():
                    self.__Header[item.split(':')[0].strip()] = item.split(':')[1].strip()
            url = protocol + '://' + host + dir
            try:
                if 'get' in method:
                        respon = requests.get(url, headers=self.__Header,timeout=5)
                elif 'post' in method:
                    respon = requests.post(url, headers=self.__Header, data=body,timeout=5)
                elif 'put' in method:
                    respon = requests.put(url, headers=self.__Header, data=body, timeout=5)
                elif 'head' in method:
                    respon = requests.head(url, headers=self.__Header, data=body, timeout=5)
                elif 'delete' in method:
                    respon = requests.delete(url, headers=self.__Header, data=body, timeout=5)
                elif 'options' in method:
                    respon = requests.options(url, headers=self.__Header, data=body, timeout=5)
                else:
                    respon = None
            except:
                if log:
                    print("Network error Or the message you provided may have an error!")
                return (None,None,None,None)
            else:
                return (url.replace(dir,''),respon.status_code,respon.text,respon.headers)
