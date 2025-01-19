with (import <nixpkgs> {});
mkShell {
    buildInputs = [
		entr
        (python3.withPackages (ps: with ps; [
			pyaml
			libsass
        ]))
    ];
}
