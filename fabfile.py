from fabric import Connection, task
from invoke.exceptions import Failure, ThreadException, UnexpectedExit

COLOUR_RESET = "\033[0m"
COLOUR_RED = "\033[31m"

HOST = "radicalt.kdl.kcl.ac.uk"
HOST_PATH = "/project/containers"
PROJECT_NAME = "radical_translations"


@task
def deploy(context, host=HOST, instance="dev", branch="master", stack="dev"):
    backup(context, host, instance, stack)
    update(context, host, instance, branch)
    up(context, host, instance, stack)


def get_connection(host):
    return Connection(host, gateway=get_gateway())


def get_gateway():
    return Connection(
        "ssh2.kdl.kcl.ac.uk", connect_kwargs={"gss_auth": True, "gss_kex": True}
    )


def cd(connection, instance):
    return connection.cd(f"{HOST_PATH}/{PROJECT_NAME}_{instance}")


@task
def backup(context, host=HOST, instance="dev", stack="dev"):
    run_command(host, instance, f"docker-compose -f {stack}.yml run postgres backup")


def run_command(host, instance, command):
    try:
        with get_connection(host) as c:
            with cd(c, instance):
                c.run(command)
    except (Failure, ThreadException, UnexpectedExit):
        print()
        print(f"{COLOUR_RED}> Failed to run command: `{command}`{COLOUR_RESET}")
        print()


@task
def update(context, host=HOST, instance="dev", branch="master"):
    run_command(host, instance, f"git pull && git checkout {branch}")


@task
def up(context, host=HOST, instance="dev", stack="dev"):
    run_command(host, instance, f"docker-compose -f {stack}.yml up --build --detach")


@task
def destroy(context, host=HOST, instance="dev", stack="dev"):
    run_command(
        host, instance, f"docker-compose -f {stack}.yml down --volumes --rmi all"
    )


@task
def shell(context, host=HOST, instance="dev", stack="dev", service="django"):
    run_command(host, instance, f"docker-compose -f {stack}.yml run {service} bash")
