from django.db.backends.postgresql import base
import os
import stat
import pathlib

def maybe_write_ssl_files():
    # Need to pass ssl keys to as filepaths - but they are stored as env variables
    # So write them from env vars to ssl dir
    # Only write if they don't already exist or if the keys in the files are different

    base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent / "ssl"

    if not os.path.exists(base_path):
        os.mkdir(base_path)
    for env_var, filename in [
        ("SSL_CA_PEM", "ca.pem"),
        ("SSL_CLIENT_PEM", "client.pem"),
        ("SSL_CLIENT_KEY_PEM", "client-key.pem"),
    ]:
        filepath = os.path.join(base_path, filename)
        write_file = False
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                existing_file = f.read()
            if existing_file != os.environ[env_var]:
                write_file = True
        else:
            write_file = True

        if write_file:
            with open(filepath, "w") as f:
                f.write(os.environ[env_var])
        
        if env_var == "SSL_CLIENT_KEY_PEM":
            try:
                os.chmod(filepath, stat.S_IREAD | stat.S_IWRITE)
            finally:
                pass

class DatabaseWrapper(base.DatabaseWrapper):
    def get_new_connection(self, conn_params):
        maybe_write_ssl_files()
        return super().get_new_connection(conn_params)
