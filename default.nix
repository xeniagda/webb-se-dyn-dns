{ pkgs ? (import <nixpkgs> {}) }:
  let python = pkgs.python313.withPackages (ps: with ps; [
        aiohttp toml
        ipython
      ]);
  in pkgs.stdenv.mkDerivation (self: {
    name = "webb-se-dyn-dns";
    src = ./. ;

    buildPhase = ''
      mkdir -p $out/bin
      cp -r $src/* $out/bin/
      rm $out/bin/config.toml.sample
      cat > $out/bin/${self.name} <<'EOF'
      #!/bin/sh
      ${python}/bin/python "$(dirname "$0")"/dyndns.py "$@"
      EOF
      chmod a+x $out/bin/${self.name}
    '';
  })
