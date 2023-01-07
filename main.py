import click

from ping import start_ping


@click.command()
@click.argument('ip', type=str)
@click.option('--port', '-p', type=int, default=80)
@click.option('--timeout', '-t', type=int, default=1)
@click.option('--count', '-c', type=int, default=None)
def main(ip, port, timeout, count):
    start_ping(ip, port, timeout, count)


if __name__ == '__main__':
    main()
