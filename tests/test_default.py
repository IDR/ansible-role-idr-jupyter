import testinfra.utils.ansible_runner
import pytest

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

# TODO: check notebook container runs after login
