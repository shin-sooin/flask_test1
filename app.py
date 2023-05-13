from flask import Flask, request, redirect

app=Flask(__name__)


# Use variable rules
nextId=4
topics=[
    {'id':1, 'title':'html', 'body':'html is ...'},
    {'id':2, 'title':'css', 'body':'css is ...'},
    {'id':3, 'title':'javascript', 'body':'javascript is ...'}
]


# html폼을 리턴하는 함수
def template(contents, content, id=None):
    contextUI=''
    if id!=None:
        contextUI=f'''
            <li><a href='/update/{id}/'>update</a></li>
            <li><form action='/delete/{id}/' method='POST'><input type='submit' value='delete'></form></li>
        '''

    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

# variable을 읽어서 li tag를 리턴해주는 함수
def getContents():
    liTags=''
    for topic in topics:
        liTags=liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags


@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')


# 파라미터를 int로 받기 위해서 타입캐스팅
@app.route('/read/<int:id>/')
def read(id):
    title=''
    body=''
    for topic in topics:
        if id==topic['id']:
            title=topic['title']
            body=topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)


@app.route('/create/', methods=['GET','POST'])
def create():
    if request.method =='GET':
        content='''
            <form action='/create/' method='POST'>
                <p><input type='text' name='title' placeholder='title'></p>
                <p><textarea name='body' placeholder='body'></textarea></p>
                <p><input type='submit' value='create'></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method=='POST':
        # 전역변수의 값을 수정할 때는 사용하는 코드 전에 이렇게 전역변수임을 알려줘야함
        global nextId
        title=request.form['title']
        body=request.form['body']
        newTopic={'id':nextId,'title':title, 'body':body}
        topics.append(newTopic)
        url='/read/'+str(nextId)+'/'
        nextId=nextId+1
        return redirect(url)


app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method =='GET':
        title=''
        body=''
        for topic in topics:
            if id==topic['id']:
                title=topic['title']
                body=topic['body']
                break
        content=f'''
            <form action='/update/{id}/' method='POST'>
                <p><input type='text' name='title' placeholder='title' value='{title}'></p>
                <p><textarea name='body' placeholder='body'>{body}</textarea></p>
                <p><input type='submit' value='update'></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method=='POST':
        # 전역변수의 값을 수정할 때는 사용하는 코드 전에 이렇게 전역변수임을 알려줘야함
        global nextId
        title=request.form['title']
        body=request.form['body']
        for topic in topics:
            if id==topic['id']:
                topic['title']=title
                topic['body']=body
                break
        url='/read/'+str(nextId)+'/'
        return redirect(url)


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id==topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

@app.route('/testing/<int:id>', methods=['GET','POST'])
def testing(id):
    if id==0:
        return 'object detection mode'
    else:
        return 'ocr mode'

if __name__=='__main__':
    app.run(debug=True, port=5001)
