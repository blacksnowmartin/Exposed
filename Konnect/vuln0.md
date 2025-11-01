Got it — here are clear, safe, and practical ways to change your MAC on Ubuntu to **78:60:5b:95:26:29**, plus verification and how to make it persistent. Quick legal note: only do this on hardware/networks you own or have permission to modify. Using a duplicate MAC on a network can cause conflicts.

---

# 1) Find your interface name

Run:

```bash
ip link show
```

Look for names like `eth0`, `enp3s0`, `wlp2s0`, etc. I’ll use `IFACE` as a placeholder below — replace it with your actual interface name.

---

# 2) Temporary change (works until reboot or interface down/up)

This is the simplest, uses standard tools:

```bash
sudo ip link set dev IFACE down
sudo ip link set dev IFACE address 78:60:5b:95:26:29
sudo ip link set dev IFACE up
```

Verify:

```bash
ip link show dev IFACE
# or
cat /sys/class/net/IFACE/address
```

---

# 3) Using `macchanger` (convenient checks + change)

Install:

```bash
sudo apt update
sudo apt install macchanger
```

Set the MAC:

```bash
sudo ip link set dev IFACE down
sudo macchanger -m 78:60:5b:95:26:29 IFACE
sudo ip link set dev IFACE up
```

Check:

```bash
macchanger -s IFACE
```

`macchanger` may prompt at install whether to enable automatic changes — choose per your preference.

---

# 4) Persistent change with NetworkManager (recommended for desktop Ubuntu)

List connections to find the right NetworkManager connection name:

```bash
nmcli connection show
```

Then set the cloned MAC for that connection:

```bash
sudo nmcli connection modify "CONNECTION_NAME" 802-3-ethernet.cloned-mac-address 78:60:5b:95:26:29
sudo nmcli connection down "CONNECTION_NAME"
sudo nmcli connection up   "CONNECTION_NAME"
```

To remove the persistent override later:

```bash
sudo nmcli connection modify "CONNECTION_NAME" 802-3-ethernet.cloned-mac-address ""
```

If you prefer to edit the connection file directly, look under `/etc/NetworkManager/system-connections/` (but use `nmcli` — it handles permissions).

---

# 5) Persistent via netplan/systemd (server/minimal installs)

**Netplan** typically manages interfaces on newer Ubuntu. Netplan itself doesn’t set MAC clone addresses, so prefer NetworkManager for persistent changes on desktops. For systems using `systemd-networkd` you can create a `.link` file:

Create `/etc/systemd/network/10-IFACE.link` (replace `IFACE` with your interface name) with:

```
[Match]
OriginalName=IFACE

[Link]
MACAddress=78:60:5b:95:26:29
```

Then reload:

```bash
sudo systemctl restart systemd-networkd
# or reboot
```

(Be careful editing system network files — test on a maintenance window if remote.)

---

# 6) Extra notes & troubleshooting

* If NetworkManager is active, `ip link` changes may be overwritten when the connection reconnects — use `nmcli` for persistence.
* Changing a MAC can temporarily disconnect you (Wi-Fi will drop and reconnect).
* If the network enforces authenticated MAC filtering, you may be blocked.
* Avoid using a MAC that is already on the same LAN — it causes collisions and connectivity problems.
* Technical note: `78:60:5b:95:26:29` has its “locally administered” bit unset (it appears globally-assigned). Many people use a locally-administered MAC (set the second-least-significant bit of the first octet) for privacy; networks generally don’t care but some do. If you want a locally-administered address instead I can show how to generate one.

---

If you tell me:

* your interface name (output of `ip link`), and
* whether you want the change temporary or persistent (NetworkManager or systemd),

I’ll give you the exact commands ready to paste.
