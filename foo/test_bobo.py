import bobo

@bobo.query('/')
def hello(person):
    print('Hello %s!' % person)

