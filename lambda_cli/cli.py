import click
from rich.console import Console
from rich.table import Table
from typing import List
from .api import LambdaAPIClient

console = Console()
api = LambdaAPIClient()

def format_table(headers: List[str], rows: List[List[str]], title: str) -> None:
    """Helper function to format and display tables"""
    table = Table(title=title)
    for header in headers:
        table.add_column(header, style="cyan")
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    console.print(table)

@click.group()
def cli():
    """Lambda Labs Cloud CLI"""
    pass

@cli.group()
def instances():
    """Manage Lambda Labs instances"""
    pass

@instances.command()
def list():
    """List all instances"""
    try:
        response = api.list_instances()
        instances_data = response.get("data", [])
        if not instances_data:
            console.print("No instances found", style="yellow")
            return

        headers = ["ID", "Name", "Type", "Region", "Status"]
        rows = [
            [
                inst["id"],
                inst.get("name", "N/A"),
                inst["instance_type"]["name"],
                inst["region"]["name"],
                inst["status"]
            ]
            for inst in instances_data
        ]
        format_table(headers, rows, "Lambda Labs Instances")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@instances.command()
@click.argument("instance-id")
def info(instance_id):
    """Get details about a specific instance"""
    try:
        response = api.get_instance(instance_id)
        instance = response.get("data", {})
        if not instance:
            console.print("Instance not found", style="red")
            return

        console.print("\n[bold cyan]Instance Details:[/bold cyan]")
        for key, value in instance.items():
            console.print(f"{key}: {value}")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@instances.command()
@click.option("--region", required=True, help="Region name (e.g., us-east-1)")
@click.option("--type", "instance_type", required=True, help="Instance type name")
@click.option("--ssh-key", multiple=True, help="SSH key names")
@click.option("--quantity", default=1, help="Number of instances to launch")
def launch(region, instance_type, ssh_key, quantity):
    """Launch new instances"""
    try:
        response = api.launch_instance(
            region_name=region,
            instance_type=instance_type,
            ssh_keys=list(ssh_key),
            quantity=quantity
        )
        console.print("Launch request successful:", style="green")
        console.print(response)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@instances.command()
@click.argument("instance-ids", nargs=-1)
def restart(instance_ids):
    """Restart specified instances"""
    try:
        response = api.restart_instances(list(instance_ids))
        console.print("Restart request successful:", style="green")
        console.print(response)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@instances.command()
@click.argument("instance-ids", nargs=-1)
def terminate(instance_ids):
    """Terminate specified instances"""
    try:
        response = api.terminate_instances(list(instance_ids))
        console.print("Termination request successful:", style="green")
        console.print(response)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@cli.group()
def ssh_keys():
    """Manage SSH keys"""
    pass

@ssh_keys.command()
def list():
    """List all SSH keys"""
    try:
        response = api.list_ssh_keys()
        keys_data = response.get("data", [])
        if not keys_data:
            console.print("No SSH keys found", style="yellow")
            return

        headers = ["ID", "Name", "Created At"]
        rows = [
            [key["id"], key["name"], key["created_at"]]
            for key in keys_data
        ]
        format_table(headers, rows, "SSH Keys")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@ssh_keys.command()
@click.option("--name", required=True, help="Name for the SSH key")
@click.option("--public-key", help="Public key content")
def add(name, public_key):
    """Add a new SSH key"""
    try:
        response = api.add_ssh_key(name, public_key)
        console.print("SSH key added successfully:", style="green")
        console.print(response)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@ssh_keys.command()
@click.argument("key-id")
def delete(key_id):
    """Delete an SSH key"""
    try:
        response = api.delete_ssh_key(key_id)
        console.print("SSH key deleted successfully:", style="green")
        console.print(response)
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@cli.command()
def instance_types():
    """List available instance types"""
    try:
        response = api.list_instance_types()
        types_data = response.get("data", {})
        if not types_data:
            console.print("No instance types found", style="yellow")
            return

        headers = ["Name", "Description", "Price/Hour"]
        rows = []
        for name, details in types_data.items():
            rows.append([
                name,
                details.get("description", "N/A"),
                f"${details.get('price_cents_per_hour', 0)/100:.2f}"
            ])
        format_table(headers, rows, "Instance Types")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@cli.command()
def filesystems():
    """List available filesystems"""
    try:
        response = api.list_filesystems()
        fs_data = response.get("data", [])
        if not fs_data:
            console.print("No filesystems found", style="yellow")
            return

        headers = ["ID", "Name", "Region", "Status"]
        rows = [
            [fs["id"], fs["name"], fs["region"]["name"], fs["status"]]
            for fs in fs_data
        ]
        format_table(headers, rows, "Filesystems")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

if __name__ == "__main__":
    cli()