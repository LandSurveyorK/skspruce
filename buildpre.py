import os
import shutil

top = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(top, "spruce", "cpp_version")
dst = os.path.join(top, "skspruce", "spruce")


def copy_spruce_source():
    """Copy the spruce cpp source, following symlinks."""
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, symlinks=False)


def disambiguate_spruce_make_unique():
    """Rewrite spruce calls to ``make_unique``.

    This enables us to compile on Windows by ensuring we call ``spruce::make_unique``
    explicitly via the namespace. This removes ambiguity since windows compiles with
    C++14 which is when ``make_unique`` was added to ``std``.
    """
    for root, dirs, files in os.walk(dst, topdown=False):
        for file in files:
            # don't rewrite the definition
            if file != "utility.h":
                with open(os.path.join(root, file), "r") as f:
                    contents = f.read()
                contents = contents.replace("make_unique", "spruce::make_unique")
                with open(os.path.join(root, file), "w") as f:
                    f.write(contents)


copy_spruce_source()
disambiguate_spruce_make_unique()
