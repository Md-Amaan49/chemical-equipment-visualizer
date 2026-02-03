#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
npm install

# Build the React app
npm run build

# Install serve globally to serve the built app
npm install -g serve