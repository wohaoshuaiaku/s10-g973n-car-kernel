# SM-G973N kernel build experiment

Build-only workspace for the Korean Samsung Galaxy S10 (SM-G973N), targeting stock Android 12 firmware G973NKSU7HWD3 and security patch 2023-04.

Uses pinned CruelKernel source and toolchain with the existing beyond1lteks configuration, plus checksum-verified Magisk 31.1 payloads.

Artifacts are experimental kernel binaries, NOT flashable firmware. Successful compilation does not establish boot, encryption, DeX, or Magisk compatibility. Device validation and packaging remain separate steps. No device partition images, credentials, or user data are stored here.

The workflow runs on relevant changes to main or via manual dispatch. Source: https://github.com/CruelKernel/samsung-exynos9820
