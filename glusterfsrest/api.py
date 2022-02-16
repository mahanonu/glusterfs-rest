# -*- coding: utf-8 -*-
"""
    api.py

    :copyright: (c) 2014 by Aravinda VK
    :license: MIT, see LICENSE for more details.
"""

from flask import render_template
from glusterfsrest.restapp import app, requires_auth, get_post_data
from glusterfsrest.restapp import run_and_response
from glusterfsrest.cli import volume, peer
import yaml
import os


@app.route("/api/<float:version>/doc")
def showdoc(version):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "doc/api-%s.yml" % version)
    apis = yaml.load(open(filename))
    return render_template("doc-%s.html" % version, apis=apis['apis'])


@app.route("/api/<float:version>/volume/<string:name>", methods=["POST"])
def volume_create(version, name):
    bricks_str = get_post_data('bricks', '')
    bricks = [b.strip() for b in bricks_str.split(",")]
    replica = int(get_post_data('replica', 0))
    stripe = get_post_data('stripe', 0)
    transport = get_post_data('transport', 'tcp').lower()
    force = get_post_data('force', False)
    start = get_post_data('start', False)

    return run_and_response(volume.create, [name, bricks, replica,
                                            stripe, transport, force, start])


@app.route("/api/<float:version>/volume/<string:name>", methods=["DELETE"])
def volume_delete(version, name):
    stop = get_post_data('stop', False)
    return run_and_response(volume.delete, [name, stop])


@app.route("/api/<float:version>/volume/<string:name>/start",
           methods=["PUT"])
def volume_start(version, name):
    force = get_post_data('force', False)
    return run_and_response(volume.start, [name, force])


@app.route("/api/<float:version>/volume/<string:name>/stop",
           methods=["PUT"])
def volume_stop(version, name):
    force = get_post_data('force', False)
    return run_and_response(volume.stop, [name, force])


@app.route("/api/<float:version>/volume/<string:name>/restart",
           methods=["PUT"])
def volume_restart(version, name):
    return run_and_response(volume.restart, [name])


@app.route("/api/<float:version>/volumes", methods=["GET"])
def volumes_get(version):
    return run_and_response(volume.info, [])


@app.route("/api/<float:version>/volume/<string:name>", methods=["GET"])
def volume_get(version, name):
    return run_and_response(volume.info, [name])


@app.route("/api/<float:version>/peers", methods=["GET"])
def peers_get(version):
    return run_and_response(peer.info, [])


@app.route("/api/<float:version>/peer/<string:hostname>", methods=["POST"])
def peer_create(version, hostname):
    return run_and_response(peer.attach, [hostname])


@app.route("/api/<float:version>/peer/<string:hostname>", methods=["DELETE"])
def peer_delete(version, hostname):
    force = get_post_data('force', False)
    return run_and_response(peer.detach, [hostname, force])
