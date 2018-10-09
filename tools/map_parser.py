from collections import namedtuple

# Describe the location of a Map pointers table
class MapDescriptor:
    def __init__(self, name, address, length, data_base_address, rooms, invalid_pointers = []):
        self.name = name
        self.address = address
        self.length = length
        self.data_base_address = data_base_address
        self.rooms = rooms
        self.invalid_pointers = invalid_pointers

# Describe the location of an area containing Rooms
RoomsDescriptor = namedtuple('RoomsDescriptor', ['name', 'address', 'length'])

# Represent a room on a Map
RoomPointer = namedtuple('RoomPointer', ['index', 'value', 'address'])

# Represent a Room and its data
class Room:
    def __init__(self, address, length, data):
        self.label = None
        self.address = address
        self.length = length
        self.data = data

def to_camel_case(snake_str):
    """Convert a string from snake_case to CamelCase"""
    return ''.join(w.title() for w in snake_str.split('_'))

class MapParser:
    """Parse a map and its rooms from a MapDescriptor

    Rooms can be divided in several memory areas - this is why a MapDescriptor
    may contain more than one RoomDescriptor.

    Furthermore, some maps contains invalid pointers, targeting memory areas without a room.
    These invalid pointers are stored in the pointers table, but skipped when looking for
    a room.
    """
    def __init__(self, rom_path, map_descriptor):
        self.map_descriptor = map_descriptor
        self.name = self.map_descriptor.name

        with open(rom_path, 'rb') as rom_file:
            rom = rom_file.read()
            self.room_pointers = self._parse_pointers_table(rom, map_descriptor)
            self.rooms_parsers = self._parse_rooms(rom, map_descriptor.rooms)
            self._label_rooms(self.rooms_parsers)

    def room_for_pointer(self, room_pointer):
        """
        Given a pointer in the map pointers table, return the target room.
        Raise if a room cannot be found for a valid pointer.

        Returns: the target Room, or 'None' if the room_pointer is invalid.
        """
        if room_pointer.address in self.map_descriptor.invalid_pointers:
            return None

        room_address = room_pointer.address
        for rooms_parser in self.rooms_parsers:
            for room in rooms_parser.rooms:
                if room.address == room_address:
                    return room

        raise Exception("Cannot find a room for room pointer '0x{:X}'".format(room_address))

    def _room_address(self, room_index, partial_pointer):
        """Return the actual address of the room data from the partial pointer"""

        # Retrieve the base address of data for this room
        data_base_address = self.map_descriptor.data_base_address
        # (data_base_address is allowed to be a lambda expression)
        if callable(data_base_address):
            data_base_address = data_base_address(room_index)

        # Compute the room data address
        return data_base_address + partial_pointer - 0x4000

    def _parse_pointers_table(self, rom, map_descriptor):
        """Return an array of words in the pointers table"""
        # Figure out where the bytes for this pointer are located
        pointers_table_address = map_descriptor.address
        rooms_count = map_descriptor.length // 2
        room_pointers = []

        for room_index in range(0, rooms_count):
            pointer_address = pointers_table_address + (room_index * 2)

            # Grab the two bytes making up the partial pointer
            lower_byte = rom[pointer_address]
            higher_byte = rom[pointer_address + 1]

            # Combine the two bytes into a single pointer (0x byte1 byte2)
            partial_pointer = (higher_byte << 8) + lower_byte

            # Compute the actual address of the room data
            room_address = self._room_address(room_index, partial_pointer)

            # Store the data into the parsed pointers table
            room_pointer = RoomPointer(index = room_index, value = partial_pointer, address = room_address)
            room_pointers.append(room_pointer)

        return room_pointers

    def _parse_rooms(self, rom, rooms_descriptors):
        """Return an array of room parsers for the given room descriptors"""
        rooms_parsers = []
        for rooms_descriptor in rooms_descriptors:
            rooms_parsers.append(RoomsParser(rom, rooms_descriptor))
        return rooms_parsers

    def _label_rooms(self, rooms_parsers):
        """
        Set labels on rooms.

        Labels are generated from the map name and room index, like 'Overworld7A'.
        Unreferenced rooms get special out-of-sequence labels.
        """
        map_prefix = to_camel_case(self.name)

        for room_index, room_pointer in enumerate(self.room_pointers):
            room = self.room_for_pointer(room_pointer)
            if room is not None:
                label = '{}{:02X}'.format(map_prefix, room_index)
                room.label = label

        ## Leftover rooms (having room data but missing from the map) get an 'Unreferenced' label.
        unreferenced_count = 0
        for rooms_parser in self.rooms_parsers:
            for room in rooms_parser.rooms:
                if room.label is None:
                    label = '{}Unreferenced{:02X}'.format(map_prefix, unreferenced_count)
                    room.label = label
                    unreferenced_count += 1


class RoomsParser:
    """
    Parse an area containing rooms description and blocks.

    Some Rooms may be unused in the map. This is why rooms must be
    described (and parsed) separately of the map.
    """
    def __init__(self, rom, rooms_descriptor):
        self.name = rooms_descriptor.name
        self.rooms = self._parse(rom, rooms_descriptor)

    def _parse(self, rom, descriptor):
        """Walk the rooms table, and parse data for each room"""
        rooms = []
        address = descriptor.address
        end_address = descriptor.address + descriptor.length

        while address < end_address:
            room = self._parseRoom(rom, address)
            rooms.append(room)

            address += room.length

        return rooms

    def _parseRoom(self, rom, address):
        """Parse a room data, until we reach the end marker"""
        END_BYTE = 0xFE

        data = []
        i = 0
        roomEnd = False

        while not roomEnd:
            byte = rom[address + i]
            data.append(byte)

            i += 1
            roomEnd = (byte == END_BYTE)

        return Room(address, i, data)