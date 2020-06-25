import configparser
import getpass
import sys
from configparser import ConfigParser, SectionProxy
from typing import Optional

from fabric import Connection, task
from fabric.util import get_local_user
from invoke.context import Context
from invoke.exceptions import Failure, ThreadException, UnexpectedExit
from paramiko.ssh_exception import AuthenticationException

COLOUR_OFF: str = "\033[0m"


def error(message: str):
    red: str = "\033[31m"

    print()
    print(f"{red}{message}{COLOUR_OFF}")


def info(message: str):
    blue: str = "\033[34m"

    print()
    print(f"{blue}{message}{COLOUR_OFF}")


cfg: ConfigParser = configparser.ConfigParser()
cfg.read("setup.cfg")

try:
    fabric_cfg: SectionProxy = cfg["fabric"]

    BRANCH = fabric_cfg["default_branch"]
    COMPOSE_CMD = fabric_cfg["compose_cmd"]
    GATEWAY = fabric_cfg["gateway"]
    HOST = fabric_cfg["host"]
    HOST_PATH = fabric_cfg["host_path"]
    INSTANCE = fabric_cfg["default_instance"]
    PROJECT = fabric_cfg["project"]
    REPOSITORY = fabric_cfg["repository"]
    STACK = fabric_cfg["default_stack"]
except KeyError:
    error("Invalid fabric configuration in `setup.cfg`")
    sys.exit(-1)

HELP = {
    "app": "App to run the tests. Omit to run all the project tests.",
    "backup": "Backup file name.",
    "branch": "Source control branch to checkout.",
    "command": "Django management command.",
    "coverage": "Set to `True` to run test coverage.",
    "Images": "Images to be removed, by default all images are removed.",
    "initial": "Set to `True` for first time deployments.",
    "instance": (
        "Server instance where to run the task, can be left empty when running "
        "local tasks."
    ),
    "remote": "Set to `True` to run the command on the remote host.",
    "service": "Service name to run the task.",
    "services": "Service names to run the task. Separate multiple services with space.",
    "stack": "Docker stack for docker commands.",
    "volumes": "Set to `True` to remove volumes.",
    "orphans": "Set to `True` to remove orphan containers.",
}


connection: Connection = None
password: str = None


@task(help=HELP)
def deploy(
    context, instance, user=get_local_user(), initial=False, stack=None, branch=BRANCH,
):
    """
    Deploy the project. By default it creates a database backup before updating from
    source control and rebuilding the docker stack.
    """
    remote = True

    if initial:
        clone(context, instance, user, branch)
    else:
        backup(context, user, remote, instance, stack)

    update(context, user, remote, instance, branch)
    up(context, user, remote, instance, stack)


@task(help=HELP)
def clone(context, instance, user=get_local_user(), branch=BRANCH):
    """
    Clone the project repository into a host instance.
    """
    local = False
    no_stack = None
    no_compose = False

    env_path = f"{HOST_PATH}/{instance}/.envs"
    env_file = f"{instance}.tar.gz"

    command = f"tar czvf .envs/{env_file} .envs/.{instance}"
    run_command(context, user, local, instance, no_stack, command, no_compose)

    with get_connection(user, HOST) as c:
        with c.cd(f"{HOST_PATH}"):
            c.run(f"mkdir -p {HOST_PATH}/{instance}")

    remote = True

    command = f"git clone {REPOSITORY} . && git checkout {branch}"
    run_command(context, user, remote, instance, no_stack, command, no_compose)

    with get_connection(user, HOST) as c:
        c.put(f".envs/{env_file}", env_path)

    command = f"tar zxvf {env_path}/{env_file} && rm {env_path}/{env_file}"
    run_command(context, user, remote, instance, no_stack, command, no_compose)

    command = f"mkdir -p {PROJECT}/media"
    run_command(context, user, remote, instance, no_stack, command, no_compose)


def run_command(
    context: Context,
    user: str,
    remote: bool,
    instance: Optional[str],
    stack: Optional[str],
    command: str,
    compose: bool = True,
):
    host = get_host(remote)
    instance = get_instance(remote, instance)
    stack = get_stack(remote, instance, stack)

    if compose:
        command = f"{COMPOSE_CMD} -f {stack} {command}"

    info(f"{host}/{instance}/{stack}\n{command}")

    try:
        if remote:
            with get_connection(user, HOST) as c:
                with c.cd(f"{HOST_PATH}/{instance}"):
                    c.run(command, pty=True)
        else:
            context.run(command, replace_env=False, pty=True)
    except (AuthenticationException, ValueError) as e:
        error(f"{e}")
    except (Failure, ThreadException, UnexpectedExit):
        error(f"{host}/{instance}\nFailed to run command: `{command}`")


def get_host(remote: bool):
    if remote:
        return HOST

    return "local"


def get_instance(remote: bool, instance: Optional[str]):
    if instance:
        return instance

    if remote:
        return INSTANCE

    return "local"


def get_stack(remote: bool, instance: str, stack: Optional[str]) -> str:
    if stack:
        return f"{stack}.yml"

    if instance != "local":
        return f"kdl_{instance}.yml"

    if remote:
        return STACK

    return "local.yml"


def get_connection(user: str, host: str) -> Connection:
    global connection

    if connection:
        return connection

    try:
        connection = Connection(host, user=user, gateway=get_gateway(user))
        if not connection.is_connected:
            raise AuthenticationException
    except AuthenticationException:
        password = get_password(user, host)

        connection = Connection(
            host,
            user=user,
            connect_kwargs={"password": password},
            gateway=get_gateway(user, password),
        )

    return connection


def get_gateway(user: str, password: Optional[str] = None) -> Connection:
    if password:
        return Connection(GATEWAY, user=user, connect_kwargs={"password": password})

    return Connection(GATEWAY, user=user)


def get_password(user: str, host: str) -> str:
    global password

    if password:
        return password

    password = getpass.getpass(prompt=f"Password for {user}@{host}: ")

    return password


@task(help=HELP)
def backup(context, user=get_local_user(), remote=False, instance=None, stack=None):
    """
    Create a database backup.
    """
    command = f"run --rm postgres backup"
    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def update(context, user=get_local_user(), remote=False, instance=None, branch=BRANCH):
    """
    Update the host instance from source control.
    """
    no_stack = None
    no_compose = False

    command = f"git checkout {branch} || git pull && git checkout {branch}"
    run_command(context, user, remote, instance, no_stack, command, no_compose)

    command = f"git pull"
    run_command(context, user, remote, instance, no_stack, command, no_compose)


@task(help=HELP)
def up(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    services=None,
):
    """
    Build the stack for the host instance.
    """
    command = f"up --build"

    if remote:
        command = f"{command} --detach"

    run_command_with_services(context, user, remote, instance, stack, command, services)


def run_command_with_services(
    context: Context,
    user: str,
    remote: bool,
    instance: str,
    stack: str,
    command: str,
    services: Optional[str],
):
    if services:
        command = f"{command} {services}"

    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def down(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    images="all",
    volumes=True,
    orphans=False,
):
    """
    Stop and remove stack components.
    """
    command = f"down --rmi {images}"

    if volumes:
        command = f"{command} --volumes"

    if orphans:
        command = f"{command} --remove-orphans"

    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def start(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    services=None,
):
    """
    Start one or more services.
    """
    command = f"start"
    run_command_with_services(context, user, remote, instance, stack, command, services)


@task(help=HELP)
def stop(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    services=None,
):
    """
    Stop one or more services.
    """
    command = f"stop"
    run_command_with_services(context, user, remote, instance, stack, command, services)


@task(help=HELP)
def restart(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    services=None,
):
    """
    Restart one or more services.
    """
    command = f"restart"
    run_command_with_services(context, user, remote, instance, stack, command, services)


@task(help=HELP)
def restore(
    context, backup, user=get_local_user(), remote=False, instance=None, stack=None,
):
    """
    Restore a database backup.
    """
    command = f"exec postgres pkill -f {PROJECT}"
    run_command(context, user, remote, instance, stack, command)

    command = f"run --rm postgres restore {backup}"
    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def shell(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    service="django",
):
    """
    Connect to a running service.
    """
    command = f"run --rm {service} bash"
    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def django(
    context, command, user=get_local_user(), remote=False, instance=None, stack=None
):
    """
    Run a Django management command.
    """
    command = f"run --rm django python manage.py {command}"
    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def test(
    context,
    user=get_local_user(),
    remote=False,
    instance=None,
    stack=None,
    app=None,
    coverage=False,
):
    """
    Run tests with pytest.
    """
    command = "pytest"

    if app:
        command = f"{command} {app}"

    if coverage:
        command = f"coverage run -m {command}"

    command = f"run --rm django {command}"
    run_command(context, user, remote, instance, stack, command)


@task(help=HELP)
def compose(
    context, command, user=get_local_user(), remote=False, instance=None, stack=None
):
    """
    Run a raw compose command.
    """
    run_command(context, user, remote, instance, stack, command)
