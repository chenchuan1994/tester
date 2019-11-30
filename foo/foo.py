import os
import time

# father_path = os.path.abspath('.')
# print(father_path)

# current_path = os.path.abspath(__file__)
# print(current_path)

def tag(name, *content, cls = None, **attrs):
    print('---------华丽的分割线---------')
    print('name = {}'.format(name))
    print('content = {}'.format(content))
    print('cls = {}'.format(cls))
    print('attrs = {}'.format(attrs))
    
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s = "%s"' % (attr, value)
                            for attr, value
                            in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


def f(a, *, b):
    return a, b




if __name__ == "__main__":
    # 关键字参数，一定要跟在位子参数后面
    # 1
    print(tag(name = 'br'))
    # 2
    print(tag('p', 'hello'))  # 第一个参数后面的任意个参数会被*content捕获，存入一个元组
    print(tag('p', 'hello', 'nice'))
    # 3
    # 函数标签中，没有明确指定名称的关键字参数会被**attrs捕获，存入一个字典
    print(tag('p', 'hello', id = 33))
    # 4
    # cls参数只能作为关键字参数传入
    print(tag('p', 'hello', 'world', cls = 'sidebar'))
    # 5
    # 即使第一个定位参数也能作为关键字参数传入
    print(tag(content = 'testing', name = 'img'))
    # 6
    # 在字典前面加上**，字典中的所有元素作为单个参数传入，同名建辉绑定到对应的具名参数上，剩下的被**attrs捕获
    my_tag = {'name':'img', 'title':'Sunset Boulevard', 'src':'sunset.jpg', 'cls':'framed'}
    print(tag(**my_tag))

    print(f(1,b= 2))