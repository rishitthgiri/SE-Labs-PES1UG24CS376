# Lab 5 – Issues Table (scheduler_system.py) — PES1UG24CS376

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| os.system("cat " + file) (B605) | Security – High | 43 | Shell command built from a string; shell injection risk | Removed the shell call; read and print the file with open() |
| Bare except + pass (B110/W0702/E722) | Bug/Security – Low | 27-28 | Swallows every error silently, hides bugs | Catch only KeyError and print a message |
| Mutable default arg `equipment_list=[]` (W0102) | Bug | 11 | List shared across all calls | Default to None, create list inside function |
| Invalid slot "14-12" gives -2 hours | Logic bug | 30-32, 48 | End before start accepted; non-string slot (1530) would crash | Validate slot; reject if end <= start or malformed |
| Equipment can go negative / KeyError | Logic bug | 16-17 | No availability or unknown-item check before decrementing | Check stock before booking; reject if unavailable |
| Files opened without `with` / encoding (R1732/W1514) | Quality | 35-37, 40 | Resource leaks if an error occurs | Use `with open(..., encoding="utf-8")` |
| Unused variables a, a_more, c (F841/W0612) | Style | 46-49 | Assigned but never used | Call functions without assigning |
| PEP8 spacing / long lines (E302, E305, E501) | Style | many | Missing blank lines, lines > 79 chars | Reformatted |
| Global state + `global` (W0603) | Design | 5-9, 12 | Module-level mutable globals | Moved into a Scheduler class |
| logConflicts naming, missing docstrings (C0103/C0114/C0116) | Quality | 39 etc. | Not snake_case; no docstrings | Renamed log_conflicts; added docstrings |
| main() runs on import | Design | 59 | Side effects when imported | Added `if __name__ == "__main__":` guard |
