Dummy servers
=============

Just-enough server programs for testing purposes. Can be used to get libmobile-based programs to unlock features within games without needing fully-fledged servers. Currently tested against mobile trainer's setup stage.

Sample usage with libmobile-bgb
-------------------------------

Make sure python is installed, then run the following in separate terminals:
* `sudo ./dummydns.py`
* `sudo ./dummysmtp.py`
* `sudo ./http.sh` (optional)
(On windows, you can run this without sudo)

Then run libmobile-bgb as follows:
* `./mobile --dns1 127.0.0.1`
