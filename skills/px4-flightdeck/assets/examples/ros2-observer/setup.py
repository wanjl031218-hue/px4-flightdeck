from setuptools import find_packages, setup

setup(
    name="flightdeck_ros_observer",
    version="0.2.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/flightdeck_ros_observer"]),
        ("share/flightdeck_ros_observer", ["package.xml", "LICENSE"]),
    ],
    install_requires=["setuptools"],
    license="MIT",
    description="Read-only PX4 local-position observer",
    entry_points={"console_scripts": ["observe_position = flightdeck_ros_observer.observer:main"]},
)
