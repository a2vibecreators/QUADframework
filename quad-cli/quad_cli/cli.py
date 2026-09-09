#!/usr/bin/env python3
"""
QUAD CLI - Main Entry Point
============================

Usage:
  quad <command> [options]

Commands:
  login     Login to QUAD
  init      Initialize a new project
  story     Generate user stories from description
  code      Generate code using PGCE algorithm
  test      Run tests on generated code
  deploy    Deploy to cloud
  burnout   Team burnout analysis
  chart     Sprint velocity and ticket charts
  status    Show current configuration status

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import click
from rich import print as rprint

from quad_cli import __version__
from quad_cli.utils import Console


@click.group()
@click.version_option(version=__version__, prog_name="quad")
def main():
    """QUAD CLI - Quick Unified Agentic Development"""
    pass


@main.command()
@click.argument("project_name", required=False)
@click.option("--resume", "-r", help="Resume from a saved draft")
@click.option("--interactive", "-i", is_flag=True, help="Force interactive mode")
def init(project_name, resume, interactive):
    """Initialize a new project.

    Examples:
      quad init banking-portal       # Create new project
      quad init                      # Interactive mode
      quad init @org-setup.xlsx      # From Excel file
      quad init --resume bank-demo   # Resume saved draft
    """
    from quad_cli.commands.init import run_init
    run_init(project_name, None, resume, interactive)


@main.command()
@click.option("--status", "-s", is_flag=True, help="Show current login status")
@click.option("--logout", is_flag=True, help="Logout")
def login(status, logout):
    """Login to QUAD.

    Examples:
      quad login                  # Login (asks for name)
      quad login --status         # Show current login
      quad login --logout         # Logout
    """
    from quad_cli.commands.login import run_login
    run_login(status=status, do_logout=logout)


@main.command()
@click.argument("question", required=True)
@click.option("--domain", "-d", help="Domain/org slug to query")
@click.option("--raw", is_flag=True, help="Output raw JSON response")
def question(question, domain, raw):
    """Ask a question with org context.

    Examples:
      quad question "Who has 20 hours availability?"
      quad question "What projects is Dev One working on?" -d bank-demo
    """
    from quad_cli.commands.question import run_question
    run_question(question, domain, raw)


@main.command()
@click.argument("environment", type=click.Choice(["dev", "prod"]))
@click.argument("project", required=True)
@click.option("--dry-run", is_flag=True, help="Show what would be deployed")
def deploy(environment, project, dry_run):
    """Deploy projects to GCP.

    Examples:
      quad deploy dev suma        # Deploy SUMA to dev
      quad deploy prod suma       # Deploy SUMA to prod
      quad deploy dev all         # Deploy all to dev
    """
    from quad_cli.commands.deploy import run_deploy
    run_deploy(environment, project, dry_run)


@main.command()
def status():
    """Show current QUAD configuration status."""
    from quad_cli.utils.config import load_config, load_credentials, get_api_url

    Console.header("QUAD Status")

    config = load_config()
    creds = load_credentials()

    # Auth status
    if creds.get("token"):
        auth_type = creds.get("auth_type", "unknown")
        user = creds.get("user", "unknown")
        Console.success(f"Authenticated: {user} ({auth_type})")
    else:
        Console.warn("Not authenticated. Run: quad login")

    # Domain status
    domain = config.get("domain_slug")
    if domain:
        Console.info(f"Domain: {domain}")
    else:
        Console.info("No domain set")

    # API status
    Console.info(f"API URL: {get_api_url()}")

    print()


@main.command()
@click.argument("subcommand", required=False, default="create")
def story(subcommand):
    """Generate user stories from description using PGCE.

    Examples:
      quad story create          # Generate stories from description
      quad story list            # List existing stories
    """
    from quad_cli.commands.story import run_story
    run_story(subcommand)


@main.command()
@click.argument("subcommand", required=False, default="generate")
def code(subcommand):
    """Generate code using PGCE algorithm.

    Examples:
      quad code generate         # Generate code from stories
      quad code status           # Show generation status
    """
    from quad_cli.commands.code import run_code
    run_code(subcommand)


@main.command("test")
@click.option("--database", is_flag=True, help="Run database tests only")
@click.option("--api", is_flag=True, help="Run API tests only")
@click.option("--web", is_flag=True, help="Run web tests only")
def test_cmd(database, api, web):
    """Run tests on generated code.

    Examples:
      quad test                  # Run all tests
      quad test --database       # Database tests only
      quad test --api            # API tests only
      quad test --web            # Web tests only
    """
    from quad_cli.commands.test import run_test
    if database:
        run_test("database")
    elif api:
        run_test("api")
    elif web:
        run_test("web")
    else:
        run_test()


@main.command()
def burnout():
    """Show team burnout analysis.

    Analyzes team workload and identifies burnout risks.

    Examples:
      quad burnout               # Show burnout analysis
    """
    from quad_cli.commands.burnout import run_burnout
    run_burnout()


@main.command()
@click.argument("chart_type", required=False, default="velocity")
def chart(chart_type):
    """Show sprint charts and analytics.

    Examples:
      quad chart velocity        # Sprint velocity chart
      quad chart tickets         # Ticket status distribution
      quad chart workload        # Team workload chart
    """
    from quad_cli.commands.burnout import run_chart
    run_chart(chart_type)


@main.command()
@click.argument("subcommand", required=False, default="list")
@click.argument("args", nargs=-1)
def context(subcommand, args):
    """Manage context memory system.

    Examples:
      quad context list                    # List all contexts
      quad context show health             # Show health context
      quad context enable health           # Enable health context
      quad context disable health          # Disable health context
      quad context clear health            # Clear health context
      quad context search "banking"        # Search contexts
    """
    from quad_cli.commands.context import run_context
    run_context(subcommand, list(args))


@main.command()
@click.argument("subcommand", required=False, default="list")
@click.argument("args", nargs=-1)
def config(subcommand, args):
    """Manage QUAD AI configuration.

    Examples:
      quad config list                         # List all config
      quad config status                       # Show AI status
      quad config set gemini.api_key "KEY"     # Set Gemini key
      quad config set claude.api_key "KEY"     # Set Claude key
      quad config set router.mode smart        # Set router mode
    """
    from quad_cli.commands.config import run_config
    run_config(subcommand, list(args))


@main.command()
@click.argument("subcommand", required=False, default="help")
@click.argument("args", nargs=-1)
def doc(subcommand, args):
    """Manage project documentation.

    Examples:
      quad doc init                        # Initialize doc structure
      quad doc generate arch               # Generate architecture docs
      quad doc generate all                # Generate all docs
      quad doc validate                    # Validate doc structure
      quad doc config show                 # Show doc config
    """
    from quad_cli.commands.doc import run_doc
    run_doc(subcommand, list(args))


@main.command()
def hooks():
    """Manage Claude CLI hooks.

    Examples:
      quad hooks enable                    # Enable hooks globally
      quad hooks disable                   # Disable hooks globally
      quad hooks status                    # Show hook status
      quad hooks session enable            # Enable for current session
      quad hooks test "quad init app"      # Test hook detection
      quad hooks logs --tail 50            # View logs
    """
    from quad_cli.commands.hooks import main as hooks_main
    hooks_main()


@main.command()
def hook():
    """Run as Claude Code hook (internal use).

    This command is used by the quad-context-hook.py for Claude Code integration.
    """
    from quad_cli.commands.hook import run_hook
    run_hook()


if __name__ == "__main__":
    main()
