import web
import bcrypt
import time
web.config.debug = False

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/manageCustomer', 'ManageCustomer',
    '/createCustomer', 'CreateCustomer',
    '/addAccount/(.*)', 'AddAccount',
    '/editCustomer/(.*)', 'EditCustomer',
    '/deleteCustomer/(.*)', 'DeleteCustomer',
    '/manageAccount', 'ManageAccount',
    '/deleteAccount/(.*)', 'DeleteAccount'
)

db = web.database(dbn='sqlite', db='bankdb')

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Template", base="MainLayout", globals={'sessions': session_data, 'current_user': session_data['user']})


class Home:
    def GET(self):
        if session_data['user']:
            web.seeother('/manageCustomer')
        else:
            return render.Home()

    def POST(self):
        data = web.input()
        myvars = dict(loginid=data.loginid)
        user = db.select("employee", where="loginid=$loginid", vars=myvars, limit=1)
        user = list(user)
        if user:
            print(user[0])
            if bcrypt.checkpw(data.password.encode(), user[0].pw):
                session_data["user"] = user[0]
                web.seeother('/manageCustomer')
                return True
        else:
            web.seeother('/')


class Register:

    def GET(self):
        return render.Register()

    def POST(self):
        data = web.input()
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        user = db.insert('employee', loginid=data.loginid, pw=hashed, post=data.custType)
        if user:
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
        customers = db.select('customer')
        customers = list(customers)
        for customer in customers:
            print(customer)
        return render.ManageCustomer(customers)


class ManageAccount:
    def GET(self):
        accounts = db.select('account')
        accounts = list(accounts)
        return render.ManageAccount(accounts)


class CreateCustomer:
    def GET(self):
        cust = False
        return render.CreateCustomer(cust)

    def POST(self):
        data = web.input()
        cust = db.insert('customer', ssnid=data.ssnid, name=data.name, age=data.age, address=data.address, city=data.city, state=data.state)
        print(cust)
        if cust:
            return render.CreateCustomer(cust)
        else:
            pass


class AddAccount:
    def GET(self, custId):
        acc = str(time.time())
        acc = acc.replace(".", "")
        added = db.insert('account', account_no=acc, customerid=custId, balance=0)
        return web.seeother('/manageCustomer')


class EditCustomer:
    def GET(self, customerId):
        myvars = dict(customerId=customerId)
        customer = db.select("customer", where="customerId=$customerId", vars=myvars, limit=1)
        print(type(customer))
        customer = list(customer)
        print(type(customer))
        return render.EditCustomer(customer)


class DeleteCustomer:
    def GET(self, customerId):
        delCustomer = db.delete('customer', where="customerid=$"+customerId)
        if delCustomer:
            web.seeother('/manageCustomer')

class DeleteAccount:
    def GET(self, account_no):
        delAccount = db.delete('account', where="account_no=$"+account_no)
        if delAccount:
            web.seeother('/manageAccount')






if __name__ == "__main__":
    app.run()
