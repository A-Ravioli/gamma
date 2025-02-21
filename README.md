# gamma: a Lambda Labs CLI

A command-line interface for interacting with Lambda Labs Cloud API.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd gamma
```

2. Install the package:
```bash
pip install -e .
```

3. Set up your API key:
Create a `.env` file in your home directory or project directory with:
```
LAMBDA_API_KEY=your-api-key-here
```

## Usage

The CLI provides several commands for managing Lambda Labs resources:

### Instance Management

List all instances:
```bash
gamma instances list
```

Get instance details:
```bash
gamma instances info <instance-id>
```

Launch a new instance:
```bash
gamma instances launch --region us-east-1 --type gpu_1x_a100_sxm4 --ssh-key your-key-name
```

Restart instances:
```bash
gamma instances restart <instance-id-1> <instance-id-2>
```

Terminate instances:
```bash
gamma instances terminate <instance-id-1> <instance-id-2>
```

### SSH Key Management

List SSH keys:
```bash
gamma ssh-keys list
```

Add an SSH key:
```bash
gamma ssh-keys add --name my-key --public-key "ssh-ed25519 KEY COMMENT"
```

Delete an SSH key:
```bash
gamma ssh-keys delete <key-id>
```

### Other Commands

List available instance types:
```bash
gamma instance-types
```

List filesystems:
```bash
gamma filesystems
```

## Help

For detailed information about any command, use the `--help` flag:

```bash
gamma --help
gamma instances --help
gamma instances launch --help
```
