#!/bin/zsh
# Aktualizuje wyłącznie FreeTube z tapu patiball/tap. Uruchamiane przez launchd
# (~/Library/LaunchAgents/com.patiball.freetube-upgrade.plist).
set -eu
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 HOMEBREW_NO_ENV_HINTS=1

echo "=== $(date '+%F %T')"

# Odświeża tylko ten tap, bez `brew update` dla wszystkich pakietów.
git -C "$(brew --repo patiball/tap)" pull -q --ff-only

if ! brew outdated --cask patiball/tap/freetube | grep -q freetube; then
  echo "FreeTube aktualny"
  exit 0
fi

# Aktualizacja zamyka aplikację, więc przy uruchomionym FreeTube czeka do następnego razu.
if pgrep -xq FreeTube; then
  echo "FreeTube jest uruchomiony, aktualizacja odłożona"
  exit 0
fi

brew upgrade --cask patiball/tap/freetube
