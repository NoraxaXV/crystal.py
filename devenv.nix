{ pkgs, lib, config, inputs, ... }:
{
  languages.python.enable = true;
  languages.python.venv.enable = true;
  enterShell = "pip install -r ./requirements.txt";
  cachix.enable = false;
}