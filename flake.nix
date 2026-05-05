{
  description = "webb-se-dyn-dns";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (sys:
      let pkgs = import nixpkgs { system = sys; };
          python = pkgs.python313.withPackages (ps: with ps; [
            aiohttp toml
            ipython
          ]);
          cfg = ./mypy-config.ini;
      in rec {
        packages.webb-se-dyn-dns = pkgs.stdenv.mkDerivation (self: {
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
        });

        devShells.default = pkgs.mkShell {
          packages = [ python ];
        };
      }
    );
}
