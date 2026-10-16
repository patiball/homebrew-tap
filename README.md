# homebrew-tap

Prywatne repozytorium pakietów Homebrew.

## FreeTube

Pakiet pobiera oficjalne wydania z https://github.com/FreeTubeApp/FreeTube/releases.
Codzienny przepływ GitHub Actions wpisuje najnowsze wydanie dopiero wtedy, gdy ma ono co najmniej 7 dni.
FreeTube nie ma podpisu Apple, dlatego pakiet po instalacji zdejmuje atrybut kwarantanny.

```
brew install --cask patiball/tap/freetube
brew upgrade --cask freetube
```

Ręczne uruchomienie aktualizacji: zakładka Actions, przepływ „Aktualizacja FreeTube”, przycisk „Run workflow”.

## Automatyczna aktualizacja na Macu

Zadanie launchd `scripts/com.patiball.freetube-upgrade.plist` (kopia w `~/Library/LaunchAgents`) codziennie o 10:00
uruchamia `scripts/upgrade-freetube.sh`. Skrypt odświeża tylko ten tap i aktualizuje tylko FreeTube.
Gdy FreeTube jest uruchomiony, aktualizacja czeka do następnego dnia. Log: `~/Library/Logs/freetube-upgrade.log`.
