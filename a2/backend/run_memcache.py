import memcache
# read port from command line
if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])
    print(port)
    memcache.webapp.run(host='0.0.0.0', port=port, debug=True)
