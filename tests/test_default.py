import testinfra.utils.ansible_runner
import pytest
import json
from time import sleep

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_services_running_and_enabled(Service):
    assert Service('jupyterhub').is_running
    assert Service('jupyterhub').is_enabled


@pytest.mark.parametrize("password,status", [
    ("ome", True),
    ("incorrect", False),
])
def test_login(Command, password, status):
    out = Command.check_output(
        'curl -L --data %s %s',
        'username=user&password=%s&submit=Sign+In' % password,
        'http://localhost:8000/jupyter/hub/login?next=')
    assert ('login_error' not in out) == status


def apicall(Command, method, token, api):
    out = Command.check_output(
        'curl -X %s -H "Authorization: token %s" '
        'http://localhost:8000/jupyter/hub/api/%s' % (method, token, api))
    if out:
        return json.loads(out)


def test_server(Sudo, Command):
    with Sudo():
        token = Command.check_output(
            'cd /srv/jupyterhub && '
            '/opt/jupyter/venv/bin/jupyterhub token user')
    assert token

    apicall(Command, 'POST', token, '/users/user/server')
    # Image is already pulled so should be pretty quick
    for c in xrange(12):
        sleep(5)
        userinfo1 = apicall(Command, 'GET', token, '/users/user')
        server = userinfo1['servers']['']
        if not server['pending']:
            break
    assert server['ready']

    apicall(Command, 'DELETE', token, '/users/user/server')
    userinfo2 = apicall(Command, 'GET', token, '/users/user')
    assert not userinfo2['servers']
