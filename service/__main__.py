"""
 _____             _                    _   _           ______          _        _
/  __ \           | |                  | | | |          | ___ \        | |      | |
| /  \/ __ _ _ __ | |_ _   _ _ __ ___  | |_| |__   ___  | |_/ /_ _  ___| | _____| |_
| |    / _` | '_ \| __| | | | '__/ _ \ | __| '_ \ / _ \ |  __/ _` |/ __| |/ / _ \ __|
| \__/\ (_| | |_) | |_| |_| | | |  __/ | |_| | | |  __/ | | | (_| | (__|   <  __/ |_
 \____/\__,_| .__/ \__|\__,_|_|  \___|  \__|_| |_|\___| \_|  \__,_|\___|_|\_\___|\__|
			| |
			|_|
=====================================================================================
						Copyright 2020 - Jordan Maxwell
						GNU General Public License v3.0
                      Written by Jordan Maxwell 05/09/2020
"""

from service import start_bot

def main() -> int:
    """
    Main entry point for the PacketBot application
    """

    return start_bot()

if __name__ == '__main__':
    sys.exit(main())