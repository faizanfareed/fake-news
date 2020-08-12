from flask import Flask, request, jsonify,render_template 


from flask_mongoengine import MongoEngine

from databases.models import *

app = Flask(__name__)


db = MongoEngine()

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://127.0.0.1/d'
}

db.init_app(app)



@app.route('/',methods=['GET','POST']) 
def index_page():

   
    print(request.method)
    #print(request.user_agent)
    #print(dir(request))
    data = request.form.get('data')
    print(data)

    
    return jsonify('Index Page')
    
@app.route('/fakenews',methods=['POST'])    
def addFakenews():

    title = request.form.get('title')
    body = request.form.get('body')

    if body  and title :
        post = FakeNews(title=title, body=body,).save()
        return 'POST added successfully.'       
    else:
        return jsonify('Fields are missing.')


@app.route('/fakenews',methods=['GET'])    
def getFakenewslist():
    posts = FakeNews.objects()

    if posts:
        return jsonify(posts)
    else:
        return jsonify('No posts existed.')  
    
    

@app.route('/fakenews/id/<string:id>',methods=['GET'])        
def getFakenews(id):
    try:
        post = FakeNews.objects(id=id).get()

        fakecounts = VoteFakeNews.objects(post=id)
        return jsonify(post,fakecounts)

    except Exception as e :
        return  jsonify(str(e))

    
@app.route('/fakenews/id/<string:id>',methods=['DELETE'])    
def deleteFakenews(id):
    try:
        post = FakeNews.objects(id=id).delete()
        VoteFakeNews.objects(post=id).delete()

        return jsonify('Post Deleted successfully.')
    except Exception as e :
        return  jsonify(str(e))

    

@app.route('/fakenews/id/<string:id>',methods=['PUT'])    
def updateFakenews(id):

    title = request.form.get('title')
    body = request.form.get('body')

    if (body is None or body == '') and ( title is None or title == '') :
        return jsonify('Update fields are empty or none.')
    else:
        try:
            post = FakeNews.objects(id=id).get()

            if post.isTitleChanged(title) and post.isBodyChanged(body):
                
                post.update(
                    title=title,
                    body=body
                )
                return jsonify('Post title and body updated successfully.')
            elif post.isTitleChanged(title):
                
                post.update(
                    title=title 
                )
                return jsonify('Post title updated successfully.')

            elif post.isBodyChanged(body):
                
                post.update(
                    body=body
                )
                return jsonify('Post body updated successfully.')
            else:
                return jsonify('Post is not updated.')  

        except Exception as e :
            return  jsonify(str(e))


@app.route('/fakenews/user',methods=['POST'])    
def adduser():

    fullname = request.form.get('fullname')
    email = request.form.get('email')


    if fullname  and email :

        try:
            user = User(full_name=fullname,email=email).save()
            return jsonify('User Created Successfully.')
        except Exception as e:
            return jsonify(str(e))    
    
    else:
        return jsonify('User not created.')



@app.route('/fakenews/markfakenews/id/<string:id>',methods=['POST'])    
def markfakenews(id):

    is_fake = request.form.get('is_fake')

    if is_fake:
        is_fake = is_fake.lower()

        if is_fake in ('true','false'):
            try:
                post = FakeNews.objects(id=id).get()
    
                VoteFakeNews(post=post, is_fake=is_fake).save()

                return jsonify('Post is marked successfully.')

            except Exception as e:
                return jsonify(str(e))    
        else:
            return jsonify('Bool value required.')

    else:
        return jsonify('Bool value required.')
    
   
   

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8000')