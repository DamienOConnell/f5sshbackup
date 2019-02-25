#!/usr/bin/env python


"""
[admin@hostname_X:Active:Standalone] ~ # /bin/df -h /var/local/ucs
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/vg--db--sda-set.2._var
                      3.0G  1.7G  1.2G  60% /var

[admin@hostname_X:Active:Standalone] ~ # /bin/df /var/local/ucs
Filesystem           1K-blocks    Used Available Use% Mounted on
/dev/mapper/vg--db--sda-set.2._var
                       3096336 1763380   1175672  60% /var
"""

df_command = "/bin/df /var/local/ucs"

df_output = """

Filesystem     1K-blocks     Used Available Use% Mounted on
/dev/sda1       79046552 39195052  35813100  53% /
"""

for line in df_output.splitlines():
    if line.endswith("/var") or line.endswith("/"):
        parts = line.split()
        if len(parts) > 6:
            # raise ValueError("Too many fields returned from df command")
            pass
        if parts[3].endswith("%"):
            result = int(parts[3].strip("%"))
            print("result is an integer now: {}".format(result))
        if parts[4].endswith("%"):
            result = int(parts[4].strip("%"))
            print("result is an integer now: {}".format(result))


# an alternative method, based on
# parts = s.split()[:4]
#
# result = ""

for line2 in df_output.splitlines():
    if line2.endswith("/var"):
        print(line2)
        simpleparts = line2.split()[:4]
        result = int(simpleparts[3].strip("%"))
        print("result is an integer now: {}".format(result))

for line2 in df_output.splitlines():
    if line2.endswith("/"):
        print(line2)
        simpleparts = line2.split()[:4]
        result = int(simpleparts[3].strip("%"))
        print("disk free % as integer: {}".format(result))
