"""
Repositories fetch and update

This module makes real network and OS interaction,
and the adapters only say how exctly this interaction
should be done.

Configuration parameters:

    * path.log.fetch
"""

from __future__ import print_function

import sys
import logging
import os
import subprocess
import textwrap

from globals import fatal
import adapter
import cache

from config import CONFIG

def _log(*message):
    logging.info(*message)
    if len(message) > 1:
        message = message[0].rstrip("\n") % tuple(message[1:])
    else:
        message = message[0].rstrip("\n")

    sys.stdout.write(message+"\n")

def _run_cmd(cmd):
    shell = isinstance(cmd, str)
    process = subprocess.Popen(
        cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate()[0]
    return process.returncode, output

def fetch_all(skip_existing=True):
    """
    Fetch all known repositories mentioned in the adapters
    """

    def _fetch_locations(known_location):
        for location, adptr in known_location.items():
            if location in existing_locations:
                continue

            cmd = adptr.fetch_command()
            if not cmd:
                continue

            sys.stdout.write("Fetching %s..." % (adptr))
            sys.stdout.flush()
            try:
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    universal_newlines=True)
            except OSError:
                print("\nERROR: %s" % cmd)
                raise
            output = process.communicate()[0]
            if process.returncode != 0:
                sys.stdout.write("\nERROR:\n---\n" + output)
                fatal("---\nCould not fetch %s" % adptr)
            else:
                print("Done")

    # Searching for location duplicates for different repositories
    known_location = {}
    for adptr in adapter.adapter.all_adapters():
        location = adptr.local_repository_location()
        if not location:
            continue
        if location in known_location \
            and adptr.repository_url() != known_location[location].repository_url():
            fatal("Duplicate location: %s for %s and %s"
                  % (location, adptr, known_location[location]))
        known_location[location] = adptr

    # Parent directories creation
    # target subdirectories will be create during the checkout process,
    # but the parent directories should be created explicitly.
    # Also we should make sure, that the target directory does not exist
    existing_locations = []
    for location in known_location:
        if os.path.exists(location):
            if skip_existing:
                existing_locations.append(location)
                print("Already exists %s" % (location))
            else:
                fatal("%s already exists" % location)

        parent = os.path.dirname(location)
        if os.path.exists(parent):
            continue

        os.makedirs(parent)

    known_location = {k:v for k, v in known_location.items() if k not in existing_locations}
    _fetch_locations(known_location)

def _update_adapter(adptr):
    """
    Update implementation.

    If `adptr` returns no update_command(), it is being ignored.
    """
    os.chdir(adptr.local_repository_location())

    cmd = adptr.update_command()
    if not cmd:
        return True

    errorcode, output = _run_cmd(cmd)
    if errorcode:
        _log("\nERROR:\n---%s\n" % output.decode("utf-8") + "\n---\nCould not update %s" % adptr)
        return False

    # Getting current repository state
    # This state will be saved after the update procedure is finished
    # (all cache entries invalidated)
    cmd = adptr.current_state_command()
    state = None
    if cmd:
        errorcode, state = _run_cmd(cmd)
        if errorcode:
            _log("\nERROR:\n---\n" + state + "\n---\nCould not get repository state: %s" % adptr)
            return False
        state = state.strip()

    # Getting list of files that were changed
    # that will be later converted to the list of the pages to be invalidated
    cmd = adptr.get_updates_list_command()
    updates = []
    if cmd:
        errorcode, output = _run_cmd(cmd)
        output = output.decode("utf-8")
        if errorcode:
            _log("\nERROR:\n---\n" + output + "\n---\nCould not get list of pages to be updated: %s" % adptr)
            return False
        updates = output.splitlines()

    entries = adptr.get_updates_list(updates)
    if entries:
        _log("%s Entries to be updated: %s", adptr, len(entries))

    name = adptr.name()
    for entry in entries:
        cache_name = name + ":" + entry
        _log("+ invalidating %s", cache_name)
        cache.delete(cache_name)

    if entries:
        _log("Done")

    adptr.save_state(state)
    return True

def update_all():
    """
    Update all known repositories, mentioned in the adapters
    and fetched locally.
    If repository is not fetched, it is skipped.
    """

    for adptr in adapter.adapter.all_adapters():
        location = adptr.local_repository_location()
        if not location:
            continue
        if not os.path.exists(location):
            continue

        _update_adapter(adptr)

def update_by_name(name):
    """
    Find adapter by its `name` and update only it.
    """
    pass

def _show_usage():
    sys.stdout.write(textwrap.dedent("""
        Usage:

            python lib/fetch.py [command]
        
        Commands:
        
            update-all      -- update all configured repositories
            update [name]   -- update repository of the adapter `name`
            fetch-all       -- fetch all configured repositories

    """))

def main(args):
    """
    function for the initial repositories fetch and manual repositories updates
    """

    if not args:
        _show_usage()
        sys.exit(0)

    logdir = os.path.dirname(CONFIG["path.log.fetch"])
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logging.basicConfig(
        filename=CONFIG["path.log.fetch"],
        level=logging.DEBUG,
        format='%(asctime)s %(message)s')

    if args[0] == 'fetch-all':
        fetch_all()
    elif args[0] == 'update':
        update_by_name(sys.argv[1])
    elif args[0] == 'update-all':
        update_all()
    else:
        _show_usage()
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
