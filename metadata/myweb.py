import web

#http://127.0.0.1:7868/

urls = (
  '/', 'index','home'
)


class index:
    def GET(self):
        return "Hello, world! Raghavendra"

class home:
    def GET(self):
        str =  "Hello, world"
        return str

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
