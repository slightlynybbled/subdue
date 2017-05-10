

def get_host(args):
    if '-h' in args:
        index = args.index('-h') + 1
    elif '--host' in args:
        index = args.index('--host') + 1
    else:
        index = None

    host = args[index] if index else '127.0.0.1'

    return host


def get_port(args):
    if '-p' in args:
        index = args.index('-p') + 1
    elif '--port' in args:
        index = args.index('--port') + 1
    else:
        index = None

    port = int(args[index]) if index else 5001

    return port

if __name__ == '__main__':
    args = ['-h', '127.0.0.1', '--port', '2000']

    print(get_host(args))
    print(get_port(args))