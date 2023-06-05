import requests,sys,os,argparse,textwrap
from package import MartSQLIAPI

VERSION = "@Мартин. MartSQLI Tool V1.0.0"
TITLE='''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is only for learning and experiment. Do not use it for illegal purposes,\n or you will bear corresponding legal responsibilities
************************************************************************************'''

LOGO=f'''
      888b     d888                                 888          .d8888b.        .d88888b.       888           8888888 
      8888b   d8888                                 888         d88P  Y88b      d88P" "Y88b      888             888   
      88888b.d88888                                 888         Y88b.           888     888      888             888   
      888Y88888P888       8888b.       888d888      888888       "Y888b.        888     888      888             888   
      888 Y888P 888          "88b      888P"        888             "Y88b.      888     888      888             888   
      888  Y8P  888      .d888888      888          888               "888      888 Y8b 888      888             888   
      888   "   888      888  888      888          Y88b.       Y88b  d88P      Y88b.Y8b88P      888             888   
      888       888      "Y888888      888           "Y888       "Y8888P"        "Y888888"       88888888      8888888 
                                                                                Github==>https://github.com/MartinxMax    
                                                                                {VERSION}  
'''
def init_loger():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>[{time:HH:mm:ss}]</green><level>[{level}]</level> -> <level>{message}</level>",
        level="INFO"
    )



def main():
    print(LOGO,TITLE)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Basic usage:
            python3 {MSQL} -f /xx/xx/xxx.txt -p <@inject_point> -e <Page Successful Display Tag> #Set Payload
            '''.format(MSQL = sys.argv[0]
                )))
    parser.add_argument('-f', '--FILE', default='',help='Request message file path')
    parser.add_argument('-p', '--POINT', default='', help='Message SQL injection point')
    parser.add_argument('-e', '--ECHO', default='', help='The parameter (-e \'x\') indicates that when Boolean injection occurs,\nthe x character appearing on the page will serve as a criterion for success')
    args = parser.parse_args()
    sqls = MartSQLIAPI.SQLIInformationRetriever()
    sqls.loadfile(args.FILE, args.POINT)
    sqls.method(echo=args.ECHO)
    sqls.setlog()
    sqls.run()


if __name__ == '__main__':
    main()