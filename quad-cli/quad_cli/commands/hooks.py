"""
QUAD Hooks Commands
===================

Manage Claude CLI hook integration.

Commands:
  quad hooks enable/disable
  quad hooks status
  quad hooks session enable/disable
  quad hooks config set <key> <value>
  quad hooks logs [--tail N] [--clear]
  quad hooks test <command>

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import click
import json
from quad_cli.hooks import (
    load_hook_config,
    save_hook_config,
    get_session_id,
    set_session_override,
    get_session_override,
    test_hook
)
from quad_cli.hooks.hook_config import (
    get_logs,
    clear_logs,
    add_prefix,
    remove_prefix,
    add_whitelist_command,
    remove_whitelist_command
)


@click.group()
def hooks():
    """Manage Claude CLI hooks"""
    pass


@hooks.command()
def enable():
    """Enable QUAD hooks globally"""
    config = load_hook_config()
    config["enabled"] = True
    save_hook_config(config)

    click.echo("\n  ✓ QUAD hooks enabled\n")
    click.echo("  Hooks will intercept QUAD commands in Claude CLI")
    click.echo(f"  Mode: {config.get('mode', 'prefix')}")
    click.echo()


@hooks.command()
def disable():
    """Disable QUAD hooks globally"""
    config = load_hook_config()
    config["enabled"] = False
    save_hook_config(config)

    click.echo("\n  ✓ QUAD hooks disabled\n")
    click.echo("  All commands will pass through to Claude directly")
    click.echo()


@hooks.command()
def status():
    """Show hook status"""
    config = load_hook_config()
    session_id = get_session_id()
    session_override = get_session_override(session_id)

    click.echo("\n  QUAD Hooks Status")
    click.echo("  " + "─" * 40)

    # Global status
    enabled = config.get("enabled", False)
    status_text = click.style("Enabled", fg="green") if enabled else click.style("Disabled", fg="red")
    click.echo(f"  Global: {status_text}")

    # Mode
    mode = config.get("mode", "prefix")
    click.echo(f"  Mode: {mode}")

    # Session
    click.echo(f"  Session ID: {session_id}")

    if session_override is not None:
        override_text = click.style("Enabled", fg="green") if session_override else click.style("Disabled", fg="red")
        click.echo(f"  Session Override: {override_text}")
    else:
        click.echo("  Session Override: Not set")

    # Mode-specific info
    if mode == "prefix":
        prefixes = config.get("prefixes", [])
        click.echo(f"  Prefixes: {', '.join(prefixes)}")
    elif mode == "whitelist":
        commands = config.get("commands", [])
        click.echo(f"  Whitelisted: {', '.join(commands)}")

    # Auto context
    auto_context = config.get("auto_context", True)
    click.echo(f"  Auto-load context: {auto_context}")

    # Fallback
    fallback = config.get("fallback", "direct")
    click.echo(f"  Error fallback: {fallback}")

    click.echo()


@hooks.group()
def session():
    """Manage per-session hooks"""
    pass


@session.command("enable")
def session_enable():
    """Enable hooks for current session"""
    session_id = get_session_id()
    set_session_override(session_id, True)

    click.echo(f"\n  ✓ Hooks enabled for session: {session_id}\n")


@session.command("disable")
def session_disable():
    """Disable hooks for current session"""
    session_id = get_session_id()
    set_session_override(session_id, False)

    click.echo(f"\n  ✓ Hooks disabled for session: {session_id}\n")


@session.command("status")
def session_status():
    """Show current session status"""
    session_id = get_session_id()
    override = get_session_override(session_id)

    click.echo(f"\n  Session: {session_id}")

    if override is not None:
        status_text = click.style("Enabled", fg="green") if override else click.style("Disabled", fg="red")
        click.echo(f"  Override: {status_text}")
    else:
        click.echo("  Override: Not set (using global setting)")

    click.echo()


@hooks.group()
def config():
    """Manage hook configuration"""
    pass


@config.command("show")
def config_show():
    """Show full configuration"""
    cfg = load_hook_config()

    click.echo("\n  Hook Configuration")
    click.echo("  " + "─" * 40)
    click.echo(json.dumps(cfg, indent=2))
    click.echo()


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set configuration value"""
    cfg = load_hook_config()

    # Parse value
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False

    # Set value
    if "." in key:
        # Nested key (e.g., "logging.enabled")
        parts = key.split(".")
        current = cfg
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    else:
        cfg[key] = value

    save_hook_config(cfg)
    click.echo(f"\n  ✓ Set {key} = {value}\n")


@hooks.group()
def prefix():
    """Manage command prefixes"""
    pass


@prefix.command("add")
@click.argument("prefix_str")
def prefix_add(prefix_str):
    """Add a prefix"""
    if add_prefix(prefix_str):
        click.echo(f"\n  ✓ Added prefix: {prefix_str}\n")
    else:
        click.echo(f"\n  Prefix already exists: {prefix_str}\n")


@prefix.command("remove")
@click.argument("prefix_str")
def prefix_remove(prefix_str):
    """Remove a prefix"""
    if remove_prefix(prefix_str):
        click.echo(f"\n  ✓ Removed prefix: {prefix_str}\n")
    else:
        click.echo(f"\n  Prefix not found: {prefix_str}\n")


@prefix.command("list")
def prefix_list():
    """List all prefixes"""
    cfg = load_hook_config()
    prefixes = cfg.get("prefixes", [])

    click.echo("\n  Command Prefixes")
    click.echo("  " + "─" * 40)
    for p in prefixes:
        click.echo(f"  - {p}")
    click.echo()


@hooks.group()
def whitelist():
    """Manage whitelisted commands"""
    pass


@whitelist.command("add")
@click.argument("command")
def whitelist_add(command):
    """Add a command to whitelist"""
    if add_whitelist_command(command):
        click.echo(f"\n  ✓ Added to whitelist: {command}\n")
    else:
        click.echo(f"\n  Command already whitelisted: {command}\n")


@whitelist.command("remove")
@click.argument("command")
def whitelist_remove(command):
    """Remove a command from whitelist"""
    if remove_whitelist_command(command):
        click.echo(f"\n  ✓ Removed from whitelist: {command}\n")
    else:
        click.echo(f"\n  Command not found in whitelist: {command}\n")


@whitelist.command("list")
def whitelist_list():
    """List whitelisted commands"""
    cfg = load_hook_config()
    commands = cfg.get("commands", [])

    click.echo("\n  Whitelisted Commands")
    click.echo("  " + "─" * 40)
    for cmd in commands:
        click.echo(f"  - {cmd}")
    click.echo()


@hooks.command()
@click.option("--tail", default=50, help="Number of recent lines to show")
@click.option("--clear", is_flag=True, help="Clear logs")
def logs(tail, clear):
    """View or clear hook logs"""
    if clear:
        clear_logs()
        click.echo("\n  ✓ Logs cleared\n")
        return

    log_content = get_logs(tail)

    click.echo("\n  Hook Execution Logs")
    click.echo("  " + "─" * 40)
    click.echo(log_content)
    click.echo()


@hooks.command()
@click.argument("command")
def test(command):
    """Test if a command would be intercepted"""
    result = test_hook(command)

    click.echo("\n  Hook Test")
    click.echo("  " + "─" * 40)
    click.echo(f"  Command: {result['command']}")

    would_intercept = result["would_intercept"]
    if would_intercept:
        click.echo(f"  Result: " + click.style("WOULD INTERCEPT", fg="green"))
    else:
        click.echo(f"  Result: " + click.style("WOULD PASS THROUGH", fg="yellow"))

    click.echo(f"  Reason: {result['reason']}")

    click.echo("\n  Configuration:")
    click.echo(f"    Enabled: {result['config']['enabled']}")
    click.echo(f"    Mode: {result['config']['mode']}")
    click.echo(f"    Session ID: {result['config']['session_id']}")
    override = result['config']['session_override']
    if override is not None:
        click.echo(f"    Session Override: {override}")

    click.echo()


def main():
    """Entry point for hooks commands"""
    hooks()


if __name__ == "__main__":
    main()
