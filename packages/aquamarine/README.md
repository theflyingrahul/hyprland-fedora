# aquamarine

Rebase of the retired official Fedora source package to upstream tag
`v0.12.1`.

The runtime now carries SOVERSION 11. The downstream patch removes hard-coded
`-O3` and advertises the development dependencies included by Aquamarine's
public headers. The display-dependent test is not runnable in Mock; the
hardware-independent attachment test remains enabled.
