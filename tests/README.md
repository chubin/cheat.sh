# Testing

## Setup

### If you're on macOS

It may be helpful to have GNU diffutils (for a mondern `diff`), GNU coreutils (for `realpath`), and GNU `sed` installed.

    $ brew install diffutils
    $ brew install coreutils
    $ brew install gnu-sed

### Install the Python dependencies

    $ pip3 install --user -r ../requirements.txt

### Update your local `tests/results/*` files

    $ FORCE_COLOR=1 CHEATSH_UPDATE_TESTS_RESULTS=YES bash ./run-tests.sh

## Running tests

To run unit tests.

    $ python3 -m pytest -v ../lib/

To run input/output tests.

    ## run the "standalone" tests
    $ FORCE_COLOR=1 bash ./run-tests.sh

Or:

    ## run the "local server" tests
    $ python3 ../bin/srv.py &
    $ FORCE_COLOR=1 CHEATSH_TEST_STANDALONE=NO bash ./run-tests.sh

You can also skip the "online" tests by adding `CHEATSH_TEST_SKIP_ONLINE=yes` to your `./run-tests.sh` command.

### A note about `FORCE_COLOR=1`as used above.

Until the future of `cheat.sh` testing has been decided, setting the environment variable `FORCE_COLOR=1` is necessary to work around some inconsistencies caused by recent changes in the Python dependency `colored`.
