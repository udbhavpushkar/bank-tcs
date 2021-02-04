import web
import bcrypt
web.config.debug = False

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/manageCustomer', 'ManageCustomer',
    '/createCustomer', 'CreateCustomer'
)

db = web.database(dbn='sqlite', db='bankdb')

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Template", base="MainLayout", globals={'sessions': session_data, 'current_user': session_data['user']})
'''
create table customer(
    -> SSNID varchar(25) NOT NULL,
    -> Name varchar(25),
    -> Age varchar(3),
    -> Address_Line1 varchar(300),
    -> Address_Line2 varchar(300),
    -> City varchar(25),
    -> State varchar(25),
    -> createdate varchar(25),
    -> CustomerID varchar(25),
    -> Unique(SSNID),
    -> Primary Key(CustomerID));


create table Account(
    -> Account_No varchar(25),
    -> Balance varchar(25),
    -> createdate varchar(25),
    -> CustomerID varchar(25),
    -> Primary Key(Account_No),
    -> Foreign Key(CustomerID) references customer(CustomerID));

create table Transaction(
    -> Source_Acc_No varchar(25) NOT NULL,
    -> Destination_Acc_No varchar(25) NOT NULL,
    -> Transaction_ID varchar(25),
    -> Last_Balance varchar(25),
    -> Updated_Balance varchar(25),
    -> createdate varchar(25),
    -> Primary Key(Transaction_ID));
'''


class Home:
    def GET(self):
        # q = 'CREATE TABLE employee (id integer primary key, loginid text, pw text, post text, created default current_timestamp)'
        # db.query(q)
        # q1 = 'CREATE TABLE'

        if session_data['user']:
            web.seeother('/manageCustomer')
        else:
            return render.Home()


class Register:
    def POST(self):
        data = web.input()
        # print(data.loginid + " Password : " + data.password)
        # q = 'CREATE TABLE employee (id integer primary key, loginid text, pw text, post text, created default
        # current_timestamp)'
        # db.query(q)
        # if bcrypt.checkpw()
        # hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        # user = db.insert('employee', loginid=data.loginid, pw=hashed)
        # print(user)
        return data


class Login:
    def POST(self):
        data = web.input()
        myvars = dict(loginid=data.loginid)
        user = db.select("employee", where="loginid=$loginid", vars=myvars, limit=1)

        user = list(user)
        if user:
            print(user[0])
            if bcrypt.checkpw(data.password.encode(), user[0].pw):
                session_data["user"] = user[0]
                return True
        return False


class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        web.seeother('/')
        print(session)


class ManageCustomer:
    def GET(self):
        return render.ManageCustomer()


class CreateCustomer:
    def GET(self):
        return render.CreateCustomer()


if __name__ == "__main__":
    app.run()
