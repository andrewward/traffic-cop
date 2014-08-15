from flask import Flask, flash, redirect, render_template
import requests
import yaml

config_yaml    = yaml.load(file("/Users/award/domains.yaml"))

app = Flask(__name__)
session_info = {
            'customer_name': '',
            'user_name'       : '',
            'password'         : '',
}
headers = {'content-type': 'application/json'}
host = 'https://api.dynect.net/REST'

def get_session():
    return requests.post(host + '/Session/', params=session_info, headers=headers).json()['data']['token']

def get_load_balancers(domain):
    formatted = []
    for domain in requests.get( host + '/GSLB/' + domain, headers=headers).json()['data']:
        formatted.append(domain.split('/')[4])
    return formatted


@app.route('/login')
def login():
    headers['Auth-Token'] = get_session()
    return redirect('trafficcop')

@app.route('/logout')
def logout():
    requests.delete(host + '/Session/', headers=headers)
    headers['Auth-Token'] = ''
    return  'Logged out'

@app.route('/trafficcop')
def trafficcop():
    balancers= []
    for domain in config_yaml['domains']:
        balancers.extend(get_load_balancers(domain))
    return render_template('trafficcop.html', balancers=balancers)


if __name__ == '__main__':
    app.run(debug=True)
