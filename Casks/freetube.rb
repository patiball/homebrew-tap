cask "freetube" do
  arch arm: "arm64", intel: "x64"

  version "0.25.3"
  sha256 arm:   "2b445d64f5e56a873debea50c785cd41400bdabc387f0d67fc7be745b2b9146e",
         intel: "40fb6c671ec75905e035968ec0c14bfe717643730af80536e625d191455f49bf"

  url "https://github.com/FreeTubeApp/FreeTube/releases/download/v#{version}-beta/freetube-#{version}-beta-mac-#{arch}.dmg"
  name "FreeTube"
  desc "YouTube player focusing on privacy"
  homepage "https://freetubeapp.io/"

  depends_on macos: :monterey

  app "FreeTube.app"

  # FreeTube nie ma podpisu Apple Developer ID ani notaryzacji,
  # więc bez zdjęcia kwarantanny Gatekeeper blokuje uruchomienie.
  postflight_steps do
    run "/usr/bin/xattr",
        args:           ["-dr", "com.apple.quarantine", "{{appdir}}/FreeTube.app"],
        writable_paths: ["FreeTube.app"],
        writable_base:  :appdir
  end

  uninstall quit: "io.freetubeapp.freetube"

  zap trash: [
    "~/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.ApplicationRecentDocuments/io.freetubeapp.freetube.sfl*",
    "~/Library/Application Support/FreeTube",
    "~/Library/Preferences/io.freetubeapp.freetube.plist",
    "~/Library/Saved Application State/io.freetubeapp.freetube.savedState",
  ]
end
