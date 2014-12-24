#!/usr/bin/python

import argparse
from requests import get
from colorama import Fore, Back, Style

parser = argparse.ArgumentParser(description='Show data from amiibro.com.')
parser.add_argument('-n', '--name', help='The name of the Amiibo')
parser.add_argument('-z', '--zipcode', help='The zipcode to check for availability')
parser.add_argument('-r', '--radius', help='The radius around the zipcode to check')
parser.add_argument('-s', '--sellers', nargs='+', default=['all'], help='The retailers that will be displayed')
parser.add_argument('-nn', '--names', action='store_true', help='Get the names of the Amiibos allowed')

args = parser.parse_args()
if (args.name is None or args.zipcode is None) and args.names is False:
    parser.print_help()
    exit(0)


def _print_amiibos(amiibos):
    for amiibo in amiibos:
        print amiibo + ' Product Code NA: ' + str(amiibos[amiibo]['productCode']['na'])
        print amiibo + ' Product Code EU: ' + str(amiibos[amiibo]['productCode']['eu'])
        print amiibo + ' Bestbuy SKU: ' + str(amiibos[amiibo]['bestbuy']['sku'])
        print amiibo + ' Target DPCI :' + str(amiibos[amiibo]['target']['dpci'])
        print amiibo + ' Toys-R-Us SKU ID: ' + str(amiibos[amiibo]['toysrus']['skuId'])
        print amiibo + ' Amazon ASIN: ' + str(amiibos[amiibo]['amazon']['asin'])
        print amiibo + ' Walmart SKU: ' + str(amiibos[amiibo]['walmart']['sku'])
        print amiibo + ' Gamestop SKU: ' + str(amiibos[amiibo]['gamestop']['sku'])
        print '========================'


def _print_item(item, type):
    print type
    print '-------------------------'
    print 'ID: ' + str(item['id'])
    print 'Name: ' + str(item['name'])
    print 'UPC: ' + str(item['upc'])
    print 'Image: ' + str(item['image'])
    print 'Ships to Store: ' + str(item['shipToStore'])
    print 'Free to Ship to Store: ' + str(item['freeToShipToStore'])
    if item['availableOnline'] is False:
        print Fore.RED + 'Available Online: ' + str(item['availableOnline']) + Fore.RESET
    else:
        print Fore.GREEN + 'Available Online: ' + str(item['availableOnline']) + Fore.RESET
    print 'Product URL: ' + str(item['productUrl'])
    print 'Add to Cart URL: ' + str(item['addToCartUrl'])
    print 'Mobile URL: ' + str(item['mobileUrl'])
    print '========================'


def _print_store(store, type):
    print type
    print '-------------------------'
    print 'Store name: ' + str(store['name'])
    print 'Store address: ' + str(store['address'])
    print 'Store address 2: ' + str(store['address2'])
    print 'City: ' + str(store['city'])
    print 'State: ' + str(store['state'])
    print 'Zipcode: ' + str(store['zipcode'])
    print Fore.BLUE + 'Phone: ' + str(store['phone']) + Fore.RESET
    print 'Hours: ' + str(store['hours'])
    print 'Distance: ' + str(store['miles']) + ' miles'
    print '========================'


def _check_data(data, type):
    if len(data.keys()) > 0:
        if data['item'] is not None:
            item = data['item']
            _print_item(item, type)
        if data['stores'] is not None:
            stores = data['stores']
            for store in stores:
                if store['inStoreAvailability'] is True:
                    _print_store(store, type)


def _check_availability(amiibos):
    if any('target' in s for s in args.sellers) or any('all' in s for s in args.sellers):
        _check_data(amiibos['target'], 'Target')
    if any('amazon' in s for s in args.sellers) or any('all' in s for s in args.sellers):
        _check_data(amiibos['amazon'], 'Amazon')
    if any('walmart' in s for s in args.sellers) or any('all' in s for s in args.sellers):
        _check_data(amiibos['walmart'], 'Walmart')
    if any('gamestop' in s for s in args.sellers) or any('all' in s for s in args.sellers):
        _check_data(amiibos['gamestop'], 'Gamestop')
    if any('bestbuy' in s for s in args.sellers) or any('all' in s for s in args.sellers):
        _check_data(amiibos['bestbuy'], 'Bestbuy')
    if any('toysrus' in s for s in args.sellers) or any('all' in s for s in args.sellers):
        _check_data(amiibos['toysrus'], 'Toys-R-Us')


def main():
    if args.names:
        BASE_URL = 'https://amiibro.herokuapp.com/api/amiibos'
        req = get(BASE_URL)
        amiibos = req.json()
        _print_amiibos(amiibos)
    else:
        BASE_URL = 'https://amiibro.herokuapp.com/api/amiibos/status'
        params = {'name': args.name, 'zip': args.zipcode, 'radius': args.radius}
        req = get(BASE_URL, params=params)
        if req.status_code == 200:
            _check_availability(req.json())
        else:
            print req.json()['message']

if __name__ == "__main__":
    main()
