IDR Jupyter (in development)
============================

Setup a JupyterHub server in Docker.
Uses DockerSpawner to spin up a dedicated container for each user.

Work in progress.
This was moved from an IDR playbook so all vars still reference the IDR.


Role Variables
--------------

See `defaults/main.yml` for defaults.
All variables are optional.
Some of the most useful ones are:
- `idr_jupyter_hub_image`: The Jupyterhub docker image
- `idr_jupyter_notebook_image`: The Jupyter notebook docker image
- `idr_jupyter_notebook_volumes`: JSON mapping of host volumes to internal notebook docker paths
- `idr_jupyter_users`: List of users that can use Jupyterhub
- `idr_jupyter_admins`: List of users with Jupyterhub admin privileges
- `idr_jupyter_urlbase`: The base for URLs created by Jupyterhub


Example Playbook
----------------

See [playbook.yml](playbook.yml).
Once deployed you should be able to login to JupyterHub at http://localhost:8000, username: `user`, password `ome`.


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
