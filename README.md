# 🛡️ domain-ip-blocker

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/) ![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) ![OS](https://img.shields.io/badge/Supported_OS-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg) [![Status](https://img.shields.io/badge/Status-Stable-success.svg)](#)

---

### Cross-platform Domain and IP Blocking Utility  
Developed by **VidyaSagar Gajivelli**

`domain-ip-blocker` is a lightweight, cross-platform command-line tool that automatically blocks or unblocks domains and their resolved IP addresses using each system’s native firewall and hosts configuration.

It provides a unified interface for managing domain/IP blocking across **Windows**, **Linux**, and **macOS**, ideal for network administrators, developers, and security engineers.

---

### ✨ Features

- 🧩 **Cross-platform** — Works seamlessly on Windows, Linux, and macOS  
- 🌐 **DNS Resolution** — Automatically resolves domains to IPv4/IPv6 addresses using `dnspython`  
- 🔥 **System Firewalls**  
  - Windows Firewall (`netsh advfirewall`)  
  - Linux `ipset` + `iptables`  
  - macOS Packet Filter (`pfctl`)  
- 🧱 **Hosts File Management** — Updates `/etc/hosts` or Windows `hosts` file  
- 📊 **Progress Indicators** — Displays real-time progress using `tqdm`  
- ⚙️ **Configurable** — Reads domain lists from plain text files in `config/`  
- 🧹 **Cleanup** — Safely restores hosts and firewall rules with `unblock`  

---

### 📦 Project Structure

```
domain-ip-blocker/
├── main.py
├── src/
│ ├── constants.py 
│ ├── domain_manager.py 
│ └── ip_manager.py
├── utils/
│ ├── command_runner.py
│ ├── domain_resolver.py
│ ├── progress_bar.py 
│ ├── file_permissions.py
│ ├── windows_firewall.py
│ ├── linux_firewall.py
│ └── darwin_firewall.py
├── config/
│ └── *.txt 
└── requirements.txt

```

---

### ⚙️ Installation Guide

#### 1. Clone the Repository
```bash
git clone https://github.com/vidyasagar/domain-ip-blocker.git
```
```bash
cd domain-ip-blocker
```

#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Install System Dependencies

##### 🪟 Windows
```bash
# No extra dependencies. The script uses the built-in Windows Firewall (netsh advfirewall)
```
##### 🐧 Linux
```bash
# Make sure the following packages are installed:
sudo apt install ipset iptables netfilter-persistent

# For non-Debian systems, install equivalents via your package manager (e.g., dnf, yum, or pacman)
```

##### 🍎 macOS
```bash
# Ensure Packet Filter (pf) is enabled (it’s built into macOS)
# No additional packages are required
```

---

### 🚀 Usage

The tool can be run directly from the command line:

```bash
python main.py [command] [options]
```


| Command | Description |
|----------|-------------|
| `block` | Blocks all domains and their resolved IPs from the `config/` folder |
| `unblock` | Removes all blocking rules (restores system to normal) |
| `--domain` | Optional flag — blocks only domains (skips firewall-level IP blocking) |

##### 💡 Examples

```bash
# Block all domains and their resolved IPs
sudo python main.py block
```

```bash
# Unblock all domains and IPs (restore original settings)
sudo python main.py unblock
```

```bash
# Block only domains (skip IP-level blocking)
sudo python main.py block --domain
```
✅ **Note:**
- Use `sudo` (Linux/macOS) or run as **Administrator** (Windows).  
- Domain lists must be stored in the `config/` folder as `.txt` files (one domain per line).

---

### 🗂️ Configuration

The tool reads domain lists from the **`config/`** directory.  
Each `.txt` file represents a category or group of domains you want to block.

You can create **any number of `.txt` files**, for example:

```
config/
├── gambling-hosts.txt
├── pornography-hosts.txt
├── ads-hosts.txt
└── social-hosts.txt
```
Each file should contain one domain per line, formatted like this:
```text
0.0.0.0    example.com
0.0.0.0    badsite.net
0.0.0.0    tracker.ads.com
```
💡 **Tips**

- You can add or edit these files anytime.

- When you run the `block` command, all `.txt` files inside `config/` are processed automatically.

- To remove all blocks, simply run `python main.py unblock`.

---

### 🧠 How It Works

1. Loads domain lists from `config/` folder.

1. Resolves each `domain` to its `IP` addresses.

1. Adds them to the `system firewall` and `hosts` file.

1. Provides an option to `unblock` and restore settings.

---

### 🤝 Contributing

Contributions, issues, and feature requests are always welcome! 💡  
If you’d like to contribute:

1. Fork this repository  
2. Create a new branch (`git checkout -b feature/YourFeatureName`)  
3. Commit your changes (`git commit -m "Add some feature"`)  
4. Push to your branch (`git push origin feature/YourFeatureName`)  
5. Open a Pull Request  

Your ideas, fixes, and improvements help make **domain-ip-blocker** better for everyone 🚀  

---

### 📜 License

This project is licensed under the **[MIT License](LICENSE)** © 2025 [Vidyasagar Gajivelli](https://github.com/vidyasagar)

