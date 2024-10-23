
class BloomFilter:
    def __init__(self):
        self.bits = 0

    def _hashes(self, key):
        # Get a 32-bit hash value
        hash_value = abs(hash(key) % (1 << 32))

        # Split into two 16 bit values
        low_bits = hash_value & 0xFFFF
        high_bits = (hash_value >> 16) & 0xFFFF
        return low_bits, high_bits


    def add(self, key):
        low_pos, high_pos = self._hashes(key)
        self.bits |= 1 << low_pos
        self.bits |= 1 << high_pos

    def might_contain(self, key):
        low_pos, high_pos = self._hashes(key)
        return (self.bits & (1 << low_pos)) and (self.bits & (1 << high_pos))

    def _true_bits(self):
        return bin(self.bits).count('1')
    #counts the number of 1s present in the binary string



#OPTIONAL
#list of good: https://dataforseo.com/free-seo-stats/top-1000-websites
#can download a csv with the top1000 most frequented websites in the us

#list of bad: https://github.com/stamparm/blackbook
#can download a raw TXT of known malware domains, the list should be updating
