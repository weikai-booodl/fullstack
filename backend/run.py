from optparse import OptionParser
from app import create_app

app = create_app("config/default.py")

if __name__ == "__main__":
    parser = OptionParser(add_help_option=False)

    parser.add_option("-h", "--host", dest="host",
                      help="Which hostname to bind to", default='127.0.0.1')

    parser.add_option("-p", "--port", dest="port", type='int',
                      help="Which port to listen on", default=5000)

    parser.add_option("-d", "--debug", dest="debug", action="store_true",
                      help="Runs devserver with debug enabled", default=False)


    options, args = parser.parse_args()

    if options.debug:
        print " * Running in debug mode"

    app.run(debug=options.debug, port=options.port, host=options.host)

