Dummy servers
=============

Just-enough server programs for testing purposes. Can be used to get libmobile-based programs to unlock features within games without needing fully-fledged servers. Currently tested against mobile trainer's setup stage.

Sample usage with libmobile-bgb
-------------------------------

Make sure python is installed, then run the following in separate terminals (On windows, you can run this without `sudo`):
* `sudo ./dummydns.py`
* `sudo ./dummypop.py`
* `sudo ./http.sh` (optional)

Then run libmobile-bgb as follows:
* `./mobile --dns1 127.0.0.1`

If the default DNS port is already in use, you can specify a different port by running:
* `sudo ./dummydns.py <port>`

And use the `mobile` program as follows:
* `./mobile --dns1 127.0.0.1 --dns_port <port>`
