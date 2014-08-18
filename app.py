from flask import Flask, redirect, render_template
import requests
import yaml

config_yaml = yaml.load(file("traffic-cop.yaml"))

app = Flask(__name__)
session_info = {
    'customer_name': config_yaml['user']['org'],
    'user_name': config_yaml['user']['name'],
    'password': config_yaml['user']['password'],
}
headers = {'content-type': 'application/json'}
host = 'https://api.dynect.net/REST'


def get_session():
    return requests.post(host + '/Session/', params=session_info,
                         headers=headers).json()['data']['token']


def get_load_balancers(domain):
    formatted = {}
    for balancer in requests.get(host + '/GSLB/' + domain,
                                 headers=headers).json()['data']:
        formatted[domain] = balancer.split('/')[4].split('.')[:-2]
    return formatted


def get_load_members(zone, fqdn):
    lookup = host + '/LoadBalancePoolEntry/' + zone + '/' + fqdn + '?detail=Y'
    return requests.get(lookup, headers=headers).json()['data']


def get_gslb_members(zone, fqdn):
    lookup = host + '/GSLBRegionPoolEntry/' + zone + '/' + fqdn \
        + 'global?detail=Y'
    return requests.get(lookup, headers=headers).json()['data']


@app.route('/login')
def login():
    headers['Auth-Token'] = get_session()
    return redirect('trafficcop')


@app.route('/logout')
def logout():
    requests.delete(host + '/Session/', headers=headers)
    headers['Auth-Token'] = ''
    return 'Logged out'


@app.route('/trafficcop')
def trafficcop():
    no_dots = []
    for zone in config_yaml['domains']:
        no_dots.append(zone.split('.')[0])
    return render_template('trafficcop.html', zones=no_dots)


if __name__ == '__main__':
    app.run(debug=True)
