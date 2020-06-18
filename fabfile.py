import configparser
import sys
from configparser import ConfigParser, SectionProxy
from typing import Optional

from fabric import Connection, task
from fabric.util import get_local_user
from invoke.context import Context
from invoke.exceptions import Failure, ThreadException, UnexpectedExit

COLOUR_OFF: str = "\033[0m"


def error(message: str):
    colour_red: str = "\033[31m"

    print()
    print(f"{colour_red}{message}{COLOUR_OFF}")


def info(message: str):
    colour_blu: str = "\033[34m"

    print()
    print(f"{colour_blu}{message}{COLOUR_OFF}")


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
    "host": "Server where to run the task. For localhost, use `l` or `local`.",
    "Images": "Images to be removed, by default all images are removed.",
    "initial": "Set to `True` for first time deployments.",
    "instance": (
        "Server instance where to run the task, can be left empty when running "
        "local tasks."
    ),
    "service": "Service name to run the task.",
    "services": "Service names to run the task. Separate multiple services with space.",
    "stack": "Docker stack for docker commands.",
    "volumes": "Set to `True` to remove volumes.",
    "orphans": "Set to `True` to remove orphan containers.",
}


@task(help=HELP)
def deploy(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    initial=False,
    branch=BRANCH,
    stack=STACK,
):
    """
    Deploy the project. By default it creates a database backup before updating from
    source control and rebuilding the docker stack.
    """
    if initial:
        clone(context, user, host, instance, branch)
    else:
        backup(context, user, host, instance, stack)

    update(context, user, host, instance, branch)
    up(context, user, host, instance, stack)


@task(help=HELP)
def clone(context, user=get_local_user(), host=HOST, instance=INSTANCE, branch=BRANCH):
    """
    Clone the project repository into a host instance.
    """
    env_path = f"{HOST_PATH}/{instance}/.envs"
    env_file = f"{instance}.tar.gz"

    run_command(
        context, user, "local", None, f"tar czvf .envs/{env_file} .envs/.{instance}"
    )

    run_command(context, user, host, "", f"git clone {REPOSITORY} {instance}")

    with get_connection(user, host) as c:
        c.put(f".envs/{env_file}", env_path)

    run_command(
        context,
        user,
        host,
        instance,
        f"tar zxvf {env_path}/{env_file} && rm {env_path}/{env_file}",
    )

    run_command(context, user, host, instance, f"mkdir {PROJECT}/media")


def run_command(
    context: Context, user: str, host: str, instance: Optional[str], command: str
):
    info(f"{host}/{instance}\n{command}")

    try:
        if is_localhost(host):
            context.run(command, replace_env=False, pty=True)
        else:
            with get_connection(user, host) as c:
                with c.cd(f"{HOST_PATH}/{instance}"):
                    c.run(command, pty=True)
    except (Failure, ThreadException, UnexpectedExit):
        error(f"{host}/{instance}\nFailed to run command: `{command}`")


def is_localhost(host: str):
    return host.lower() in ["l", "local"]


def get_connection(user: str, host: str) -> Connection:
    return Connection(host, user=user, gateway=get_gateway(user))


def get_gateway(user: str) -> Connection:
    return Connection(
        GATEWAY, user=user, connect_kwargs={"gss_auth": True, "gss_kex": True}
    )


@task(help=HELP)
def backup(context, user=get_local_user(), host=HOST, instance=INSTANCE, stack=STACK):
    """
    Create a database backup.
    """
    run_command(
        context, user, host, instance, f"{get_compose_cmd(stack)} run postgres backup"
    )


def get_compose_cmd(stack: str) -> str:
    if stack.lower() == "l":
        stack = "local"

    return f"{COMPOSE_CMD} -f {stack}.yml"


@task(help=HELP)
def update(context, user=get_local_user(), host=HOST, instance=INSTANCE, branch=BRANCH):
    """
    Update the host instance from source control.
    """
    run_command(context, user, host, instance, f"git checkout {branch} && git pull")


@task(help=HELP)
def up(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    services=None,
):
    """
    Build the stack for the host instance.
    """
    command = f"{get_compose_cmd(stack)} up --build"

    if not is_localhost(host):
        command = f"{command} --detach"

    run_command_with_services(context, user, host, instance, command, services)


def run_command_with_services(
    context: Context,
    user: str,
    host: str,
    instance: str,
    command: str,
    services: Optional[str],
):
    if services:
        command = f"{command} {services}"

    run_command(context, user, host, instance, command)


@task(help=HELP)
def down(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    images="all",
    volumes=True,
    orphans=False,
):
    """
    Stop and remove stack components.
    """
    command = f"{get_compose_cmd(stack)} down --rmi {images}"

    if volumes:
        command = f"{command} --volumes"

    if orphans:
        command = f"{command} --remove-orphans"

    run_command(context, user, host, instance, command)


@task(help=HELP)
def start(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    services=None,
):
    """
    Start one or more services.
    """
    command = f"{get_compose_cmd(stack)} start"
    run_command_with_services(context, user, host, instance, command, services)


@task(help=HELP)
def stop(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    services=None,
):
    """
    Stop one or more services.
    """
    command = f"{get_compose_cmd(stack)} stop"
    run_command_with_services(context, user, host, instance, command, services)


@task(help=HELP)
def restart(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    services=None,
):
    """
    Restart one or more services.
    """
    command = f"{get_compose_cmd(stack)} restart"
    run_command_with_services(context, user, host, instance, command, services)


@task(help=HELP)
def restore(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    backup=None,
):
    """
    Restore a database backup.
    """
    if not backup:
        error("Please provide a backup file name.")
        sys.exit(-1)

    run_command(
        context,
        user,
        host,
        instance,
        f"{get_compose_cmd(stack)} exec postgres pkill -f {PROJECT}",
    )
    run_command(
        context,
        user,
        host,
        instance,
        f"{get_compose_cmd(stack)} run postgres restore {backup}",
    )


@task(help=HELP)
def shell(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    service="django",
):
    """
    Connect to a running service.
    """
    command = f"{get_compose_cmd(stack)} run {service} bash"
    run_command(context, user, host, instance, command)


@task(help=HELP)
def django(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    command=None,
):
    """
    Run a Django management command.
    """
    if not command:
        command = ""

    command = f"{get_compose_cmd(stack)} run django python manage.py {command}"
    run_command(context, user, host, instance, command)


@task(help=HELP)
def test(
    context,
    user=get_local_user(),
    host=HOST,
    instance=INSTANCE,
    stack=STACK,
    coverage=False,
    app=None,
):
    """
    Run tests with pytest.
    """
    test_command = "pytest"

    if coverage:
        test_command = f"coverage run -m {test_command}"

    if not app:
        app = ""

    command = f"{get_compose_cmd(stack)} run django {test_command} {app}"
    run_command(context, user, host, instance, command)
