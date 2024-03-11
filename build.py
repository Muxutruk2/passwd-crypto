# -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "passwordcrypto"
default_task = "publish"

@init
def set_properties(project):
    project.version = "1.0.dev1"
    # Define the source directory for your unit tests
    project.set_property("dir_source_unittest_python", "src/unittest/python")
    project.set_property('coverage_break_build', False)
    project.set_property("distutils_upload_repository", "https://upload.pypi.org/legacy/")
    project.set_property("distutils_upload_sign", False)  # Set to True if you want to sign your distributions
    project.set_property("distutils_upload_verbose", True)  # Set to True for verbose output during upload


    
    # Define additional dependencies, if needed
    project.depends_on("cryptography")

    # Define other properties as needed
    project.set_property("dir_source_main_python", "src/main/python")
    project.set_property("flake8_break_build", True)  # Fail the build on flake8 violations
    project.set_property("coverage_threshold_warn", 70)  # Adjust the coverage threshold as needed
