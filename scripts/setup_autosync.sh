#!/bin/sh
git config core.hooksPath .githooks
chmod +x .githooks/post-commit || true
echo "Set core.hooksPath to .githooks"
