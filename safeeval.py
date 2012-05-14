#encoding=utf-8
#code by G
#2010-11-20
'''
为序列化操作提供安全转换。
对eval数据进行词法分析，确保eval的数据中不会包含不合法的TRUE等写法，
并且在隔离、安全的环境执行eval。
用法：
myobj = safe_eval(eval_str)
'''

import re

def safe_eval(eval_str,**kw):
    '''
    安全eval，确保eval的内容是合法的，并且隔离的。
    **kw不可用，以后扩展为可定义命名空间。
    '''
    #callback functions
    def start_structure(scanner, token): return "start structure", token
    def key(scanner, token):   return "key", token
    def value(scanner, token): 
        #非法写法
        if token.lower() == 'true'and token != 'True':
            raise 'value Error "%s"'%token
    def str_value(scanner,token):   
        return "string value",token
    def end_structure(scanner, token):  return "end start structure",token
        
    scanner = re.Scanner([
        (r"[{\[(]", start_structure),
        (r"[\w]+\s*:", key),
        (r"['\"][^'\"]+['\"]",str_value),
        (r"[\w]+", value),
        (r"\s*,\s*",None),
        (r"[})\]]", end_structure),
    ])
 
    tokens, remainder = scanner.scan(eval_str)
    for token in tokens:
        print token
    #make a list of safe functions
    safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'de grees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
    #use the list to filter the local namespace s
    safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
    #add any needed builtins back in.
    #由于所有内置的对象被屏蔽 __builtins__中的所有对象不可使用，所以True、False需要单独定义
    #加入命名空间
    safe_dict['True'] = True
    safe_dict['False'] = False
    return eval(eval_str,{'__builtins__':None},safe_dict)

def test_ok():
    print safe_eval("{1:'true',2:123,3:(True,[True])}")
    
def test_bad():
    print safe_eval("{1:'true',2:123,3:(True,[true])}")

def test_bad2():
    print safe_eval("__import__('os').system('dir')")
    

if __name__ == '__main__':
    print eval("{1:'true',2:123,3:(True,[True])}")
    

