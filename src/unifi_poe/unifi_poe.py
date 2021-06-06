import click
import re

from unifi_poe.unifi import UnifiApi, UnifiControllerType, UnifiPoEMode


def _validate_mac_address(ctx, param, value):
    if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
        msg = "the {} is not a valid MAC address"
        raise click.BadParameter(msg.format(value))
    return value


@click.group()
@click.option(
    "--host",
    help="The URL of the Unifi controller",
    required=True,
)
@click.option(
    "--username",
    help="username to access the Unifi api",
    required=True,
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=False,
    help="password to access the Unifi api",
)
@click.option(
    "--site",
    help="Unifi site name",
    default="default",
)
@click.option(
    "--controller_type",
    help="Unifi controller type",
    type=click.Choice(["udm", "unifi_controller"], case_sensitive=False),
    default="udm",
)
@click.option(
    "-m",
    "--switch-mac",
    callback=_validate_mac_address,
    help="MAC Address of the switch who's port you wish to control",
    required=True,
)
@click.option(
    "-p",
    "--switch-port",
    type=click.IntRange(0, 47),
    help="The port on the switch you wish to control",
    required=True,
)
@click.pass_context
def cli(ctx, host, username, password, site, controller_type, switch_mac, switch_port):
    """Control the state of port SWITCH_PORT on Unifi switch SWITCH_MAC_ADDRESS"""
    ctx.obj = (
        switch_mac,
        switch_port,
        UnifiApi(
            host,
            username,
            password,
            site=site,
            controller_type=UnifiControllerType[controller_type],
        ),
    )


def poe_mode_set(ctx, mode):
    switch_mac, switch_port, api = ctx.obj
    switch_info = api.get_switch_info(switch_mac)
    existing_overrides = switch_info["port_overrides"]

    for port in existing_overrides:
        if port["port_idx"] == switch_port:
            port["poe_mode"] = mode.name
            break
    else:
        raise Exception("No existing override")

    api.request(
        "/rest/device/{}".format(switch_info["_id"]),
        method="PUT",
        data={"port_overrides": existing_overrides},
    )
    click.echo(f"Set poe_mode of port {switch_port} to {mode.name}")


@cli.command(help="Turn on PoE port")
@click.pass_context
def on(ctx):
    poe_mode_set(ctx, UnifiPoEMode.auto)


@cli.command(help="Turn off PoE port")
@click.pass_context
def off(ctx):
    poe_mode_set(ctx, UnifiPoEMode.off)


@cli.command(help="Power cycle PoE port")
@click.pass_context
def cycle(ctx):
    switch_mac, switch_port, api = ctx.obj
    api.request(
        "/cmd/devmgr",
        method="POST",
        data={
            "cmd": "power-cycle",
            "mac": switch_mac,
            "port_idx": switch_port,
        },
    )


if __name__ == "__main__":
    cli()
