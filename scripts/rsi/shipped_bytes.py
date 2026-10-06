"""Bytes a user downloads: committed size at HEAD of the shipped Python source. Prints shipped_bytes=<n>."""
import subprocess

listing = subprocess.run(["git", "ls-tree", "-r", "-l", "-z", "HEAD"], capture_output=True, check=True).stdout
total = 0
for entry in listing.split(b"\0"):
    if not entry:
        continue
    meta, path = entry.decode("utf-8", "replace").split("\t", 1)
    size = meta.split()[3]
    parts = path.split("/")
    if (size != "-" and path.lower().endswith(".py") and len(parts) == 1
            and not parts[0].startswith(".")):
        total += int(size)
print(f"shipped_bytes={total}")
