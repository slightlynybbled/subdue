from subdue import ThermocoupleReader

tc = ThermocoupleReader()

first_channel = 1
second_channel = 4

tc.enable_channel(channel_number=first_channel, tc_type='K')

print('--- reading channel 1 ---')
for _ in range(5):
    print(tc.read_one(first_channel))

print('--- reading channels 1 and 4 ---')
tc.enable_channel(channel_number=second_channel, tc_type='K')
for _ in range(5):
    print('{}: {}'.format(first_channel, tc.read_one(first_channel)))
    print('{}: {}'.format(second_channel, tc.read_one(second_channel)))
