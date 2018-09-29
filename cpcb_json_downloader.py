import json
from pprint import pprint
import base64
import argparse
import os
import subprocess

map_file = 'data/cpcb/map.json'
with open(map_file) as f:
    map = json.load(f)


def params_for_site(site_id):
    '''Returns a list of dictionaries of parameters for site.'''
    for params in map['parameters']:
        if params['station_id'] == 'site_' + str(site_id):
            return params['parameters']


def params_dic_to_lists(params):
    """Converts the list of dicts to two separate lists."""
    parameters = []
    parameterNames = []
    for d in params:
        parameters.append(d['id'])
        parameterNames.append(d['name'])

    return parameters, parameterNames


def stringify_list(l):
    """Stiringifies lists into the format specified by the API."""
    return '"' + '","'.join(l) + '"'


def get_str(site, city, state, from_d, to_d, p, pn):
    return '{{"criteria":"15 Minute","reportFormat":"Tabular","fromDate":"{} T00:00:00Z","toDate":"{} T23:59:59Z","state":"{}","city":"{}","station":"site_{}","parameter":[{}],"parameterNames":[{}]}}'.format(
                                                                                        from_d, to_d,                                 state,        city,               site, stringify_list(p), stringify_list(pn))                                                        


def get_data(site, city, state, from_d, to_d):
    """Gets the relevant data from the API, while printing a log."""
    p, pn = params_dic_to_lists(params_for_site(site))
    string = get_str(site, city, state, from_d, to_d, p, pn)
    encoded = base64.b64encode(string.encode())
    # print(string)
    # print(str((encoded)))
    command = "curl -k 'https://app.cpcbccr.com/caaqms/advanced_search' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0' -H 'Accept: q=0.8;application/json;q=0.9' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://app.cpcbccr.com/ccr/' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Connection: keep-alive' --data '{}' > data/cpcb/site_{}_{}_{}.json".format((encoded.decode('ascii')), site, from_d, to_d)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    # print(out[:100], '------')
    # print(command)


def get_stations_in_city(city):
    for st in map['stations']:
        if city == st['cityName']:
            return st['stationsInCity']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ls", type=str,
                        help="List all the stations of a given city prettily.")
    parser.add_argument("site", type=int, help="Integral site_id.", nargs='*')
    parser.add_argument("--from_d", "-f", type=str,
                        help="Starting date in the format DD-MM-YYYY.")
    parser.add_argument("--to_d", "-t", type=str,
                        help="Ending date in the format DD-MM-YYYY.")
    parser.add_argument('--city', '-c', type=str,
                        help="Precise city of the sites.")
    parser.add_argument('--state', '-s', type=str,
                        help="Precise state of the city/sites.")

    args = parser.parse_args()
    if args.ls:
        pprint(get_stations_in_city(args.ls))
    if args.site:
        print("Getting data for {} sites.".format(len(args.site)))
        i = 1
        for site_id in args.site:
            get_data(site_id, args.city, args.state, args.from_d, args.to_d)
            print("Done", i)
            i += 1
    return


if __name__ == "__main__":
    days = {
        1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31
    }
    # sites_arr = [114,117,301,1420,108,1560,104,103,118,1421,1422,116,106,1423,1424,109,1425,122,1561,115,1427,1426,1429,105,1428,1431,125,1563,107,124,1430,113,119,
    sites_arr = [301,106,109]

    def helper(site, i, year):
        print(site, i)
        m = str(i)
        if i < 10:
            m = '0'+m
        get_data(str(site), 'Delhi', 'Delhi', '01-'+m+'-20'+str(year), str(days[i])+'-'+m+'-20'+str(year))
    
    # helper(106, 12, 13)
    # helper(109, 1, 14)
    # helper(109, 2, 14)
    # helper(109, 3, 14)
    # helper(109, 4, 14)

    print(len(sites_arr), "sites to download.")
    for site in sites_arr:
        print("Data for site", site)
        for i in range(1,7):
            print("\t month", i)
            m = str(i)
            if i < 10:
                m = '0'+m
            get_data(str(site), 'Delhi', 'Delhi', '01-'+m+'-2013', str(days[i])+'-'+m+'-2013')
            get_data(str(site), 'Delhi', 'Delhi', '01-'+m+'-2014', str(days[i])+'-'+m+'-2014')
