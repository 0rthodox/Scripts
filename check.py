import os
import sys
import hashlib
import re

# We expect that submissions:
# - are stored in different folders for different problems;
# - each solution file is named using pattern {run_id}-{name_or_login}-{problem}-{time_stamp}.cpp.
# This file structure is one of the default options when exporting contest data from ejudge.

# helper function, get file content hash from file name
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# folder to check
# typically this script is started like: python3 check.py path/to/folder/for/problem/x
folder = "." if len(sys.argv) == 1 else sys.argv[1]

# everything caught will be stored here
hashes = {}

# special case - obvious copy-paste from VK will be stored here
COPIED_SYMBOLS_KEYWORD = "COPY_PASTE_NOT_COMPILING"
hashes[COPIED_SYMBOLS_KEYWORD] = []


# list all the files in the folder
for src in os.listdir(folder):
    # skip not C++ sources
    if src.split('.')[1] != "cpp":
        continue

    # split file name, get run id and user login or name
    run = int(src.split('.')[0].split('-')[0])
    user = src.split('.')[0].split('-')[1]

    # create file names for raw and stripped asm listings
    asm = src.split('.')[0] + ".s"
    asm_clean = asm + ".clean"

    # compile C++ to asm
    cmd = "g++ -c -S -o " + folder + "/" + asm + " " + folder + "/" + src + " >/tmp/antiplagiat 2>&1"
    os.system(cmd)

    # if we failed to compile ...
    if not os.path.isfile(folder + "/" + asm):
        # ... open compilation output ...
        with open("/tmp/antiplagiat", encoding = "utf8", errors = 'ignore') as f:
            # ... and check for typical errors caused by copy-paste from VK
            for line in f:
                # if we found typical copy-paste, 
                # add this submission into special case store and break
                if re.search("stray", line):
                    hashes[COPIED_SYMBOLS_KEYWORD].append({"run":run,"user":user})
                    break
        # go to the next C++ file, there is no point to process this file further
        continue

    # if we are here, the compilation was ok,
    # so remove from asm references to orig C++ files, this makes asm listings comparable
    cmd2 = "cat " + folder + "/" + asm + " | grep -v \"[.]file\" > " + folder + "/" + asm_clean
    os.system(cmd2)

    # just in case, this should never happen
    if not os.path.isfile(folder + "/" + asm_clean):
        continue

    # calculate hash for stripped asm listing
    digest = hashlib.md5(open(folder + "/" + asm_clean,'rb').read()).hexdigest()

    # and store this hash
    if digest not in hashes:
        hashes[digest] = [{"run":run,"user":user}]
    else:
        hashes[digest].append({"run":run,"user":user})


# So, we have all the hashes, let's process them.
for h in hashes:

    # Dirty procedure, that cleans the data a bit.
    # We'd like to have only 1 run per user per hash.
    # Otherwise, we'll get tons of self-plagiarism, that is not plagiarism actually.

    users_per_hash = {}
    for record in hashes[h]:
        run = record["run"]
        user = record["user"]
        users_per_hash[user] = run

    hashes[h] = []
    for user in users_per_hash:
        hashes[h].append({"run":users_per_hash[user],"user":user})

    # At this stage we have only 1 run per user per hash.

    # Consider suspicious and print:
    # - if we have duplicate solutions per hash after self-plagiarism was excluded
    # - everything that looks copy-pasted from VK
    if len(hashes[h]) > 1 or h == COPIED_SYMBOLS_KEYWORD:
        print("=== %s ===" % h)
        # sort by run id (that is the same as submission time)
        for run in sorted(hashes[h], key=lambda k: k['run']):
            print(run["user"].replace("_", " ") + " : " + str(run["run"]))
        print("")

