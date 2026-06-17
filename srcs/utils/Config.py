from typing import Any
from sys import stderr
from constants import Colors, ZoneTypes
from .Hub import Hub, Connection

CONNECTION_FORMAT = ('Expected format - "<start_zone>-<end_zone> '
                     '[max_link_capacity=<positive integer>(optional)]"')
HUB_FORMAT = ('Expected format - "<name> <x> <y> '
              '[<metadata_key>=<metadata_value> ...(optional)]".')


class ConfigError(Exception):
    """Handles bad configuration."""
    pass


class Config():
    def __init__(self, filename: str) -> None:
        """
           Parses and saves all simulation settings.

        Attributes:

        start_hub: Hub - Hub from where the drones part
        end_hub: Hub - Drones' final destination
        nb_drones: int - Number of drones
        hubs: list - List of all hubs in the simulation
        connections: list - List of all zone pairs that are
            connected
        """
        parsed: dict[str, Any] = {'hubs': [], 'connections': []}
        self.parser(filename, parsed)
        self.start_hub: Hub = parsed['start_hub']
        self.end_hub: Hub = parsed['end_hub']
        self.nb_drones: int = parsed['nb_drones']
        self.hubs: list[Hub] = parsed['hubs']
        self.connections: list[Connection] = parsed['connections']

    def parser(self, filename: str, parsed: dict[str, Any]) -> None:
        """
        Parses the text configuration file line by line into
        practical data structures.

        filename: str - path to the source file from the directory
        in which the script is being run. Use join from os.path to
        concatenate subdirectories if project portability to other
        OSs is a concern.
        """

        f_lines: list[str]
        try:
            with open(filename, "r") as f:
                f_lines = f.read().split('\n')
        except FileNotFoundError:
            print(f'Error: file "{filename}" not found.', file=stderr)
            exit(1)
        is_first = True
        for i, line in enumerate(f_lines):

            comment: int = line.find('#')
            if comment != -1:
                line = line[:comment].strip()
            if not line:
                continue
            try:
                key: str
                value: str
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip()

                if key not in ['nb_drones', 'start_hub',
                               'hub', 'end_hub', 'connection']:
                    raise ConfigError('Not a valid configuration field key.')

                if is_first:
                    parsed['nb_drones'] = self.parse_first_line(key, value)
                    is_first = False

                self.parse_line(key, value, parsed)
            except ConfigError as e:
                print(f'Error in {filename} (line {i + 1}): {e}', file=stderr)
                exit(1)

        try:

            if not parsed.get('start_hub'):
                raise ConfigError('No "start_hub" defined.')
            if not parsed.get('end_hub'):
                raise ConfigError('No "end_hub" defined.')
        except ConfigError as e:
            print(f'Error in {filename}: {e}.')
            exit(1)

    def parse_first_line(self, key: str, value: str) -> int:
        """
        Checks if first line defines "nb_drones".

        key: str - Should be "nb_drones".

        value: str - Should be a positive integer.
        """
        if key != 'nb_drones':
            raise ConfigError('First line field key must be "nb_drones".')
        try:
            nb_drones: int = int(value)
            if nb_drones < 1:
                raise ValueError
            return nb_drones
        except (TypeError, ValueError):
            raise ConfigError('"nb_drones" value must be a positive integer.')

    def parse_line(self, key: str, value: str, parsed: dict[str, Any]) -> None:
        """
        Depending on which of the valid keys is passed, parse_line will
        parse and validate each argument set accordingly, storing them
        in a dictionary to later be turned into a Config obj.

        key: str - One of the 4 valid keys after "nb_drones":
        "start_hub", "end_hub", "hub" or "connection"

        value: str - Values to be parsed, validated and assigned.

        parsed: dict[str, Any] - Storage to keep track of all parsed data.

        """
        match key:
            case 'start_hub':
                if parsed.get('start_hub'):
                    raise ConfigError('Multiple definition of "start_hub".')
                parsed['start_hub'] = self.parse_hub(value.split(None, 3))
                parsed['hubs'].append(parsed['start_hub'])
            case 'end_hub':
                if parsed.get('end_hub'):
                    raise ConfigError('Multiple definition of "end_hub".')
                parsed['end_hub'] = self.parse_hub(value.split(None, 3))
                parsed['hubs'].append(parsed['end_hub'])
            case 'hub':
                parsed['hubs'].append(self.parse_hub(value.split(None, 3)))
            case 'connection':
                parsed['connections'].append(
                    self.parse_connection(value.split(None, 1), parsed))

    def parse_hub(self, args: list[str]) -> Hub:
        """
        Will create an Hub obj my parsing the list of
        arguments (args: list[str])

        """
        parsed: dict[str, Any] = {}
        args_len: int = len(args)

        if args_len < 3:
            raise ConfigError('Insufficient arguments for hub field. ' +
                              HUB_FORMAT)

        if args_len > 4:
            print(args_len)
            print(args)
            raise ConfigError('Too many arguments for hub field. ' +
                              HUB_FORMAT)

        if args_len > 3:
            if not args[3].startswith('[') or not args[3].endswith(']'):
                raise ConfigError(f'"{args[3]}" is not a valid ' +
                                  'metadata argument. ' +
                                  HUB_FORMAT)
            parsed.update(self.extract_hub_metadata(args[3][1:-1]))

        if args[0].find('-') != -1:
            raise ConfigError('Hub name can\'t have "-".')
        parsed['name'] = args[0]

        try:
            parsed['x'] = int(args[1])
        except TypeError:
            raise ConfigError(f'"{args[1]}" is not a positive integer.')

        try:
            parsed['y'] = int(args[2])
        except TypeError:
            raise ConfigError(f'"{args[2]}" is not a positive integer.')

        return Hub(**parsed)

    def extract_hub_metadata(self, metadata: str) -> dict[str, Any]:
        """
        Extractor made specifically for hub kind metadata.

        metadata: str - string with the key/value pairs for hub
        metadata with the brackets already cut off
        """
        parsed: dict[str, Any] = {}
        meta_pairs: list[str] = metadata.split()
        for pair in meta_pairs:
            key: str
            value: str
            key, _, value = pair.partition('=')
            key = key.strip()
            value = value.strip()
            if parsed.get(key):
                raise ConfigError(f'Repeated key "{key}".')
            match key:
                case 'color':
                    try:
                        parsed['color'] = Colors(value)
                    except ValueError:
                        raise ConfigError(f'"{value}" is not a valid color. ' +
                                          'Valid colors: ' +
                                          f'{[c.value for c in Colors]}.')
                case 'zone':
                    try:
                        parsed['zone'] = ZoneTypes(value)
                    except ValueError:
                        raise ConfigError(f'"{value}" is not a valid ' +
                                          'zone type. Valid zone types: ' +
                                          f'{[z.value for z in ZoneTypes]}.')
                case 'max_drones':
                    try:
                        parsed['max_drones'] = int(value)
                        if parsed['max_drones'] < 1:
                            raise ValueError
                    except (TypeError, ValueError):
                        raise ConfigError(f'"{value}" is not a positive ' +
                                          'integer.')
                case _:
                    raise ConfigError(f'"{key}" is not a valid metadata key.')
        return parsed

    def parse_connection(self, args: list[str],
                         parsed: dict[str, Any]) -> Connection:
        connection: dict[str, Any] = {}
        """
        Will create a Connection obj my parsing the list of
        arguments and checking them against already registered Hubs
        and Connections.

        args: list[str] - argument list as strings.

        parsed: dict[str, Any] - dictionary for updating and lookup.

        """

        args_len: int = len(args)

        if args_len < 1:
            raise ConfigError('Insufficient arguments for connection field. ' +
                              CONNECTION_FORMAT)
        if args_len > 2:
            raise ConfigError('Too many arguments for connection field. ' +
                              CONNECTION_FORMAT)
        if args_len > 1:
            if not args[1].startswith('[') or not args[1].endswith(']'):
                raise ConfigError('Second argument is not a ' +
                                  'valid metadata argument. ' +
                                  HUB_FORMAT)
            connection.update(self.extract_connection_metadata(args[1][1:-1]))

        start_end: list[str] = [z.strip() for z in
                                args[0].split('-') if z.strip() != '']

        if len(start_end) != 2:
            raise ConfigError('First connection field ' +
                              'argument must be comprised of ' +
                              'exactly 2 zone names.')
        zone1: Hub
        zone2: Hub
        zone1, zone2 = self.validate_connection(start_end[0],
                                                start_end[1], parsed)
        zone1.neighbours.append(zone2)
        zone2.neighbours.append(zone1)
        connection['zone1'] = zone1
        connection['zone2'] = zone2
        return Connection(**connection)

    def extract_connection_metadata(self, metadata: str) -> dict[str, int]:
        """
        Extractor made specifically for connection kind metadata.

        metadata: str - string with the key/value pairs for connection
        metadata with the brackets already cut off.
        """
        max_link_capacity: int

        key: str
        val: str
        key, _, val = metadata.partition('=')
        key = key.strip()
        val = val.strip()
        if key != 'max_link_capacity':
            raise ConfigError(f'"{key}" is not a valid key. ' +
                              'Valid key: "max_link_capacity".')

        try:
            max_link_capacity = int(val)
            if max_link_capacity < 1:
                raise ValueError
            return {'max_link_capacity': max_link_capacity}
        except (TypeError, ValueError):
            raise ConfigError('"max_link_capacity" value is not a ' +
                              'valid integer.')

    def validate_connection(self, zone1: str, zone2: str,
                            parsed: dict[str, Any]) -> tuple[Hub, Hub]:
        """
        Checks if connection configuration uses names from already
        registered hubs. It will also check if the zone pair has already
        been saved in another Connection obj.
        """

        hubs: list[Hub] = parsed['hubs']
        z1: Hub | None = None
        z2: Hub | None = None

        for hub in hubs:
            if hub.name == zone1:
                z1 = hub
            if hub.name == zone2:
                z2 = hub

        if not z1:
            raise ConfigError(f'Unknown hub name "{zone1}".')

        if not z2:
            raise ConfigError(f'Unknown hub name "{zone2}".')

        if zone1 == zone2:
            raise ConfigError('Connection zone 1 can\'t be the same ' +
                              'as connection zone 2.')

        for connection in parsed['connections']:
            if {zone1, zone2} == {connection.zone1.name,
                                  connection.zone2.name}:
                raise ConfigError('Repeated zone connection.')

        return (z1, z2)


if __name__ == '__main__':
    filename = 'maps/easy/01_linear_path.txt'
    config = Config(filename)
    print(config.start_hub)
