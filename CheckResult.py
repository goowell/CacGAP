'''demo'''
import csv
from collections import OrderedDict


def parse_config():
    gap_start = False
    offset_start = False
    gap_limits = []
    offset_limits = []

    with open('mea2cfg.conf') as cf:
        for l in cf.readlines():
            if offset_start:
                if l.startswith(' '):
                    offset_limits.append(float(l.split(':')[1]))
                else:
                    offset_start = False
            if gap_start:
                if l.startswith(' '):
                    gap_limits.append(float(l.split(':')[1]))
                else:
                    gap_start = False

            if offset_start or gap_start:
                continue

            if l.startswith('OffsetLimits:'):
                offset_start = True
                gap_start = False

            if l.startswith('GapLimits:'):
                gap_start = True
                offset_start = False
    formatted_gap_limits = [(gap_limits[i * 2], gap_limits[i * 2 + 1])
                            for i in range(int(len(gap_limits) / 2) -1, -1, -1)]
    formated_offset_limits = [(offset_limits[i * 2], offset_limits[i * 2 + 1])
                              for i in range(int(len(offset_limits) / 2) -1, -1, -1)]
    return formatted_gap_limits, formated_offset_limits


def generate_xx_index(index):
    base = ord('A')
    return chr(base + int(index / 26)) + chr(base + (index % 26))


def compare_limit(limit, v):
    v = float(v)
    if v >= limit[1] and v <= limit[0]:
        return 0
    elif v > limit[0]:
        return v - limit[0]
    else:
        return v - limit[1]


def caculate_all():
    import os
    gap_index = '30{0}-GAP'
    offset_index = '31{0}-OFF'
    gap_ng_index = 'GAP{0}NG'
    offset_ng_index = 'OFF{0}NG'
    diff_prefix = 'diff{0}'
    gap_skips = [0, 10, 24, 34]
    gap_limits = list(reversed([(0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.35, 0.24), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18),
                  (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18), (0.36, 0.18)]))
    offset_limits = list(reversed([(0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23),
                     (0.03, -0.23), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.04, -0.2), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23), (0.03, -0.23)]))
    points_mapping = [
        ('Gap_1_y_7', '30BV-GAP'),
        ('Gap_2_y_7', '30BJ-GAP'),
        ('Gap_3_y_7', '30AL-GAP'),
        ('Gap_4_y_7', '30AX-GAP'),
        ('Gap_1_x_7', '30AB-GAP'),
        ('Gap_3_x_7', '30AJ-GAP'),
        ('Gap_2_x_7', '30BH-GAP'),
        ('Gap_4_x_7', '30AZ-GAP')
    ]
    try:
        gap_limits, offset_limits = parse_config()
    except FileNotFoundError:
        print('not config file found, use the default value: gap_limits, offset_limits')
        print(gap_limits, offset_limits)
    except Exception as exc:
        print("error raised when parsing config file:", exc)
        return

    for idx in gap_skips:
        gap_limits.insert(idx, None)

    for fn in os.listdir():
        try:
            if fn.endswith('.csv') and not fn.startswith('done'):
                print("start to parse file: " + fn)
                rows = []
                headers = []
                with open(fn) as csvf:
                    all_data = csv.DictReader(csvf)
                    headers = all_data.fieldnames
                    for d in all_data:
                        for i in range(0, 48):
                            xx = generate_xx_index(i)
                            ng_idx = offset_ng_index.format(xx)
                            idx = offset_index.format(xx)
                            d.update({ng_idx: compare_limit(
                                offset_limits[i], d[idx])})
                            if i not in gap_skips:
                                ng_idx = gap_ng_index.format(xx)
                                idx = gap_index.format(xx)
                                d.update(
                                    {ng_idx: compare_limit(gap_limits[i], d[idx])})
                        for dp in points_mapping:
                            d.update({diff_prefix.format(dp[1].split('-')[0]): float(d[dp[0]])-float(d[dp[1]])})
                        rows.append(d)
                new_headers = [x for x in list(rows[0].keys()) if x not in headers]
                headers.extend(sorted(new_headers))

                print("   output to: " + 'done_' + fn)
                with open('done_' + fn, 'w', newline='') as csvf:
                    writer = csv.DictWriter(csvf, headers)
                    writer.writeheader()
                    writer.writerows(rows)
        except Exception as exc:
            print("   invalid data format in file: " + fn, "   error: ", exc)


def main():
    import datetime
    print('program started...')
    start = datetime.datetime.now()
    caculate_all()
    print('done in {0}'.format((datetime.datetime.now() - start)))


if __name__ == '__main__':
    main()
