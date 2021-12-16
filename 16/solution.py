def parse(lines):
    packet = lines[0].strip()
    return packet

def lazy_read_bits(hexstring):
    for h in hexstring:
        bits = bin(int(h, base=16))[2:]
        padded = bits.zfill(4)
        for b in padded:
            yield b


class Packet:
    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id
        self.done = False
        self.length = 6
        
    def extend(self, bits):
        raise Exception('Not implemented')
        
    def get_value(self):
        raise Exception('Not implemented')
    
    def build_packet(header):
        version, type_id = int(header[:3], base=2), int(header[3:], base=2)
        Packet.version_counter += version
        if type_id == 4:
            return LiteralPacket(version, type_id)
        else:
            return OperatorPacket(version, type_id)
    
    bits = None
    i = 0
    version_counter = 0
    
    def reset():
        Packet.bits = None
        Packet.i = 0
        Packet.version_counter = 0
    
    def parse(packet):
        while packet.needs_bits > 0:
            need = packet.needs_bits
            Packet.i += need
            packet.extend(''.join(Packet.bits[Packet.i-need:Packet.i]))
        while not packet.done:
            h = Packet.get_new_header()
            p = Packet.build_packet(h)
            Packet.parse(p)
            packet.add_subpacket(p)
            
    def get_new_header():
        header = Packet.bits[Packet.i:Packet.i+6]
        Packet.i += 6
        return ''.join(header)


class LiteralPacket(Packet):
    def __init__(self, version, type_id):
        super().__init__(version, type_id)
        self.needs_bits = 5
        self.bin_value = ''
        
    def extend(self, bits):
        self.length += len(bits)
        self.bin_value += bits[1:]
        if bits[0] == '0':
            self.needs_bits = 0
            self.done = True
            self.value = int(self.bin_value, base=2)
        
    def get_value(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, version, type_id):
        super().__init__(version, type_id)
        self.needs_bits = 1
        self.operator_type = None
        self.subpackets = []
        self.subpacket_count, self.subpacket_bits = None, None
        self.value = None
        
    def extend(self, bits):
        if self.operator_type == None:
            self.operator_type = int(bits)
            self.needs_bits = 15 if self.operator_type == 0 else 11
            self.length += 1
            
        elif self.needs_bits  == 15:
            self.subpacket_bits = int(bits, base=2)
            self.needs_bits = 0
            self.length += 15
        elif self.needs_bits == 11:
            self.subpacket_count = int(bits, base=2)
            self.needs_bits = 0
            self.length += 11
    
    def add_subpacket(self, packet):
        self.subpackets.append(packet)
        if not self.subpacket_count == None:
            self.subpacket_count -= 1
            if self.subpacket_count == 0:
                self.done = True
                self.length += sum([p.length for p in self.subpackets])
        if not self.subpacket_bits == None:
            self.subpacket_bits -= packet.length
            if self.subpacket_bits <= 0:
                self.done = True
                self.length += sum([p.length for p in self.subpackets])
        
    def get_value(self):
        value = 0
        if not self.value == None:
            return self.value
        elif self.type_id == 0:
            value = sum([p.get_value() for p in self.subpackets])
        elif self.type_id == 1:
            value = 1
            for p in self.subpackets:
                value *= p.get_value()
        elif self.type_id == 2:
            value = min([p.get_value() for p in self.subpackets])
        elif self.type_id == 3:
            value = max([p.get_value() for p in self.subpackets])
        elif self.type_id == 5:
            value = 1 if self.subpackets[0].get_value() > self.subpackets[1].get_value() else 0
        elif self.type_id == 6:
            value = 1 if self.subpackets[0].get_value() < self.subpackets[1].get_value() else 0
        elif self.type_id == 7:
            value = 1 if self.subpackets[0].get_value() == self.subpackets[1].get_value() else 0
        self.value = value
        return self.value



def main(arg):
    packet = parse(arg)
    bit_iterator = lazy_read_bits(packet)
    bits = list(bit_iterator)
    Packet.reset()
    Packet.bits = bits
    
    header = Packet.get_new_header()
    top_packet = Packet.build_packet(header)
    Packet.parse(top_packet)
    
    print(Packet.version_counter)
    
    print(top_packet.get_value())
    


TEST_INPUT = """9C0141080250320F1802104A08""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
