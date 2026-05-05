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
        devShells.default = pkgs.mkShell {
          packages = [ python ];
        };
      }
    );
}
