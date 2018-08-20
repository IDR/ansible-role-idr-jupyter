IDR Jupyter (in development)
============================

Setup a JupyterHub server in Docker.
Uses DockerSpawner to spin up a dedicated container for each user.

Work in progress.
This was moved from an IDR playbook so all vars still reference the IDR.


Dependencies
------------

This role requires Docker to be installed.
For instance, you can use the `openmicroscopy.docker` role.


Role Variables
--------------

All variables are optional:
- `idr_jupyter_ip`: Accessible IP of the server running JupyterHub, default `ansible_default_ipv4.address`, if you have more than one NIC you are strongly recommended to set this, e.g. `ansible_<NIC>.ipv4.address`
- `idr_jupyter_prefix`: The base prefix for JupyterHub, default `/`
- `idr_jupyter_pull_latest`: Always pull the latest notebook image, default `False`
- `idr_jupyter_notebook_image`: The Jupyter notebook docker image
- `idr_jupyter_hub_log_level`: Log level for JupyterHub
- `idr_jupyter_proxy_token`: Persistent token to allow connections to persist over a restart
- `idr_jupyter_cull_options`: List of parameters to be passed to the cull idle servers service, see https://github.com/jupyterhub/jupyterhub/blob/0.9.2/examples/cull-idle/cull_idle_servers.py
- `idr_jupyter_notebook_remove_containers`: Automatically stop and delete containers when the hub is restarted, default `True`
- `idr_jupyter_notebook_system_uid`: UID of the notebook Docker container, default `1000`
- `idr_jupyter_notebook_volumes`: JSON mapping of host volumes to internal notebook docker paths
- `idr_jupyter_users`: List of users that can use JupyterHub, if empty all users will be allowed, default `[root]`
- `idr_jupyter_admins`: List of users with JupyterHub admin privileges, default `[root]`
- `idr_jupyter_additional_config`: Dictionary of additional JupyterHub configuration options

Authentication options: See [defaults/main.yml](defaults/main.yml) for predefined options. Use `idr_jupyter_additional_config` for additional options


Example Playbook
----------------

See [playbook.yml](playbook.yml).
Once deployed you should be able to login to JupyterHub at http://localhost:8000, username: `user`, password `ome`.


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
