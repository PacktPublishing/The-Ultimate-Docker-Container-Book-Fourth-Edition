#!/usr/bin/env bash
set -e

# Base directory
dir="simple-tracing-java"

# Create project directories
mkdir -p "./src/main/java/com/example/demo"
mkdir -p "./src/main/resources"

# Create empty files
touch "./settings.gradle"
touch "./build.gradle"
touch "./src/main/java/com/example/demo/DemoApplication.java"
touch "./src/main/java/com/example/demo/HelloController.java"
touch "./src/main/resources/application.properties"

echo "Project structure for $dir has been created."