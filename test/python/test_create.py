#!/usr/bin/python3

import subprocess
import pytest
import os

from utils import create_project


@pytest.fixture(scope="module", params=['cartridge'])
def project_path(request, module_tmpdir):
    return create_project(module_tmpdir, 'project-'+request.param, request.param)


def test_project(project_path):
    process = subprocess.run(['tarantoolctl', 'rocks', 'make'], cwd=project_path)
    assert process.returncode == 0, \
        "Error building project"
    process = subprocess.run(['./deps.sh'], cwd=project_path)
    assert process.returncode == 0, "Installing deps failed"
    process = subprocess.run(['.rocks/bin/luacheck', '.'], cwd=project_path)
    assert process.returncode == 0, "luacheck failed"
    process = subprocess.run(['.rocks/bin/luatest'], cwd=project_path)
    assert process.returncode == 0, "luatest failed"


def test_rocks(tmpdir):
    base_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__), '..', '..')
    )
    process = subprocess.run(['tarantoolctl', 'rocks', 'make', '--chdir', base_dir], cwd=tmpdir)
    assert process.returncode == 0, "tarantoolctl rocks make failed"

    project_name = 'test_project'
    cmd = [
        "cartridge", "create",
        "--name", project_name,
        "--template", 'cartridge'
    ]
    process = subprocess.run(cmd, cwd=tmpdir, env={'PATH': '.rocks/bin'})

    project_path = os.path.join(tmpdir, project_name)
    process = subprocess.run(['tarantoolctl', 'rocks', 'make'], cwd=project_path)
    assert process.returncode == 0, \
        "Error building project"
