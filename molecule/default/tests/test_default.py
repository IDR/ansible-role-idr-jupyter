import os
import testinfra.utils.ansible_runner
import json
import pytest
from time import sleep

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_services_running_and_enabled(host):
    assert host.service('jupyterhub').is_running
    assert host.service('jupyterhub').is_enabled


@pytest.mark.parametrize("password,status", [
    ("ome", True),
    ("incorrect", False),
])
def test_login(host, password, status):
    out = host.check_output(
        'curl -L --data %s %s',
        'username=user&password=%s&submit=Sign+In' % password,
        'http://localhost:8000/jupyter/hub/login?next=')
    assert ('login_error' not in out) == status


def apicall(host, method, token, api):
    out = host.check_output(
        'curl -X %s -H "Authorization: token %s" '
        'http://localhost:8000/jupyter/hub/api/%s' % (method, token, api))
    if out:
        return json.loads(out)


def test_server(host):
    with host.sudo():
        token = host.check_output(
            'cd /srv/jupyterhub && '
            '/opt/jupyter/venv/bin/jupyterhub token user')
    assert token

    apicall(host, 'POST', token, '/users/user/server')
    # Image is already pulled so should be pretty quick
    for c in range(12):
        sleep(5)
        userinfo = apicall(host, 'GET', token, '/users/user')
        servers = userinfo['servers']
        if servers and servers[''] and not servers['']['pending']:
            break
    assert servers['']['ready']

    apicall(host, 'DELETE', token, '/users/user/server')
    for c in range(12):
        sleep(5)
        userinfo = apicall(host, 'GET', token, '/users/user')
        if not userinfo['servers']:
            break
    assert not userinfo['servers']
