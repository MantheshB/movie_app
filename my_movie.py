from flask import Flask,render_template,request,redirect,url_for
import pymysql

app=Flask(__name__)


@app.route("/update_action/<int:movie_id>", methods=['GET','POST'])
def update_action(movie_id):
    if request.method=="POST":
        sql="update new_movies.my_movies set movie_name=(%s), timing=(%s), location=(%s) where movie_id=(%s)"
        n=request.form['movie_name']
        print(n)
        args=(request.form['movie_name'], request.form['timing'], request.form['location'],movie_id)
        cur=con.cursor()
        cur.execute(sql,args)
        cur.execute('commit')
    return redirect(url_for('index'))

    #return render_template('index1.html')

@app.route("/update_movie/<int:movie_id>", methods=['GET','POST'])
def update_movie(movie_id):
    if request.method=="POST":
        sql="select * from new_movies.my_movies where movie_id=(%s)"
        args=(movie_id)
        ulist = []
        cur=con.cursor()
        cur.execute(sql, args)
        #ulist=cur.fetchone()
        for item in cur:
            ulist.append(item)

    return render_template('update.html', ulist=ulist)

@app.route("/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    cur=con.cursor()
    sql1="select movie_name from new_movies.my_movies where movie_id=(%s)"
    cur.execute(sql1, movie_id)
    movie_name=cur.fetchone()

    sql="Delete from new_movies.my_movies where movie_id=(%s)"
    cur.execute(sql,movie_id)
    cur.execute("commit")
    #return "<h3>Contact Deleted Successfully</h3>"
    print(movie_name[0])
    return render_template('delete.html', movie_name=movie_name[0])



@app.route('/',methods=['GET','POST'])
def index():
    if(request.method=="POST"):
        #movie_id=request.form["movie_id"]
        movie_name=request.form["movie_name"]
        timing=request.form["timing"]
        location=request.form["location"]
        print(timing)
        sql="INSERT INTO new_movies.my_movies(movie_name,timing,location) VALUES(%s,%s,%s)"
        args=(movie_name,timing,location)
        print(args)
        cur=con.cursor()
        cur.execute(sql,args)
        cur.execute("commit")
    sql='select * from new_movies.my_movies'
    cur=con.cursor()
    cur.execute(sql)
    #print(cur)
    mylist=[]
    for c in cur:
        mylist.append(c)
       # print(mylist)
    return render_template('index.html', mylist=mylist)




con=pymysql.connect(host='localhost',
                    port=3306,
                    user='root',
                    password='admin',
                    db='new_movies'
)

if  __name__=='__main__':
    app.run(debug=True)