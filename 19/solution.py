import inspect
import math

def parse(lines):
    scanners = []
    beacons = []
    sc_ind = 0
    for l in lines:
        if l.isspace() or l == '':
            s = Scanner(beacons, sc_ind)
            scanners.append(s)
            beacons = []
        elif l.startswith('---'):
            sc_ind = int(''.join([d for d in l.split() if d.isnumeric()]))
        else:
            beacons.append([int(b) for b in l.strip().split(',')])

    s = Scanner(beacons, sc_ind)
    scanners.append(s)
    return scanners

def rotate(rotation_n, coord):
    # rotation_n = number from 0 to 23
    # choose facing direction (x, -x, y, -y, z, -z) and then one of 4 as up direction
    x, y, z = coord
    ind_base = rotation_n//6
    ind_rot= rotation_n%3
    ind_neg = rotation_n%2
    rotations = [
        (x, y, z,),
        (x, -y, -z),
        (x, z, -y),
        (x, -z, y)
     ]
    def shift(r, i):
        (a, b, c) = r
        return [(a, b, c), (b, c, a), (c, a, b)][i]
    rot = rotations[ind_base]
    if ind_neg:
        (a, b, c) = rot
        rot = (-a, -b, c)
    rot = shift(rot, ind_rot)
    return rot

class Scanner:

    def __init__(self, beacons, index):
        self.position = None
        self.beacons = beacons
        self.rotation = None
        self.index = index

    def set_position(self, x, y, z):
        self.position = (x, y, z)

    def set_rot(self, r):
        self.rotation = r

    def get_beacons(self, rotation=None):
        if rotation is None:
            rotation = self.rotation
        bs = [rotate(rotation, b) for b in self.beacons]

        if self.position is not None:
            (x0, y0, z0) = self.position
            bs = [(x-x0, y-y0, z-z0) for (x, y, z) in bs]
        return bs

    def rotate_beacons(self, rot, beacons):
        return [rotate(rot, b) for b in beacons]

    def shift_beacons(self, shift, beacons):
        dx, dy, dz = shift
        return [(x-dx, y-dy, z-dz) for (x, y, z) in beacons]

    def matches(self, other, rotation):
        beacons = self.get_beacons(rotation)
        beacons = self.shift_beacons(other.position, beacons)

        other_beacons = other.get_beacons()

        for (x0, y0, z0) in other_beacons:
            other_shifted = [(x - x0, y - y0, z - z0) for (x, y, z) in other_beacons]
            for (x1, y1, z1) in beacons:
                shifted = [(x-x1, y-y1, z-z1) for (x, y, z) in beacons]
                if len(set(shifted).intersection(set(other_shifted))) >= 12:
                    return True, (x1-x0, y1-y0, z1-z0)

        return False, None
    

def main(arg):
    scanners = parse(arg)
    base_scanner = scanners[0]
    base_scanner.set_position(0, 0, 0)
    base_scanner.set_rot(0)
    matched = [base_scanner]
    from_i = 0
    while not len(matched) == len(scanners):
        new_matched = []
        for first in matched[from_i:]:
            for second in scanners:
                if second in matched or second in new_matched:
                    continue
                for rot in range(24):
                    match, shift = second.matches(first, rot)
                    if match:
                        x, y, z = first.position
                        dx, dy, dz = shift
                        second.set_position(x+dx, y+dy, z+dz)
                        second.set_rot(rot)
                        new_matched.append(second)
                        break
        from_i = len(matched)
        matched += new_matched
        print([m.index for m in matched])
        if len(new_matched) == 0:
            raise Exception("nothing found!")
    all_beacons = set()
    for m in matched:
        for b in m.get_beacons():
            all_beacons.add(b)
    print(len(all_beacons))

    largest_dist = 0
    for s in scanners:
        for t in scanners:
            (a, b, c) = s.position
            (d, e, f) = t.position
            largest_dist = max(largest_dist, abs(a-d)+abs(b-e)+abs(c-f))
    print(largest_dist)

TEST_INPUT = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".split('\n')

if __name__ == "__main__":
    with open("input.txt") as f:
        INPUT = f.readlines()
    print("Test:")
    main(TEST_INPUT)
    print("Input:")
    main(INPUT)
