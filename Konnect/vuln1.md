Nice — here are **exact, ready-to-run commands** to temporarily set your interface’s MAC to **78:60:5b:95:26:29** on Ubuntu. These changes last until the interface is brought down by the system or the machine reboots.

> Legal reminder: only change MAC addresses on networks and devices you own or are authorized to modify.

---

# Quick one-shot (using `ip`)

Replace `IFACE` with your interface name (example: `wlp2s0`, `enp3s0`, `eth0`).

Save current MAC (so you can restore it):

```bash
ORIG=$(cat /sys/class/net/IFACE/address)
echo "original MAC: $ORIG"
```

Temporarily set the MAC:

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

Restore the original MAC:

```bash
sudo ip link set dev IFACE down
sudo ip link set dev IFACE address $ORIG
sudo ip link set dev IFACE up
```

---

# Alternative (convenient) — using `macchanger`

If you prefer `macchanger` (gives handy status output):

Install (if needed):

```bash
sudo apt update
sudo apt install macchanger
```

Set MAC:

```bash
sudo ip link set dev IFACE down
sudo macchanger -m 78:60:5b:95:26:29 IFACE
sudo ip link set dev IFACE up
```

Show status:

```bash
macchanger -s IFACE
```

Revert to previous (if `macchanger` stored it):

```bash
sudo macchanger -p IFACE
```

Or restore the `$ORIG` value saved above with the `ip` commands.

---

# Wi-Fi / NetworkManager note

If NetworkManager is managing the interface, it may override changes when it reconnects. The `ip` / `macchanger` method still works for a temporary session, but you may see NM reapply settings if you disconnect/reconnect via GUI. To avoid that while testing, stop NetworkManager temporarily (only if you’re comfortable and not remote):

```bash
sudo systemctl stop NetworkManager
# do your MAC change and testing
sudo systemctl start NetworkManager
```

(If you're connected remotely, don’t stop NetworkManager — you could lose access.)

---

# Quick checklist

1. Run `ip link show` to find `IFACE`.
2. Save original MAC to `$ORIG`.
3. Use `ip` or `macchanger` to set the new MAC.
4. Verify with `cat /sys/class/net/IFACE/address`.
5. Restore `$ORIG` when done.

---

If you paste the output of `ip link show` (or just the interface name), I’ll give you the exact commands with `IFACE` already filled in so you can copy/paste.
