import json
import urllib2
import argparse

# http://xbmc:xbmc@mr-saturn.local:8080/jsonrpc

FORMAT_360P = "360p"
FORMAT_480P = "480p"
FORMAT_720P = "720p"
FORMAT_LIVE = "live"

FORMAT_DICT = {'live': FORMAT_LIVE, 
               '360': FORMAT_360P,
               '360p': FORMAT_360P,
               '480': FORMAT_480P,
               '480p': FORMAT_480P,
               '720': FORMAT_720P,
               '720p': FORMAT_720P}

def load_jtv_url(hostname, user, fmt, port='8080'):
    json_version = '{ "jsonrpc": "2.0", "method": "JSONRPC.Version", "id": 1 }'
    json_play = ('{"jsonrpc": "2.0",'
                 ' "method": "Player.Open",'
                 ' "params":{"item":'
                 ' {"file" : "plugin://plugin.video.jtv.archives/?url=&mode=2&name=%s&quality=%s" }},'
                 ' "id" : "1"}' % (user, fmt))

    print(json_play)

    req_version = urllib2.Request('http://%s:%s/jsonrpc'%(hostname, port))
    req_version.add_header('Content-type', 'application/json')

    req_play = urllib2.Request('http://%s:%s/jsonrpc'%(hostname, port))
    req_play.add_header('Content-type', 'application/json')

    urllib2.urlopen(req_version, json_version)
    urllib2.urlopen(req_play, json_play)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load up a JTV url on xbmc with the command line')
    parser.add_argument('--format', '-f',
                        default='live', 
                        help='Playback format for the stream. (available: live, 360, 480, 720)')
    parser.add_argument('--hostname', '-n', 
                        help='Hostname of the XBMC server to open JTV stream on. Default is the server entered in the configuration file, or localhost.')
    parser.add_argument('jtv_username',
                        help='The name of the JTV user whose channel to watch')

    args = parser.parse_args()

    hostname = args.hostname
    if hostname is None:
        hostname = 'mr-saturn.local' #Cheating

    try:
        fmt = FORMAT_DICT[args.format]
    except:
        pass

    load_jtv_url(hostname, args.jtv_username, fmt)
