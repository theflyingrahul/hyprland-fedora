# Graphical release smoke tests

Mock proves package construction and dependency resolution, not compositor
behavior. Run this plan on native Fedora 44 x86_64 and aarch64 systems with
real DRM, input, PipeWire, D-Bus, systemd user sessions, and SELinux enforcing.

## Test image

- Start from a clean Fedora 44 installation with current updates.
- Enable only standard Fedora repositories and the immutable candidate
  HyprWM snapshot.
- Verify package and repository metadata signatures.
- Install `hyprland-desktop`; repeat the optional-application section with
  `hyprwm-complete`.
- Preserve the DNF transaction ID and repository revision with the test
  results.

## Login and compositor

1. Confirm the display manager lists exactly the normal Hyprland session and
   no UWSM session.
2. Log in as an unprivileged user.
3. Confirm the compositor creates a graphical systemd user session and exits
   cleanly on logout.
4. Exercise multiple monitors, hotplug, mode changes, scale changes, rotation,
   adaptive sync where supported, and suspend/resume.
5. Exercise keyboard, pointer, touch, tablet, and seat behavior available on
   the test hardware.
6. Start native Wayland and XWayland clients and verify clipboard, drag and
   drop, focus, resize, fullscreen, and mixed-DPI behavior.
7. Review `journalctl --user`, kernel DRM logs, and the SELinux audit log for
   new denials or crashes.

## Desktop integration

- Start `hyprpaper`, change wallpapers through `hyprctl`, and restart its user
  unit.
- Start `hypridle`, trigger idle and resume actions, then invoke `hyprlock`.
- Verify hyprlock rejects an incorrect password, accepts the correct password,
  handles multiple monitors, and resumes after suspend without bypassing PAM.
- Exercise manual and scheduled `hyprsunset` color changes and restore the
  neutral state.
- Trigger a privileged action and verify `hyprpolkitagent` receives, displays,
  accepts, rejects, and cancels the authentication request.
- Confirm all user services stop at logout and do not leak into another user
  session.

## Portal and PipeWire

1. Confirm `xdg-desktop-portal` selects the Hyprland backend while other
   installed portal backends remain co-installable.
2. Test full-screen, output, window, and region screenshots.
3. Test color picking with hyprpicker and the slurp fallback.
4. Start a PipeWire screen-cast from a browser and conferencing client,
   validate the Qt share picker, audio/video continuity, cancellation, and
   stream teardown.
5. Verify D-Bus activation names, user-unit state, and portal logs.

## Optional applications and Qt

- Exercise launcher search providers, Unicode, calculator, desktop entries,
  and explicit options.
- Exercise PipeWire device and stream controls in hyprpwcenter.
- Exercise the shutdown UI without granting unexpected privileges.
- Verify hyprsysteminfo reports the packaged compositor and hardware.
- Launch every hyprland-guiutils executable.
- Set the Hyprland Qt platform theme and Quick Controls style, then test Qt
  Widgets and QML applications for startup, colors, icons, dialogs, and
  Wayland operation.

## Plugins

For each official plugin package:

1. Confirm its RPM requires the exact Hyprland EVR and
   `hyprland-plugin-api`.
2. Load the plugin using its packaged path.
3. Exercise its documented behavior.
4. Unload it and confirm compositor stability.
5. Attempt installation with a deliberately mismatched Hyprland repository
   snapshot and confirm DNF rejects the transaction.

## Upgrade and rollback

1. Install the prior immutable snapshot and create representative user
   configuration.
2. Upgrade normally with `dnf upgrade`.
3. Repeat the login, portal, lock, and plugin checks.
4. Repoint the repository at the retained prior snapshot and perform the
   documented DNF downgrade or history rollback.
5. Confirm the old compositor and exact plugin set operate again.

A release is blocked by crashes, authentication bypass, unresolved SELinux
denials, portal selection failures, broken XWayland, exact-ABI dependency
violations, or inability to return to the retained prior snapshot.
