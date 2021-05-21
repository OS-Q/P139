from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-energiamsp430")
FRAMEWORK_VERSION = platform.get_package_version("framework-energiamsp430")
assert isdir(FRAMEWORK_DIR)

board = env.BoardConfig()

variants_dir = join(
    "$PROJECT_DIR", board.get("build.variants_dir")) if board.get(
        "build.variants_dir", "") else join(FRAMEWORK_DIR, "variants")

env.Append(
    CPPDEFINES=[
        ("ARDUINO", 10807),
        ("ENERGIA", int(FRAMEWORK_VERSION.split(".")[1]))
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core")),
        join(variants_dir, board.get("build.variant")),
        join(platform.get_package_dir(
            "toolchain-timsp430"), "msp430", "include")
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Target: Build Core Library
#

libs = []

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkEnergia"),
    join(FRAMEWORK_DIR, "cores", board.get("build.core"))
))

env.Append(LIBS=libs)
