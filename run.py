#run.py is only used to run the application
import ConfigParser
from bop import app


#config can be used to store whichever configuration values. In this case, it stores DEBUG flag, IP, URL and port number settings
@app.route('/config/')
def config():
    str = []
    str.append('Debug:'+app.config['DEBUG'])
    str.append('port:'+app.config['port'])
    str.append('url:'+app.config['url'])
    str.append('ip_address:'+app.config['ip_address'])
    return '\t'.join(str)

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "bop/etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
    except:
        print "Could not read configs from:, config_location"

        init(app)

if __name__ == '__main__':
    init(app)
    app.run(
            host=app.config['ip_address'],
            port=int(app.config['port']))
