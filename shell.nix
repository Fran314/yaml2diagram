with (import <nixpkgs> {});
let
	dev = pkgs.writeShellApplication {
		name = "dev";
		runtimeInputs = with pkgs; [
			entr
		];
		text = ''
			# shellcheck disable=SC2010
			ls -A1 | grep -v "$1" | entr -r bash -c "./yaml2diagram diagram.local.yml \"$1\""
		'';
	};
in mkShell {
    buildInputs = [
        (python3.withPackages (ps: with ps; [
			pyaml
			libsass
        ]))
    ];

	packages = [
		dev
	];
}
