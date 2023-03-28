# Entry point for spasm, the Sphinx assembler/emulator
# Copyright (C) 2023  Ben Burrill <bburrill98@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from .emulator import Emulator
import sys

def main():
    if len(sys.argv) != 2:
        print(f'Usage: spasm <file>', file=sys.stderr)
        return 1
    else:
        Emulator.run_from_file(sys.argv[1], reraise=False)
        return 0

if __name__ == '__main__':
    sys.exit(main())
