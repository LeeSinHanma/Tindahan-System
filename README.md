# Tindahan System

A desktop point-of-sale and inventory app for Philippine tindahan and sari-sari
stores, built with Python, Tkinter, and SQLite. Manage product sales, stock,
customer debts, shopping lists, and manual cash-in/cash-out records in one place.

[MIT license](LICENSE) · Copyright © 2026 Saiken Studio

## Features

- **Sales and inventory:** barcode checkout, quick-access products, product and
  stock management, restocking by name or barcode, and low-stock tracking.
- **Store records:** customer debts and payments, shopping lists, a sales
  dashboard, finance summaries, and PDF exports.
- **Cash In / Out:** custom wallet or bank accounts, transfer details, reference
  searches, duplicate warnings, and claimed/completed status tracking.
- **Separate service fees:** editable stacking fee rules, per-transfer overrides,
  and daily, weekly, monthly, and yearly totals independent of product sales.
- **Accounts:** first-run owner setup, administrator/staff navigation, and salted
  password hashing with migration of existing accounts.
- **Desktop interface:** collapsible navigation, layouts for smaller windows,
  keyboard shortcuts, and optional user-selected checkout sounds.
- **Installation:** a graphical Linux installer and uninstaller, portable
  packages, dependency notices, and accompanying library/application source.

## Install with the setup wizard

The first release is being prepared. Verified Linux builds are currently created
in `dist/releases/`; published packages will appear on the project's
[Releases page](https://github.com/LeeSinHanma/Tindahan-System/releases).
Windows installer recipes and CI are configured; native Windows build/testing
and its dependency-license review remain pending.

Packaged apps include Python, Tk, audio playback, and PDF dependencies. You do
not need to install Python or activate a virtual environment to use an installer.

### Linux x86-64

1. Open `Tindahan-System-<version>-linux-x86_64-setup.run`.
   If your file manager blocks it, open **Properties → Permissions** and allow
   it to run as a program, then open it again.
2. Optionally choose an existing store database with **Choose existing database…**.
3. Click **Install**, then **Finish**. Launch **Tindahan System** from the
   application menu.

Setup installs for your user account, can add a desktop shortcut, and keeps an
existing installed database. No sudo or manual extraction is needed.

To uninstall, open **Uninstall Tindahan System** from the application menu and
click **Uninstall**, then **Finish**. You can also reopen setup and choose
**Uninstall…**, or open the standalone `*-uninstall.run` file. Uninstall removes
the program and shortcuts while keeping store records and selected sounds.
Older installations can use the standalone uninstaller; updating adds its menu
entry. The terminal alternative is `sh ~/.local/opt/tindahan-system/uninstall.sh`.

For portable use, extract the Linux `.tar.gz` and run `./POS-System` from its
folder. `sh install.sh` provides the terminal installer.

### Windows x64

After a Windows build passes its platform and license checks, run
`Tindahan-System-<version>-windows-x86_64-setup.exe`. Its wizard installs for the
current user, adds a Start menu shortcut, and offers a desktop shortcut.
Uninstall through Windows Settings. For the portable ZIP, extract the entire
folder before running `POS-System.exe`.

## Store data and upgrades

Close the app before updating or uninstalling. Installed apps keep their records
outside the application directory:

| Run mode | Database location |
| --- | --- |
| Source checkout | `<project>/pos.db` |
| Installed Windows | `%LOCALAPPDATA%\TindahanSystem\pos.db` |
| Installed Linux | `${XDG_DATA_HOME:-~/.local/share}/tindahan-system/pos.db` |

`TINDAHAN_DATA_DIR` can explicitly select another data directory for either run
mode. An installed app automatically copies an existing `pos.db` beside its
executable into its user-data directory on first launch, including committed
SQLite WAL data. The old database remains intact; an existing destination is
never replaced. When moving from a source checkout, close the source app and
select its database in the Linux setup wizard. For portable packages, copy the
database beside the extracted executable **before its first launch**.
Keep a backup of your original database. If you already launched the installed
copy, close both copies and explicitly choose which database to keep before
replacing anything. Do not run the source and installed copies as separate
live shop databases; their records are independent.

## Run from source

Source development requires Python 3.10 or newer with Tkinter and SQLite support,
`pygame` for optional checkout audio, and `reportlab` for PDF exports.

On Arch Linux or CachyOS, install Tk and the SDL2 audio library:

```bash
sudo pacman -S --needed tk sdl2_mixer
```

If pip builds pygame from source, a C compiler, Python development headers,
SDL2 development files, and SDL2 mixer development files must be available.
On Arch Linux or CachyOS, the Python and SDL2 packages include development files;
install `base-devel` for the build tools.

From the project directory, without needing shell activation:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

For Windows development:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

If you prefer activation, Bash/Zsh use `source .venv/bin/activate`; Fish uses
`source .venv/bin/activate.fish`.

The source app creates `pos.db` in the project directory on first launch.
Checkout is silent until you choose a sound; no checkout recording is included.
If pygame was built before SDL2 mixer was installed, rebuild it after installing
the required development libraries:

```bash
.venv/bin/python -m pip install --force-reinstall --no-cache-dir --no-binary=pygame pygame
```

## Build packages

Build each package on its target operating system. Python 3.12 is used in the
build workflow; the source app supports Python 3.10+. On Windows, install
[Inno Setup 6](https://jrsoftware.org/isinfo.php) for the setup wizard.

```bash
python -m pip install -r requirements-build.txt
python scripts/build.py --version 0.1.0
```

Use your virtual environment's Python as above. On Windows, `--portable-only`
skips Inno Setup and produces only the ZIP. Linux builds require a working
graphical display; use `xvfb-run -a python scripts/build.py --version 0.1.0`
on a headless builder. Packages and SHA-256 checksums appear in `dist/releases/`.
The build checks the bundled screens, user-selected audio, and PDF generation using a
temporary database; it leaves shop records untouched.
Linux builds also produce the standalone graphical `.run` installer and check
the wizard, the installed application, and an update that preserves records.

Release builds also verify the retained dependency files against a reviewed
inventory and check that license/source materials are packaged. The current
review covers the local CachyOS/Python 3.14 Linux build. A different dependency
version or build environment (including the first Windows/Ubuntu CI builds)
stops before packaging until its actual inventory and notices are reviewed.
The candidate evidence is saved as `build/third-party-inventory-*.json` and
uploaded with CI diagnostics. See [the packaging audit](docs/THIRD_PARTY_AUDIT.md)
and [source/rebuild instructions](packaging/third_party/SOURCE_CODE.md).

The GitHub Actions **Build desktop packages** workflow can be started manually
from the Actions tab with a version number. It tests and builds on Windows and
Ubuntu separately, then uploads artifacts when the inventory review passes.
It does not publish a release. Ubuntu 22.04 is the configured Linux build
baseline; packages built there target systems with
glibc 2.35+ and an X11 desktop or XWayland. Builds made on a newer distribution
can require newer system libraries, so use the workflow artifacts for broader
Linux distribution. ARM, Alpine/musl, and macOS packages are not included.

## Desktop interface

On a fresh database, the first screen asks you to create the store owner's
administrator account. Choose your own username and a password of at least
4 characters, then confirm it. There are no built-in administrator credentials.
Later launches show the normal sign-in form; additional accounts are managed
through **Users** after the owner signs in.

Existing accounts and shop records are preserved. Older plaintext passwords
are migrated to salted PBKDF2-SHA256 hashes on startup. An account still using
the retired shared default must choose a new password after signing in, before
it can access the store. Remembered login cannot bypass that step. Passwords
are case-sensitive and preserve spaces. Changing a password clears remembered
login for that account. Older app versions expect plaintext passwords and cannot
authenticate against the upgraded hashes; keep a pre-upgrade database backup
if you need to roll back. Existing database backups keep their original password
storage. Change the retired password anywhere else you reused it.

The interface supports windows from 960×640 upward. Use the sidebar menu button
to collapse navigation. POS, Shopping List, and Customers & Debt use tabs on
smaller windows and show panels side by side when there is enough space.
Checkout and Sign out stay accessible in compact layouts.

- Inventory: **F1** adds a product, **F2** edits, **F3** deletes, **F4** restocks,
  and **F5** opens settings. Untracked products are available in the stock filter.
  Restock supports partial product names and barcodes, with matching products,
  barcodes, and current stock shown in a selectable list. Select a row, enter
  the quantity, and confirm Restock. Typing filters the list; Enter or Search
  searches immediately and selects an exact barcode match for scanner use.
  Double-clicking a result or pressing Enter in the list focuses the quantity.
- POS: **F1** opens quick access and **Shift+Enter** opens checkout.
  **Checkout sound** lets you choose a WAV, OGG, or MP3 file (up to 10 MB),
  preview or stop it, mute it, or remove it. Checkout is silent until you choose
  a sound. Audio failures never undo a completed sale.
- Product forms: **Ctrl+Enter** saves and **Esc** closes the dialog.
- Shopping List: use the visible controls or the **More** menu for bulk actions.
  **Space** toggles a checked row.
- Tables: click a column heading to sort. Scroll horizontally for wider tables.
- **F11** toggles fullscreen.

Selected audio is copied into the app's user-data `sounds` directory, outside
the repository and installed program. It survives updates and remains available
if the original file moves. The preference applies to the store database on
that machine. When moving to another machine, choose a sound there again or
also transfer the `sounds` directory. No uploaded recording is distributed in
source archives or installers. Choose audio you have permission to use.

Finance offers Today, Last 7 days, and Last 30 days. Gross profit subtracts
product costs from sales, before other expenses, using current product cost
prices. Inventory and debt figures show current balances.

## Cash-in and cash-out tracking

Open **Cash In / Out** in the sidebar. Under **Accounts**, add your own
account names and numbers, such as GCash 1, GCash 2, Maya, or BDO. Account numbers
keep their leading zeros. Both services use the same shop accounts and fee rules.
Transfers are recorded manually from details verified in your wallet or bank app.

Use **Record transfer** and choose **Cash-In** or **Cash-Out**. Both capture the
transfer date/time, shop account, customer account, amount, service fee, and last
five reference digits. Account labels change with the direction:

- **Cash-Out:** your shop account receives the transfer; the customer account
  sends it. Records start **Unclaimed**. Use **Confirm cash handed over** after
  giving the customer their cash.
- **Cash-In:** your shop account sends to the customer's receiving account.
  Records start **Pending**. Use **Confirm transfer completed** after sending the
  money. These records then show **Completed** and their completion time.

Completed transfers and claimed cash-outs cannot be completed again. Existing
cash-out records keep their original details and are automatically labeled Cash-Out.

Search one to five reference digits, including a partial ending such as `7890`.
Searches include all dates and both services unless you choose a service, status,
or shop-account filter. The service column distinguishes the direction.

Matching service type, shop account, calendar date, amount, and reference ending
triggers a duplicate-entry warning, including for previously completed records.
Opposite directions can share a reference ending. Review the matches before
choosing to save another record of the same type.

Fees stack using the defaults below:

| Cash-in / cash-out amount | Suggested fee |
|---|---|
| PHP 1–499 | PHP 5 |
| PHP 500–999 | PHP 10 |
| PHP 1,000 | PHP 15 |
| PHP 1,500 | PHP 25 |
| PHP 2,000 | PHP 30 |

Each full PHP 1,000 adds PHP 15. A positive remainder below PHP 500 adds PHP 5;
a remainder of PHP 500 or more adds PHP 10. Amounts with centavos follow the same
thresholds. **Fee rules** lets you edit the block amount, remainder split, and
three fees, with example calculations before saving.

The transaction fee prefills automatically. Typing in it creates a custom fee
that stays in place if you change the amount. **Use suggested fee** returns to
automatic calculation. Zero-fee overrides are supported. Saved transactions retain
their recorded fees when the rules change.

Cash-in/out amounts and service fees have their own shared ledger. Product sales, product
profit figures, and inventory are independent of cash-out records.

**Cash In / Out → Fee totals** shows service-fee totals for today, this week, this
month, and this year, with claimed and unclaimed portions and transaction counts.
Totals use transfer dates and each transaction's saved fee, including overrides.
Weeks start Monday; months and years follow the calendar, through today. These
totals cover all shop accounts and are independent of transaction-search filters.
Choose **Both services**, **Cash-In**, or **Cash-Out** to report combined or
individual service fees. Each period also shows the Cash-In/Cash-Out breakdown.
Recording or completing a transfer updates the totals; reopening the tab or
selecting **Refresh fee totals** also refreshes them.

## Verification

With a working graphical display, run:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The checks use temporary databases and cover responsive layouts, sign-in roles,
product editing, checkout, quick access, shopping lists, payments, and reporting.
They also cover password migration, safe database imports, custom audio handling,
installer update/rollback, uninstall data preservation, and license/source packaging.
Cash-out checks also cover fee boundaries, overrides, duplicate warnings, partial
references, concurrent claims, and separation from product sales. Its core checks
can run without a graphical display:

```bash
.venv/bin/python -m unittest discover -s tests -p test_cash_out.py -v
```

## License and third-party materials

Tindahan System's original project code is licensed under the **MIT License**.
Copyright (c) 2026 **Saiken Studio**. See [LICENSE](LICENSE) for the complete terms.

Dependencies retain their own copyrights and licenses. The reviewed Linux
packages include [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), full license
texts, and a version/origin/checksum manifest. Pygame and application source,
with rebuild instructions, accompany the app and are also supplied as a separate
`Tindahan-System-<version>-sources.tar.gz` release file. Choose **Licenses** in
the app or Linux setup/uninstaller to read or save the notices.

See the [third-party audit](docs/THIRD_PARTY_AUDIT.md) and
[library source and rebuild instructions](packaging/third_party/SOURCE_CODE.md)
for the packaged materials and platform review status. Store databases, personal
checkout audio, virtual environments, and generated packages are excluded from
the Git repository.
